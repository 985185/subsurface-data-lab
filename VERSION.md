# Legacy Well Digital Twin Reconstruction Engine

## Version Freeze — v1.0

Frozen: F-15 A (Dec 2008 window)

Scope:
- HTML DDR parsing
- JSONL structured events
- Rule-based event classification
- Time validation (24h, gap/overlap detection)
- Consecutive phase block segmentation
- Cross-day dominant phase continuity
- Hierarchical phase selection (PRIMARY vs SUPPORT)
- Incident flag detection (WELL_CONTROL, EQUIPMENT_FAILURE)

Data window:
2008-12-13 → 2008-12-23 (11 validated days)

Notes:
2008-12-12 excluded (incomplete stub DDR).

This version establishes deterministic reconstruction
without any LLM dependency.
