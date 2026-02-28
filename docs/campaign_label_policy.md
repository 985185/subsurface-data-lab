# Campaign Label Policy (Deterministic)

## Daily labels
Each DDR day is classified into:
- A PRIMARY dominant phase (e.g., DRILLING, CASING, CEMENTING, PERFORATION, DST, TESTING, SLOT_MOVE), or
- SUPPORT-only (no PRIMARY dominance)

## SUPPORT-only days
A day is SUPPORT-only when PRIMARY dominance cannot be established (e.g., only TRIP / MUD_CONDITIONING / WAITING / OTHER / overlays).

SUPPORT-only days:
- are retained for completeness
- do not create phase transitions
- do not form campaign-level phase blocks
- may be attached as annotations to adjacent blocks for reporting

## Overlays
These are recorded but never dominant:
- WELL_CONTROL
- EQUIPMENT_FAILURE
- INTEGRITY_TEST
