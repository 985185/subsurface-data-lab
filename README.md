# Legacy Well Digital Twin Reconstruction Engine (LW-DTRE)

LW-DTRE deterministically reconstructs drilling campaign timelines from
Volve Daily Drilling Reports (DDR).

The engine converts raw DDR HTML files into structured campaign-scale
operational timelines using rule-based extraction and classification.

This project is designed for:

-   Academic validation
-   SPE-grade research
-   Regulatory analysis
-   Open reproducible subsurface studies

------------------------------------------------------------------------

## What This Engine Does

Given a folder of DDR HTML files, LW-DTRE performs:

1.  Deterministic extraction of operations table rows
2.  Conversion to structured daily JSONL events
3.  Campaign-level merging
4.  Deterministic event classification
5.  Dominant daily phase detection
6.  Cross-day phase continuity segmentation

The system produces campaign-scale structured datasets suitable for:

-   Timeline reconstruction
-   Operational phase analysis
-   Injectivity and integrity correlation
-   Well lifecycle modeling

------------------------------------------------------------------------

## Repository Structure

tools/ Extraction and classification scripts\
schema/ Event schema definitions\
data/derived/ Reconstructed campaign artifacts\
analysis/ Experimental notebooks and investigations\
docs/ Design notes and validation documents

Canonical reconstruction outputs live under:

data/derived/`<WELL>`{=html}/

------------------------------------------------------------------------

## Validated Campaigns (v1.1)

  Well        Year   Days   Events   Phase Blocks
  ----------- ------ ------ -------- --------------
  15/9-F-4    2008   69     886      23
  15/9-F-12   2007   96     1059     8
  15/9-F-10   2009   71     1075     7

Total events processed: \>3000

------------------------------------------------------------------------

## Design Philosophy

-   Fully deterministic
-   No AI required for baseline reconstruction
-   Minimal dependencies
-   Reproducible
-   Campaign-scale continuity aware
-   Transparent rule-based classification

------------------------------------------------------------------------

## Current Limitations

-   Event taxonomy coarse (drilling dominant)
-   Cementing / casing detection incomplete
-   No quantitative classifier benchmarking yet
-   No depth correlation integration yet

------------------------------------------------------------------------

## Next Development Phase

-   Expand event classification taxonomy
-   Improve cementing and casing detection
-   Introduce deterministic tripping logic
-   Add validation metrics
-   Integrate depth/time integrity checks
-   Prepare SPE-ready campaign case study

------------------------------------------------------------------------

## Status

v1.1 marks transition from prototype validation to multi-well
campaign-scale reconstruction.

The engine is stable and reproducible.

Taxonomy refinement is the next major milestone.
