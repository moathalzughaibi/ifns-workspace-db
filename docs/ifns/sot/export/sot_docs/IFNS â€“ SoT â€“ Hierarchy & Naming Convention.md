# IFNS SoT – Hierarchy & Naming Convention (v0.1)
This document defines how to name and organize pages in the **IFNS – UI Master (SoT)** workspace,
so that the 14-step spine, sub-steps, and cross-cutting clusters remain consistent and readable.
## 1. Core principles
1. The **14 steps** form the primary spine (Step 01 … Step 14).
2. Each step has:
   - One light **parent page**: `01 – Narrative & Intent`.
   - Several **child pages**, which are treated as *sub-steps* of that step.
3. Cross-cutting clusters (Indicator System, Telemetry & QC, Runtime Calendars) live in their own hubs,
   but must declare which steps they relate to.
## 2. Naming for 14-step pages and sub-steps
For each step `NN` (01–14):
- **Root page title:**
  - `Step NN – <Step Name>`
- **Parent narrative page:**
  - `Step NN – <Step Name> / 01 – Narrative & Intent`
- **Child pages (sub-steps):**
  - `NN.1 – <Short child title>`
  - `NN.2 – <Short child title>`
  - `NN.3 – <Short child title>`
  - …
Examples:
- `Step 07 – DIL / 01 – Narrative & Intent`
  - `07.1 – DIL Role & Scope`
  - `07.2 – Data Domains & Coverage`
  - `07.3 – Canonical Price Model`
  - `07.4 – Indicator Families & Frameworks`
- `Step 10 – MSA / 01 – Narrative & Intent`
  - `10.1 – MSA – Role in the IFNS Stack`
  - `10.2 – MSA – Structural Ontology`
  - `10.3 – MSA – STRUCTURE_MTF and Derived Feature Frameworks`
  - …
## 3. Cross-cutting clusters (Indicator System, Telemetry, Calendars)
Some assets cut across multiple steps and should **not** be forced under a single step.
These live in dedicated hubs and declare their relationships explicitly.
### 3.1 Indicator System
- Hub page: `Stock Indicator System – Master Index V2`.
- Phase pages: `Phase N – <Phase Name>`.
- For each phase, add a short **Related Steps** section near the top, e.g.:
  - `Related Steps: Step 07 – DIL; Step 08 – MI; Step 10 – MSA; Step 11 – MSI; Step 12 – DRA; Step 13 – SEL`.
### 3.2 Telemetry & QC
- Hub page: `Telemetry & QC (V2 hub)`.
- Example child: `QC Weekly Telemetry V1`.
- Each telemetry spec should include a **Related Steps** note, e.g. for QC Weekly:
  - `Related Steps: Step 12 – DRA; Step 13 – SEL; Step 14 – AAQ`.
### 3.3 Runtime Templates & Calendars
- Hub page: `Runtime Templates & Calendars (V2 hub)`.
- Children for daily/weekly/monthly calendars and runtime templates.
- Related Steps: Step 04 (Timeline), Step 06 (System Architecture), and any relevant ML phases.
## 4. Editing rules
1. **Do not expand parent narrative pages** back into long documents. Keep them short and index-like.
2. When adding new detail, create or extend **child pages (sub-steps)** under the relevant step.
3. When introducing a new cross-cutting spec (e.g., a new telemetry view), place it in the appropriate hub
   and add a `Related Steps` line.
4. When migrating content from Git-only docs, always:
   - Create a human-readable SoT page in Notion (following the naming above).
   - Reference the Git artifacts (CSV/JSON/YAML) as machine-readable companions.
