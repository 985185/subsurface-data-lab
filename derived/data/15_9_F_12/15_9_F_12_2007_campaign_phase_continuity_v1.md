# 15/9/F/12 — 2007 Campaign Phase Continuity (v1)

Input: `/content/drive/MyDrive/LW_DTRE/derived/15_9_F_12/15_9_F_12_campaign_events_typed.jsonl`
Events: 1059
Days with classified activity: 96

## Phase blocks

| Block | Start | End | Days | Dominant phase |
|---:|---|---|---:|---|
| 1 | 2007-06-14 | 2007-06-14 | 1 | WAITING |
| 2 | 2007-06-15 | 2007-06-27 | 13 | DRILLING |
| 3 | 2007-06-28 | 2007-06-28 | 1 | EQUIPMENT_FAILURE |
| 4 | 2007-06-29 | 2007-07-23 | 25 | DRILLING |
| 5 | 2007-07-24 | 2007-07-25 | 2 | EQUIPMENT_FAILURE |
| 6 | 2007-07-26 | 2007-09-15 | 52 | DRILLING |
| 7 | 2007-10-12 | 2007-10-12 | 1 | WAITING |
| 8 | 2007-12-31 | 2007-12-31 | 1 | DRILLING |

## Notes

- Dominant phase per day is the most frequent `event_type` (excluding UNKNOWN/blank).
- Blocks collapse consecutive days with the same dominant phase.
