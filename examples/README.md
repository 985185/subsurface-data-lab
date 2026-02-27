# Examples — DDR Day Event Outputs

This directory contains example outputs generated from Daily Drilling Report (DDR) HTML files.

Each file represents one report day converted into structured machine-readable events.

## File Format

All files use JSON Lines (JSONL) format:

- One JSON object per line
- Each line represents one operational time block from the DDR "Operations" table
- No surrounding array brackets

Example (single event):

{
  "wellbore": "15/9-19 A",
  "date": "1997-10-10",
  "start_time": "00:00",
  "end_time": "02:00",
  "activity_raw": "workover -- wire line",
  "state": "ok",
  "remark": "LOGGED FROM 3556 M TO 2592 M.",
  "end_depth_md": "3937"
}

## What This Represents

Each event corresponds directly to one row in the DDR Operations table.

The fields preserve:

- chronological structure (start/end time)
- original activity classification
- operational state
- engineer-written narrative remarks

No interpretation or classification is applied in the raw example files.

## Purpose of These Examples

These example files serve as:

- validation artifacts for schema compliance
- demonstration of reproducible extraction
- ground truth samples for future event classification
- baseline inputs for well-level timeline reconstruction

## Important Notes

- These files are generated from HTML DDR reports.
- No AI or NLP is used at this stage.
- The extraction process is deterministic and reproducible.

Future versions of the pipeline will enrich these events with:

- normalized event types
- derived metrics
- cross-day stitching into full well timelines
