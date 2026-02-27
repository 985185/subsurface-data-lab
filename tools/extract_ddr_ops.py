#!/usr/bin/env python3
"""
extract_ddr_ops.py

Batch-extract DDR "Operations" table rows from Volve-style DDR HTML files and write JSONL events.

Inputs:
- One HTML file or a folder containing many HTML files.

Outputs:
- One JSONL file per HTML file, written to an output folder.

Design goals:
- Deterministic extraction (no AI)
- Stable field contract
- Minimal dependencies (beautifulsoup4 only)

Example:
  python tools/extract_ddr_ops.py --input "/path/to/ddr_html" --output "./out_events"

Notes:
- This script attempts to parse wellbore/date from the DDR header text ("Wellbore:" and "Period:").
- If header parsing fails, it will fall back to filename parsing when possible.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

try:
    from bs4 import BeautifulSoup  # type: ignore
except ImportError:
    print("ERROR: Missing dependency 'beautifulsoup4'. Install with: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


@dataclass
class ExtractResult:
    input_file: Path
    output_file: Optional[Path]
    events_written: int
    wellbore: Optional[str]
    date: Optional[str]
    error: Optional[str]


WELLBORE_RE = re.compile(r"Wellbore:\s*([0-9/.\-\sA-Za-z]+?)\s+Period:", re.IGNORECASE)
PERIOD_RE = re.compile(
    r"Period:\s*(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}\s*-\s*(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}",
    re.IGNORECASE,
)

# Example filename patterns:
# 15_9_19_A_1997_10_10.html
# 15_9_F_15_A_2008_12_17.html
FILENAME_DATE_RE = re.compile(r".*_(\d{4})_(\d{2})_(\d{2})\.html$", re.IGNORECASE)


def safe_read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def parse_header_wellbore_and_date(soup: BeautifulSoup) -> Tuple[Optional[str], Optional[str]]:
    """
    Try to parse wellbore and date from DDR header text.
    """
    text = soup.get_text(" ", strip=True)

    wellbore = None
    m = WELLBORE_RE.search(text)
    if m:
        wellbore = m.group(1).strip()

    date = None
    m = PERIOD_RE.search(text)
    if m:
        date = m.group(1)

    return wellbore, date


def parse_date_from_filename(html_path: Path) -> Optional[str]:
    m = FILENAME_DATE_RE.match(html_path.name)
    if not m:
        return None
    y, mo, d = m.group(1), m.group(2), m.group(3)
    try:
        datetime(int(y), int(mo), int(d))
    except ValueError:
        return None
    return f"{y}-{mo}-{d}"


def parse_wellbore_from_filename(html_path: Path) -> Optional[str]:
    """
    Best-effort: convert '15_9_F_15_A_2008_12_17.html' -> '15/9-F-15 A'
    Not guaranteed; header parsing is preferred.
    """
    stem = html_path.stem  # without .html
    parts = stem.split("_")
    if len(parts) < 4:
        return None

    # We expect: 15, 9, F, 15, A, 2008, 12, 17  (varies by well)
    # We'll take everything up to the year as "well parts".
    # Find the first 4-digit year token:
    year_idx = None
    for i, p in enumerate(parts):
        if re.fullmatch(r"\d{4}", p):
            year_idx = i
            break
    if year_idx is None or year_idx < 2:
        return None

    well_tokens = parts[:year_idx]  # e.g. ["15","9","F","15","A"]
    if len(well_tokens) < 2:
        return None

    # Build "15/9-..." prefix
    prefix = f"{well_tokens[0]}/{well_tokens[1]}"
    rest = well_tokens[2:]

    if not rest:
        return prefix

    # Join rest with '-' except final letter part separated by space
    # If last token is a single letter (A/B/C), treat as suffix after space.
    suffix_letter = rest[-1] if len(rest[-1]) == 1 and rest[-1].isalpha() else None
    core = rest[:-1] if suffix_letter else rest

    core_str = "-".join(core) if core else ""
    if core_str:
        wb = f"{prefix}-{core_str}"
    else:
        wb = prefix

    if suffix_letter:
        wb = f"{wb} {suffix_letter}"

    return wb


def find_operations_table(soup: BeautifulSoup):
    """
    Volve DDR HTML commonly uses id='operationsInfoTable'.
    If id not found, fall back to searching by header text.
    """
    table = soup.find("table", {"id": "operationsInfoTable"})
    if table is not None:
        return table

    # Fallback: locate a table containing "Remark" and "Activity" headers
    for t in soup.find_all("table"):
        header_text = t.get_text(" ", strip=True).lower()
        if "remark" in header_text and "activity" in header_text and "state" in header_text:
            return t

    return None


def extract_operations_events(html_path: Path) -> ExtractResult:
    try:
        html = safe_read_text(html_path)
        soup = BeautifulSoup(html, "html.parser")

        wellbore, date = parse_header_wellbore_and_date(soup)

        # Fallbacks
        if date is None:
            date = parse_date_from_filename(html_path)
        if wellbore is None:
            wellbore = parse_wellbore_from_filename(html_path)

        table = find_operations_table(soup)
        if table is None:
            return ExtractResult(
                input_file=html_path,
                output_file=None,
                events_written=0,
                wellbore=wellbore,
                date=date,
                error="Could not find Operations table (operationsInfoTable).",
            )

        rows = table.find_all("tr")
        if not rows or len(rows) < 2:
            return ExtractResult(
                input_file=html_path,
                output_file=None,
                events_written=0,
                wellbore=wellbore,
                date=date,
                error="Operations table has no data rows.",
            )

        # Skip header row
        data_rows = rows[1:]

        events: List[Dict] = []
        for r in data_rows:
            cols = [c.get_text(" ", strip=True) for c in r.find_all("td")]

            # Expected: start, end, end depth, activity, state, remark
            if len(cols) < 6:
                # Skip malformed rows silently (common in odd HTML)
                continue

            start, end, depth, activity, state, remark = cols[:6]

            event = {
                "wellbore": wellbore,
                "date": date,
                "start_time": start,
                "end_time": end,
                "activity_raw": activity,
                "state": state,
                "remark": remark,
                "end_depth_md": depth if depth != "" else None,
                "event_type": None,
                "source_file": html_path.name,
            }
            events.append(event)

        out_path = html_path.with_suffix("").name + "_events.jsonl"
        return ExtractResult(
            input_file=html_path,
            output_file=Path(out_path),
            events_written=len(events),
            wellbore=wellbore,
            date=date,
            error=None,
        ), events  # type: ignore

    except Exception as e:
        return ExtractResult(
            input_file=html_path,
            output_file=None,
            events_written=0,
            wellbore=None,
            date=None,
            error=str(e),
        )


def iter_html_files(input_path: Path, recursive: bool) -> Iterable[Path]:
    if input_path.is_file() and input_path.suffix.lower() == ".html":
        yield input_path
        return

    if input_path.is_dir():
        pattern = "**/*.html" if recursive else "*.html"
        for p in sorted(input_path.glob(pattern)):
            if p.is_file():
                yield p
        return

    raise FileNotFoundError(f"Input path not found: {input_path}")


def write_jsonl(output_dir: Path, out_name: str, events: List[Dict], overwrite: bool) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / out_name

    if out_path.exists() and not overwrite:
        raise FileExistsError(f"Output exists (use --overwrite): {out_path}")

    with out_path.open("w", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")

    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract DDR Operations table to JSONL events.")
    parser.add_argument("--input", required=True, help="Path to a DDR HTML file or a folder of HTML files.")
    parser.add_argument("--output", required=True, help="Output folder for JSONL files.")
    parser.add_argument("--recursive", action="store_true", help="Recursively search for .html files in subfolders.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output files.")
    parser.add_argument("--dry-run", action="store_true", help="Parse and report counts, but do not write outputs.")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()

    html_files = list(iter_html_files(input_path, args.recursive))
    if not html_files:
        print("No .html files found.", file=sys.stderr)
        return 2

    total_events = 0
    ok_files = 0
    failed_files = 0

    for html_path in html_files:
        try:
            # extract (returns (meta, events))
            res_events = extract_operations_events(html_path)
            # Because extract_operations_events returns two different shapes on error vs success,
            # handle carefully:
            if isinstance(res_events, tuple) and len(res_events) == 2 and isinstance(res_events[0], ExtractResult):
                res, events = res_events
            else:
                # error case only
                res = res_events  # type: ignore
                events = []  # type: ignore

            if res.error:
                failed_files += 1
                print(f"[FAIL] {html_path.name} :: {res.error}")
                continue

            out_name = html_path.with_suffix("").name + "_events.jsonl"
            if args.dry_run:
                print(f"[OK]   {html_path.name} -> {len(events)} events (dry-run)")
            else:
                out_path = write_jsonl(output_dir, out_name, events, overwrite=args.overwrite)
                print(f"[OK]   {html_path.name} -> {len(events)} events -> {out_path}")

            ok_files += 1
            total_events += len(events)

            # quick header sanity visibility
            if res.wellbore or res.date:
                print(f"       parsed header: wellbore={res.wellbore!r}, date={res.date!r}")

        except Exception as e:
            failed_files += 1
            print(f"[FAIL] {html_path.name} :: {e}")

    print("\nSummary")
    print(f"  HTML files: {len(html_files)}")
    print(f"  OK: {ok_files}")
    print(f"  Failed: {failed_files}")
    print(f"  Total events written: {total_events}" if not args.dry_run else f"  Total events parsed: {total_events}")

    return 0 if failed_files == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
