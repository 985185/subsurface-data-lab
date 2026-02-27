# Subsurface Data Lab
Part of the Subsurface Data Lab:
https://github.com/<yourusername>/subsurface-data-lab
An open research environment for reconstructing, analysing, and querying operational history of oil & gas and CO₂ storage wells from real field data.
## What is Subsurface Data Lab?

Subsurface Data Lab is a collection of open workflows, datasets, and tools designed to turn raw petroleum field data into structured, queryable engineering knowledge.

Real wells generate large volumes of operational records: drilling reports, logging files, well logs, completion data, and test results. Most of this information exists only as documents intended for human reading, not machine analysis.

This project converts those records into structured data that can be searched, analysed, and reused for engineering, regulatory, and research purposes.
## Why this project exists

Daily drilling reports, logs, and operational documents contain critical information about:

• well construction
• operational problems
• well integrity indicators
• non-productive time (NPT)
• cementing and casing history
• pressure behaviour

However, these records are typically stored as PDFs, HTML reports, or proprietary formats and cannot be queried across wells.

This repository provides a reproducible method to reconstruct the operational history of wells and make the information usable for:

- decommissioning assessment
- well integrity review
- CCS storage analysis
- regulatory evaluation
- research and education
## Data Source

Initial development uses the publicly available Volve Field dataset released by Equinor.  
The Volve dataset is one of the few complete field data releases and provides a realistic test environment for developing reproducible subsurface data workflows.****
## What this repository contains

This is the master entry point for all Subsurface Data Lab projects.

Each linked repository performs a specific function:

| Repository | Purpose |
|-----------|------|
| volve-metadata-index | Indexes and catalogues all files in the Volve dataset |
| well-knowledge-graph | Organises files by well and creates structured well manifests |
| manifest-tools | Generates per-well structured outputs |
| (future) digital-twin-engine | Reconstructs chronological operational timelines from drilling reports |

## Core Concept

The project follows a simple progression:

Raw files → indexed data → structured well records → reconstructed well history

The long-term objective is to allow an engineer or regulator to answer questions such as:

- What actually happened in this well?
- When did problems occur?
- How was the well constructed?
- What risks exist for abandonment or CO₂ storage?

Instead of manually reading hundreds of reports, the system reconstructs a chronological operational history.
## Project Status

Active research project.

The system is under continuous development and prioritises transparency and reproducibility over optimisation.
## Long Term Vision

To create an open, reproducible framework for transforming legacy well data into structured knowledge that supports:

- safer well abandonment
- improved regulatory oversight
- CO₂ storage verification
- historical well understanding

The goal is not to build a commercial platform, but to make complex subsurface operational history understandable and reusable.
