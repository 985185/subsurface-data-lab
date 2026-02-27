# Event Type Vocabulary (v0.1)

This document defines the controlled vocabulary for normalized DDR event classification.

## Core Event Types

- DRILLING
- TRIP
- WIRELINE
- DST
- CASING
- CEMENTING
- MUD_CONDITIONING
- TESTING
- RIG_UP_DOWN
- WAITING
- EQUIPMENT_FAILURE
- WELL_CONTROL
- PERFORATION
- OTHER

## Design Principles

- One primary event_type per DDR operation row.
- Derived from activity_raw and/or remark.
- Rule-based (deterministic).
- Extendable but controlled.
