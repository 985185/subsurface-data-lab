# Getting Started

This project is organised as a workflow.  
Follow the steps in order.

You do NOT need to understand the entire system before starting.

---

## Step 1 — Index the dataset
Repository: volve-metadata-index

Purpose:
Create a complete inventory of all files in the Volve dataset.

Output:
A CSV catalogue of all field data files.

Why:
Before analysing wells, we must know what data exists.

---

## Step 2 — Organise by well
Repository: well-knowledge-graph

Purpose:
Associate each file with a specific well and build well-level manifests.

Output:
Per-well structured file manifests.

Why:
Engineering questions are asked per well, not per file.

---

## Step 3 — Generate structured outputs
Repository: manifest-tools (or your actual name)

Purpose:
Create standardised well folders and structured outputs.

Output:
Well folders containing organised data and machine-readable manifests.

Why:
Allows consistent processing across all wells.

---

## Step 4 — Reconstruct well history (in development)
Repository: Digital Twin Engine (future)

Purpose:
Extract operational events from drilling reports and rebuild chronological well history.

Output:
Timeline of drilling, casing, cementing, and operational events.

Why:
Allows engineers and regulators to understand what actually happened in the well.
