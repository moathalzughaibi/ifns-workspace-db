# IFNS – SoT Handover & Notion Integration Guide

Version: v1.0
Date: 2025-11-19

This document is the **final handover** for the IFNS – UI Master (Source of Truth) work
completed in this cycle.

It has three main jobs:

1. Summarize what has been delivered (all split kits and core SoT helpers).
2. Explain the **integration plan** for the new Notion agent (step-by-step).
3. Describe optional **future improvements** so they can be implemented later without
   changing the current spine.


---

## 1. Delivered SoT assets

The following markdown files in the handover folder constitute the **SoT kit** for IFNS. They are meant to be imported into Notion as structured pages.

### 1.1 14-step spine – Narrative & Intent split kits

Each of these files defines a **parent** `01 – Narrative & Intent` page and its child pages
(sub-steps) for one of the 14 steps.

- `Step_01_Preface_Integration_Narrative_Split_Kit.md` – Step 01 (Preface Integration)
- `Step_02_Executive_Summary_Narrative_Split_Kit.md` – Step 02 (Executive Summary)
- `Step_03_Visionary_Technical_Narrative_Split_Kit.md` – Step 03 (Visionary Technical)
- `Step_04_Timeline_Narrative_Split_Kit.md` – Step 04 (Timeline)
- `Step_05_Operational_Genesis_Narrative_Split_Kit.md` – Step 05 (Operational Genesis)
- `Step_06_System_Architecture_Narrative_Split_Kit.md` – Step 06 (System Architecture)
- `Step_07_DIL_Narrative_Split_Kit.md` – Step 07 (DIL)
- `Step_08_MI_Narrative_Split_Kit.md` – Step 08 (MI)
- `Step_09_EI_Narrative_Split_Kit.md` – Step 09 (EI)
- `Step_10_MSA_Narrative_Split_Kit.md` – Step 10 (MSA)
- `Step_11_MSI_Narrative_Split_Kit.md` – Step 11 (MSI)
- `Step_12_DRA_Narrative_Split_Kit.md` – Step 12 (DRA)
- `Step_13_SEL_Narrative_Split_Kit.md` – Step 13 (SEL)
- `Step_14_Advanced_Awareness_Narrative_Split_Kit.md` – Step 14 (Advanced Awareness)

### 1.2 Core ML – Phase 6 runtime templates

- `Core_ML_Phase6_Runtime_Templates_Split_Kit.md`  
  Defines the parent and child pages for **Core ML – Phase 6 – Implementation & Runtime Templates**, including indicator engines, feature services, backfill/recalc, and monitoring/telemetry templates.

### 1.3 Telemetry & QC – QC Weekly spec

- `QC_Weekly_Telemetry_V1_Spec_Kit.md`  
  Converts `QC_Weekly_Telemetry_V1.md` from the repo into a Notion-ready **QC Weekly Telemetry V1** page, with meta, design goals, emit guidance, and relationships to other telemetry assets.

### 1.4 Global helpers for the SoT

- `IFNS_UI_Master_SoT_Reading_Guide_v0_1.md`  
  Reading guide explaining the overall structure (14-step spine, Indicator System, Telemetry, SxE), and giving tailored itineraries for Executives, ML/Eng, SxE/UX, and Ops/Risk.

- `IFNS_SoT_Hierarchy_and_Naming_Convention_v0_1.md`  
  Defines the naming rules for steps, sub-steps (NN.x), and cross-cutting hubs like Indicator System, Telemetry & QC, and Runtime Calendars.

- `IFNS_SoT_Missing_Assets_Report_v0_1.md`  
  Lists repo files (docs, schemas, data) that are **not explicitly referenced** in the SoT kits, grouped by category. This is the canonical list to decide what to import later vs. archive.

---

## 2. Notion integration plan (for the new agent)

This section is written **for the Notion/Git-enabled agent** who will take these files
and reflect them into the Notion workspace.

### 2.1 Create / confirm the SoT root

1. In Notion, create (or confirm) a root page named:

   > `IFNS – UI Master (SoT)`

2. At the top of this root, create a short intro and add **three prominent links**:

   - `IFNS – UI Master (SoT) – Reading Guide`
   - `IFNS – SoT – Hierarchy & Naming Convention`
   - `IFNS – SoT – Missing / Non-Referenced Assets Report`

3. Import the three markdown files and map them to those pages:

   - `IFNS_UI_Master_SoT_Reading_Guide_v0_1.md`
   - `IFNS_SoT_Hierarchy_and_Naming_Convention_v0_1.md`
   - `IFNS_SoT_Missing_Assets_Report_v0_1.md`

### 2.2 Rebuild the 14-step spine

For each of the 14 steps:

1. Create a **root page** at the top level under the SoT root:

   - `Step NN – <Step Name>`

2. Inside that root, create a child page:

   - `01 – Narrative & Intent`

3. Open the corresponding split kit markdown file, e.g.:

   - `Step_07_DIL_Narrative_Split_Kit.md`

4. From the kit:
   - Copy the content under **“A. Parent page – `01 – Narrative & Intent`”** into the `01 – Narrative & Intent` page.
   - For each **child page description** in section B (e.g. `07.1 – ...`), create a subpage under Step NN with the same title,
     and paste the corresponding ```markdown``` block into it.

5. Apply the naming rules from `IFNS_SoT_Hierarchy_and_Naming_Convention_v0_1.md`:

   - Child pages should be titled like `NN.x – <Short child title>`.
   - Keep the parent `01 – Narrative & Intent` pages **light** (overview + index only).

### 2.3 Import Core ML – Phase 6 runtime templates

1. Under the SoT root, create a hub page:

   - `Core ML – Indicator System (Phases)`

2. Inside that hub, create a child page for Phase 6:

   - `Phase 6 – Implementation & Runtime Templates`

3. Open `Core_ML_Phase6_Runtime_Templates_Split_Kit.md` and:

   - Paste the **parent** section into `Phase 6 – Implementation & Runtime Templates`.
   - Create child pages for each template section (runtime architecture, engine template, feature service template,
     backfill & recalculation, monitoring & telemetry, etc.) and paste the corresponding ```markdown``` blocks.

4. Near the top of the Phase 6 parent page, add a **Related Steps** note, for example:

   > Related Steps: Step 07 – DIL; Step 08 – MI; Step 10 – MSA; Step 11 – MSI; Step 12 – DRA; Step 13 – SEL.

### 2.4 Import QC Weekly Telemetry V1 spec

1. Under the Telemetry cluster (create if missing), make a hub page:

   - `Telemetry & QC (V2 hub)`

2. Under that hub, create a child page:

   - `QC Weekly Telemetry V1`

3. From `QC_Weekly_Telemetry_V1_Spec_Kit.md`, copy the ```markdown``` block into this page.

4. At the top of the page, add a **Related Steps** note:

   > Related Steps: Step 12 – DRA; Step 13 – SEL; Step 14 – AAQ.

5. Ensure there are links (references) to the JSON schema and NDJSON example mentioned in the spec. Those artifacts
   remain machine-readable sources; the Notion page is the human-readable SoT.

### 2.5 Align existing Notion pages

The existing Notion workspace already contains earlier versions of many pages. The goal is **not** to delete history,
but to align it with the new SoT.

For each area (Steps, Indicator System, Telemetry, Runtime Calendars):

1. **Do not overwrite blindly.** Instead:
   - Move legacy pages to an `Archive` section under the SoT root (or tag them clearly as `Legacy V1`).
   - Use the new SoT pages (built from these kits) as the primary reference going forward.

2. Where a legacy page contains unique content that is **not** represented in the SoT kits:
   - Either migrate that content into the appropriate sub-step page,
   - Or create a new child page and link it from the Reading Guide or the relevant hub.

3. Use `IFNS_SoT_Missing_Assets_Report_v0_1.md` as the official checklist to decide which repo assets
   to migrate into Notion and which to keep as Git-only history.

---

## 3. Plan for optional future improvements

The current SoT is **complete enough** for reviewers, critics, and engineers to work with.
However, the following enhancements can be implemented later if desired, without breaking the existing structure.

### 3.1 Telemetry & QC hub refinement

- Build a full split kit for the `Telemetry & QC (V2 hub)` page, similar to the steps and Phase 6 kit.
- Define child pages such as:
  - `TQ – 1. Telemetry Universe Overview`
  - `TQ – 2. QC Weekly Views`
  - `TQ – 3. Telemetry Schema & Examples`
  - `TQ – 4. CI Guards & Alerting`
  - `TQ – 5. Dashboards & SxE Surfaces`
- Cross-link these back to Steps 12, 13, and 14, and to any runtime/monitoring templates.

### 3.2 Runtime Templates & Calendars hub

- Create a split kit for `Runtime Templates & Calendars (V2 hub)`:
  - Parent: overview of runtime schedules and lanes.
  - Children: daily/weekly/monthly calendars, example runbooks, promotion/rollback checklists.
- Cross-link with Step 04 (Timeline), Step 06 (Architecture – Environments & Deployment Lanes),
  and Phase 6 runtime templates.

### 3.3 Indicator System – Phases 1–5

- For each earlier phase (1–5), create a split kit similar to Phase 6, with:
  - Parent: purpose, scope, relationship to steps.
  - Children: data sources, taxonomy tables, evaluation criteria, QC hooks.
- Make sure each phase has a **Related Steps** note referencing the relevant spine steps
  (typically 07–11, and 12–13 for evaluation and learning).

### 3.4 SxE-specific summaries

- Optionally, build a small SxE hub that aggregates all `SxE Representation...` and
  `Integration Points` sections from the various steps into one design-oriented view.
- This would be useful when handing off to a dedicated UX team, but is not required for
  the current SoT completeness.

---

## 4. Final notes

- The work completed in this cycle is **intentionally conservative**: it restructures and clarifies
  existing content rather than inventing new concepts.
- The 14-step spine is now readable as a set of steps and sub-steps; Core ML Phase 6 and QC Weekly
  have clear homes; and the Reading Guide + Naming Convention + Missing Assets report provide the
  necessary meta-structure.

For the new agent:

- Treat these markdown files as the **authoritative SoT kit** for building the new Notion root.
- Use the hierarchy and naming convention as your style guide.
- Use the missing-assets report as your migration checklist.
- Avoid deleting history; instead, make the new SoT pages the primary view, and keep older material
  either archived or clearly labeled as legacy.

Once the Notion workspace has been rebuilt following this guide, IFNS – UI Master (SoT) should be ready
for deep review, criticism, and eventual SxE/UX handoff without structural confusion.
