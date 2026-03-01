#!/usr/bin/env python3
"""
tools/apply_event_type.py

Reads a JSONL of DDR "events" and writes a JSONL with an added/updated field:
    event_type

This version is intentionally simple and robust:
- First uses structured "domain -- subdomain" patterns (your activity_raw examples).
- Then falls back to keyword matching across activity_raw + remark.
- If nothing matches, event_type = "UNKNOWN".

Usage:
  python tools/apply_event_type.py --in  path/to/events_raw.jsonl --out path/to/events_typed.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, Optional


# -----------------------------
# Helpers
# -----------------------------

def norm(s: Optional[str]) -> str:
    if not s:
        return ""
    return " ".join(s.strip().lower().split())


def parse_structured_activity(activity_raw: str) -> tuple[str, str]:
    """
    Parse patterns like:
      "completion -- completion string"
      "formation evaluation -- log"
    Returns (domain, subdomain) in normalized lowercase.
    If no delimiter, returns ("", "").
    """
    a = norm(activity_raw)
    if " -- " not in a:
        return ("", "")
    left, right = a.split(" -- ", 1)
    return (left.strip(), right.strip())


# -----------------------------
# Core classifier
# -----------------------------

# Your desired event_type vocabulary (keep stable):
# DRILLING, TRIP, CASING, CEMENTING, WIRELINE, PERFORATION,
# MUD_CONDITIONING, EQUIPMENT_FAILURE, WELL_CONTROL,
# INTEGRITY_TEST, WAITING, UNKNOWN

DOMAIN_MAP = {
    # Common structured "domain" buckets seen in Volve DDR exports
    "drilling": "DRILLING",
    "moving": "WAITING",  # "moving -- skid" is basically non-drilling ops / waiting-ish for our purposes
    "interruption": "EQUIPMENT_FAILURE",  # interruptions often are failures; refined below with subdomain
    "formation evaluation": "WIRELINE",   # logs often wireline/LWD; refined below
    "completion": "CASING",               # completion string / BOP often fits casing/completion bucket; refined below
    "workover": "WAITING",
    "plug abandon": "WAITING",
    "testing": "INTEGRITY_TEST",
    "well control": "WELL_CONTROL",
}

# More specific structured (domain, subdomain) overrides
STRUCTURED_OVERRIDES = {
    ("moving", "skid"): "WAITING",
    ("interruption", "fish"): "EQUIPMENT_FAILURE",
    ("interruption", "rig up/down"): "WAITING",
    ("interruption", "maintain"): "EQUIPMENT_FAILURE",
    ("interruption", "other"): "EQUIPMENT_FAILURE",

    ("formation evaluation", "log"): "WIRELINE",
    ("formation evaluation", "wire line"): "WIRELINE",
    ("formation evaluation", "wireline"): "WIRELINE",

    ("completion", "completion string"): "CASING",
    ("completion", "bop/wellhead equipment"): "CASING",
    ("completion", "test scsssv"): "INTEGRITY_TEST",

    ("plug abandon", "mechanical plug"): "WAITING",
    ("plug abandon", "mill"): "WAITING",

    ("workover", "rig up/down"): "WAITING",
    ("workover", "wire line"): "WIRELINE",
}

# Keyword fallback rules (applies if structured mapping fails or is absent)
# Order matters: first match wins.
KEYWORD_RULES: list[tuple[str, str]] = [
    # Well control / kicks
    (r"\b(kick|well control|shut[\s-]?in|bop test due to kick|losses|lost circulation)\b", "WELL_CONTROL"),

    # Casing / cementing
    (r"\b(run casing|casing\b|liner\b|shoe\b|centraliz|float collar|hanger)\b", "CASING"),
    (r"\b(cement|cementing|woc\b|wait on cement|bump plug)\b", "CEMENTING"),

    # Trips / BHA handling
    (r"\b(trip|tripping|pull out of hole|p[o0]oh\b|run in hole|r[i1]h\b|backream|reaming)\b", "TRIP"),

    # Wireline / logging / perforation
    (r"\b(wireline|wire line|logging|log run|cbl\b|vdl\b|pl[tf]\b|plt\b|mdt\b|rst\b|formation evaluation)\b", "WIRELINE"),
    (r"\b(perforat|shoot\b)\b", "PERFORATION"),

    # Mud / circulation / conditioning
    (r"\b(condition mud|mud conditioning|circulate|circulation|sweep|viscos|mud weight|pill|clean hole)\b", "MUD_CONDITIONING"),

    # Equipment failure / NPT-ish
    (r"\b(fail|failure|repair|broken|leak|stuck|fish|fishing|packoff|washout|lost tool|motor|mwd|lwd|pump|top drive)\b", "EQUIPMENT_FAILURE"),

    # Waiting / idle / weather
    (r"\b(waiting|wait\b|standby|weather|no operations|n/a|rig move|skid)\b", "WAITING"),

    # Drilling (keep last-ish so it doesn't steal other categories)
    (r"\b(drill|drilling|rotat|tag bottom|make hole|r[o0]p\b)\b", "DRILLING"),

    # Integrity / pressure testing
    (r"\b(test|pressure test|integrity test|leak off test|lot\b|fit test|bop test|negative test|positive test)\b", "INTEGRITY_TEST"),
]


def classify(activity_raw: str, remark: str) -> str:
    """
    Returns one of the canonical event types.
    """
    a = norm(activity_raw)
    r = norm(remark)

    # 1) Structured mapping: "domain -- subdomain"
    domain, sub = parse_structured_activity(a)
    if domain:
        if (domain, sub) in STRUCTURED_OVERRIDES:
            return STRUCTURED_OVERRIDES[(domain, sub)]
        if domain in DOMAIN_MAP:
            # Some light refinement for known domains
            if domain == "interruption":
                # subdomain can imply WAITING vs EQUIPMENT_FAILURE
                if any(x in sub for x in ["rig up/down", "skid", "move", "waiting"]):
                    return "WAITING"
                return "EQUIPMENT_FAILURE"
            if domain == "formation evaluation":
                return "WIRELINE"
            if domain == "completion":
                # completion can be casing-ish or integrity tests; let override handle specifics
                return DOMAIN_MAP[domain]
            return DOMAIN_MAP[domain]

    # 2) Keyword fallback (activity + remark)
    blob = f"{a} {r}".strip()
    for pattern, etype in KEYWORD_RULES:
        if re.search(pattern, blob, flags=re.IGNORECASE):
            return etype

    return "UNKNOWN"


# -----------------------------
# JSONL IO
# -----------------------------

def read_jsonl(path: Path) -> list[Dict[str, Any]]:
    out: list[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def write_jsonl(path: Path, rows: list[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for obj in rows:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def apply_types(in_path: Path, out_path: Path) -> tuple[int, int]:
    rows = read_jsonl(in_path)
    changed = 0

    for ev in rows:
        activity_raw = ev.get("activity_raw") or ev.get("activity") or ""
        remark = ev.get("remark") or ""
        new_type = classify(str(activity_raw), str(remark))
        old_type = ev.get("event_type")

        ev["event_type"] = new_type
        if old_type != new_type:
            changed += 1

    write_jsonl(out_path, rows)
    return (len(rows), changed)


# -----------------------------
# CLI
# -----------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Add/overwrite event_type in a DDR events JSONL.")
    ap.add_argument("--in", dest="in_path", required=True, help="Input JSONL path")
    ap.add_argument("--out", dest="out_path", required=True, help="Output JSONL path")
    args = ap.parse_args()

    in_path = Path(args.in_path)
    out_path = Path(args.out_path)

    if not in_path.exists():
        raise FileNotFoundError(f"Input not found: {in_path}")

    n, changed = apply_types(in_path, out_path)
    print(f"Read: {n} events")
    print(f"Wrote: {out_path}")
    print(f"event_type changed/assigned: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
