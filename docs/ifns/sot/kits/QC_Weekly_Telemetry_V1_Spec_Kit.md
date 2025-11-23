# QC Weekly Telemetry V1 – Spec Kit

This file restructures the existing `QC_Weekly_Telemetry_V1.md` asset into a Notion-friendly layout.

Content is taken from the current markdown and organized into clear sections; no new

metrics or fields are invented here.


## A. Parent page – `QC Weekly Telemetry V1`

In Notion, create or update a page named **`QC Weekly Telemetry V1`** and use the body below.

```markdown
# QC Weekly Telemetry V1

Narrative spec for the **weekly QC telemetry** view of IFNS.


## Meta

- **Role:** Weekly QC telemetry schema and emit guidance.
- **Original file name:** `QC_Weekly_Telemetry_V1.md`
- **Original repo path:** `docs/ifns/indicators/QC_Weekly_Telemetry_V1.md`
- **Schema artifact:** `sync/ifns/qc_weekly_schema_v1.json`
- **Example artifact:** `sync/ifns/qc_weekly_example_v1.ndjson`

> In the SoT, treat **this page** as the human-readable source of truth for QC Weekly.

> The JSON/NDJSON artifacts remain the machine-readable counterparts.


## Design goals

- One event per **view per week**.
- Includes both overall metrics and `family_breakdown[]` for at-a-glance rollups.
- `manifest_sha256` pins the exact feature set used that week.

## Emit guidance

- Write NDJSON lines to a dated file (e.g., `qc_weekly_2025-11-28.ndjson`).
- Use the per-feature **policy thresholds** from the training matrix to compute coverage/drift/clipping,
  then aggregate those results up to the **family** level for `family_breakdown[]`.

## Relationship to other telemetry

- Weekly QC is a **rollup view** on top of lower-level telemetry (per-run, per-model, per-indicator).
- It is designed for:

  - Ops & Risk: to see where coverage or drift is degrading.

  - ML & DIL owners: to spot families that need retraining or feature repair.

- The JSON schema (`qc_weekly_schema_v1.json`) should be mirrored in the Telemetry Schema tab,

  and the example NDJSON (`qc_weekly_example_v1.ndjson`) should be mirrored in a Telemetry Examples tab.

```
