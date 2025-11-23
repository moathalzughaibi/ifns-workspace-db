# IFNS – UI Master (SoT) – Home Page Layout
This file proposes a concrete layout for your new Notion page:
**`IFNS – UI Master (SoT)`** – the single landing page for reviewers and future agents.
You can copy/paste the sections below into that Notion page and then wire the links to the actual pages/DBs.
## 1. Hero / Overview block
```markdown
# IFNS – UI Master (Source of Truth)
The **Intelligent Financial Nerve System (IFNS)** documentation lives here.
This page is the _single_ entry point for:
- The 14-step IFNS operational spine,
- All V2 spec cards (Indicators, Telemetry, Runtime, Manifests & Policy),
- Core databases (Feature Catalog, QCWeekly, CalendarGaps2025, …),
- Links to Git mirrors and runtime templates.
> Source of truth is **this Notion workspace** + linked databases. Git and runtime are mirrors.
```
## 2. Quick navigation (3-column layout)
In Notion, use a three-column layout. Example content:
```markdown
## Quick Navigation
**Column 1 – Start here**
- [Step 01 – Preface Integration](…)
- [Step 02 – Executive Summary](…)
- [Step 03 – Visionary–Technical Overview](…)
- [IFNS – Notion Page Index (historical)](…)
**Column 2 – Core specs (V2)**
- [Indicators – Core ML Build (V2)](…)
- [Manifests & Policy (V2)](…)
- [Telemetry & QC (V2)](…)
- [Runtime Templates & Calendars (V2)](…)
**Column 3 – Databases**
- [Feature Catalog](…)
- [QCWeekly](…)
- [CalendarGaps2025](…)
- [Universe / CatalogL1 / CatalogL2L3](…)
```
## 3. 14-step spine table
Add a table (or toggle list) summarizing each step with its main artifacts.
```markdown
## IFNS 14-Step Operational Spine
| Step | Name | Primary focus | Key links |
|------|------|--------------|-----------|
| 01 | Preface Integration | Context & framing | [Step 01 hub](…) |
| 02 | Executive Summary | High-level what/why | [Step 02 hub](…) |
| 03 | Visionary–Technical Overview | Big-picture architecture | [Step 03 hub](…) |
| 04 | Preface Timeline / Evolution | Timelines & phases | [Step 04 hub](…) |
| 05 | Foundations & Problem Definition | Problem framing | [Step 05 hub](…) |
| 06 | System Architecture | Layers & components | [Step 06 hub](…) |
| 07 | Data Intelligence Layer (DIL) | Data, features, labels | [Step 07 hub](…) |
| 08 | Modeling Intelligence (MI) | Models & training | [Step 08 hub](…) |
| 09 | Execution Intelligence (EI) | Orders, routing, slippage | [Step 09 hub](…) |
| 10 | Market Structural Awareness (MSA) | Market regimes & structure | [Step 10 hub](…) |
| 11 | Model & Signal Integration | Signal wiring into portfolios | [Step 11 hub](…) |
| 12 | Decision & Risk Architecture (DRA) | Risk, limits, guardrails | [Step 12 hub](…) |
| 13 | Self-Evaluation & Learning (SEL) | Feedback loops, post-mortems | [Step 13 hub](…) |
| 14 | Advanced Awareness & Future Extensions | Long-term extensions | [Step 14 hub](…) |
```
## 4. Databases & telemetry block
Create a section that lists the key Notion databases and how to read them.
```markdown
## Core Databases
**Feature Catalog**
- Purpose: Master list of indicators and frameworks (L1/L2/L3) with families, ML roles, and universe tiers.
- Views: By Level, By Family, By ML Role, Universe – Tiered.
**QCWeekly**
- Purpose: Weekly data quality / coverage snapshots.
- Views: By Week, By Horizon, Watchlist – Drift & Coverage, Holiday / Special Weeks.
**CalendarGaps2025**
- Purpose: Market holidays, early closes, and schedule gaps.
- Views: By Month, By Market, Risk-Sensitive Gaps.
```
## 5. Workflows & “How to use this space”
Add a section that explains how different personas navigate the SoT.
```markdown
## How to Use This Space
**If you are a reviewer (conceptual):**
- Start with: Step 02 – Executive Summary.
- Then: Step 03 – Visionary–Technical Overview.
- Finally: browse Steps 07–12 for deeper technical understanding.
**If you are a Notion/Git agent:**
- Use the 14-step table to find the right hub.
- Use the Core Databases section to know which DB to edit.
- Use the repo crosswalk (`Repo_Inventory_and_Git-Notion_Crosswalk...`) to sync with Git.
**If you are working on runtime / SxE:**
- Start with: Telemetry & QC (V2), Runtime Templates & Calendars (V2).
- Then: Step 09 – EI and Step 12 – DRA hubs.
```
## 6. Historical / archives section
Finally, add a compact section that links to V1 and drafts, clearly labeled.
```markdown
## Historical & Archives
These pages are **historical** – do not edit, but feel free to read for context:
- [IFNS – UI Master (V1)](…) – original 14-step write-up.
- [Drafts & Working Notes](…) – raw ideation and scratch work.
- [Core ML Build Stages (historical)](…) – earlier view of ML lifecycle.
> Status: Historical – all active work now lives in the 14-step hubs and V2 spec pages.
```
