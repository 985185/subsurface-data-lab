#!/usr/bin/env python3
"""
apply_event_type.py

Reads a DDR day events JSONL file, applies rule-based classification to each row,
and writes a new JSONL with event_type populated.

Usage:
  python tools/apply_event_type.py --input examples/in.jsonl --output examples/out.jsonl
"""

import argparse
import json
from pathlib import Path

from classify_event import classify_event


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Path to input .jsonl file")
    p.add_argument("--output", required=True, help="Path to output .jsonl file")
    args = p.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    n = 0
    with in_path.open("r", encoding="utf-8") as fin, out_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue

            obj = json.loads(line)

            activity = obj.get("activity_raw", "")
            remark = obj.get("remark", "")

            obj["event_type"] = classify_event(activity, remark)

            fout.write(json.dumps(obj, ensure_ascii=False) + "\n")
            n += 1

    print(f"Classified {n} events -> {out_path}")


if __name__ == "__main__":
    main()
