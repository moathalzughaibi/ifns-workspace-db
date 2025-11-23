# IFNS – UI Master (SoT) – Reading Guide
Version: v0.1
Date: 2025-11-19

> This guide explains **how to read** the IFNS – UI Master (Source of Truth) workspace in Notion
> and how the different documents relate to each other. It does **not** introduce new concepts;
> it simply stitches together work that already exists in the 14-step spine and the V2 specs.

---

## 1. Purpose of this guide

The IFNS documentation is intentionally rich and multi-layered. Without a map, it can feel like
separate projects. This guide has three jobs:

1. Show how the **14-step spine** hangs together as one narrative.
2. Show where the **ML indicator system, runtime templates, and telemetry** plug into that spine.
3. Give tailored **reading itineraries** for different audiences (Executive, ML/Eng, SxE/UX, Ops/Risk).

You can think of this guide as the **Table of Contents with context** for the IFNS SoT.

---

## 2. High-level structure of IFNS – UI Master (SoT)

At a high level, the IFNS SoT is organized into four major clusters:

1. **14-Step Operational Spine (Legacy Master, now decomposed)**
2. **Core ML Indicator System (Phases 1–6, plus future phases)**
3. **Telemetry, QC, and Runtime Calendars (V2 assets)**
4. **SxE (System-to-Experience) and Advanced Awareness**

Each cluster is represented in Notion by one or more *root pages*, which have now been refactored
into a light **parent page** plus several **child pages** (split kits).

### 2.1 14-Step Operational Spine

These steps describe IFNS from first preface through advanced awareness. In the SoT, each step has:

- One parent page: `01 – Narrative & Intent` (short overview, intent, and child index).
- Several child pages: each capturing one major heading from the original long document.

The steps (all now split) are:

1. **Step 01 – Preface Integration**
2. **Step 02 – Executive Summary**
3. **Step 03 – Visionary–Technical Overview (SxE)**
4. **Step 04 – Preface Timeline**
5. **Step 05 – Operational Genesis Framework (OGF)**
6. **Step 06 – System Architecture**
7. **Step 07 – DIL (Data & Indicator Layer)**
8. **Step 08 – MI (Model Intelligence)**
9. **Step 09 – EI (Execution Intelligence)**
10. **Step 10 – MSA (Market Structural Awareness)**
11. **Step 11 – MSI (Model & Signal Integration)**
12. **Step 12 – DRA (Dynamic Risk & Allocation)**
13. **Step 13 – SEL (Systemic Experience & Learning)**
14. **Step 14 – Advanced Awareness & Quantum Cognition (AAQ)**

Each of these has a corresponding split-kit markdown file (for example:
`Step_05_Operational_Genesis_Narrative_Split_Kit.md`) which defines the parent and its children.

### 2.2 Core ML Indicator System

This cluster describes how the **indicator and feature system** is structured, evaluated, and deployed.
In the SoT, it is represented by:

- `Stock Indicator System – Master Index V2` (hub)
- Phase documents (`Phase 1` … `Phase 6` … future)

So far, the following phase has a split kit:

- **Phase 6 – Implementation & Runtime Templates**
  → `Core_ML_Phase6_Runtime_Templates_Split_Kit.md`
  This defines how indicator engines, feature services, backfill, and monitoring are standardized.

Other phases will follow the same pattern over time (Phase 1–5, and any higher phases).

### 2.3 Telemetry, QC, and Runtime Calendars

This cluster defines **how we watch IFNS itself**:

- `Telemetry & QC (V2 hub)` – overall telemetry/QC universe
- `QC Weekly Telemetry V1` – the weekly QC view
- Telemetry schemas, examples, IO utilities, and CI guard workflows
- `Runtime Templates & Calendars (V2 hub)` – calendars, gaps, and runtime templates

These are currently partially structured; future work will introduce:

- `QC_Weekly_Telemetry_V1` split kit
- Telemetry & QC SoT parent + children
- Runtime Calendars split kit and cross-links to Step 04 & Step 06.

### 2.4 SxE and Advanced Awareness

Two areas concentrate the SxE (System-to-Experience) and “mirror” philosophy:

- **Step 03 – Visionary–Technical Overview**
  → Defines SxE as a first-class layer and introduces Mirror, Admin, Harness/Telemetry surfaces.

- **Step 14 – Advanced Awareness & Quantum Cognition**
  → Defines deeper awareness, scenario reasoning, narrative intelligence, and meta-metrics.

Many other steps include SxE subsections (e.g. `SxE Representation of MSA`, `SxE Representation of MSI`,
`SxE Integration Points` in the architecture). These should be treated as **feeds** into the SxE design,
with Step 03 and Step 14 acting as the primary SxE lenses.

---

## 3. Reader profiles and recommended itineraries

This section gives **practical reading paths** depending on who is reviewing the system.

### 3.1 Executive / Decision-Maker

Focus: understanding *what* IFNS is, *why* it exists, and *how* it is governed.

**Suggested itinerary:**

1. **Step 02 – Executive Summary**
   - Parent page `01 – Narrative & Intent`
   - Child pages:
     - `Exec – 1. What this step does`
     - `Exec – 2. Audience`
     - `Exec – 3. Key bullets that must always appear`
     - `Exec – 4. Summary structure`

2. **Step 01 – Preface Integration**
   - Especially: key messages and success criteria for Step 01.

3. **Step 05 – Operational Genesis Framework**
   - `OGF – 1. IFNS as an Operational System, Not a Toolkit`
   - `OGF – 2. Core Intelligence Layers`
   - `OGF – 5. Scope and Boundaries`

4. **Step 03 – Visionary–Technical Overview**
   - `SxE – 1. System-to-Experience as a First-Class Layer`
   - `SxE – 2. Mirror – Awareness as a Primary Product`

5. **Step 04 – Preface Timeline**
   - Read the parent, then scan Phase 0–5 to understand the rollout path.

6. Optionally, **Step 14 – Advanced Awareness & Quantum Cognition**
   - For long-term vision of how IFNS might evolve in higher awareness.

This path gives an executive a *story* of IFNS as a living system, without diving into ML or runtime details.

### 3.2 ML / Engineering (Models, Features, Runtime)

Focus: indicators, features, model integration, and runtime architecture.

**Suggested itinerary:**

1. **Step 07 – DIL (Data & Indicator Layer)**
   - All child pages (role, data domains, canonical price model, indicator frameworks…)

2. **Step 08 – MI (Model Intelligence)**
   - How signals are formed, evaluated, and surfaced.

3. **Step 10 – MSA (Market Structural Awareness)**
   - `MSA – 2. Structural Ontology`
   - `MSA – 3. STRUCTURE_MTF and Derived Feature Frameworks`

4. **Step 11 – MSI (Model & Signal Integration)**
   - Integration patterns, contracts, policy-driven logic.

5. **Core ML – Phase 6 – Implementation & Runtime Templates**
   - Parent page + 8 child pages, especially:
     - Runtime architecture
     - Indicator engine template
     - Feature service template
     - Backfill & recalculation
     - Monitoring & telemetry templates

6. Telemetry & QC (once SoT kits are in place)
   - QC Weekly Telemetry view
   - Telemetry schema & examples
   - CI guards and runtime monitoring

7. **Step 06 – System Architecture**
   - `Arch – 2. Core Components and Their Responsibilities`
   - `Arch – 3. Environments and Deployment Lanes`
   - `Arch – 4. Data and Decision Flow`

This path answers: *What do we build? How do we run it? How is it monitored?*

### 3.3 SxE / Product / UX (Mirror & Admin)

Focus: turning system roles into interfaces and experiences.

**Suggested itinerary:**

1. **Step 03 – Visionary–Technical Overview**
   - Entire set of `SxE –` child pages.

2. **Step 14 – Advanced Awareness & Quantum Cognition**
   - `AAQ – 1. Layers of Awareness`
   - `AAQ – 2. Quantum Cognition`
   - `AAQ – 3. Narrative Intelligence & Reasoning Reports`
   - `AAQ – 5. SxE Representation of Advanced Awareness`

3. From the spine, collect all SxE-related child pages:
   - `SxE Representation of MSA` (Step 10)
   - `SxE Representation of MSI` (Step 11)
   - `SxE Integration Points` (Step 06)
   - Any “Mirror/Admin” mentions in DRA/SEL.

4. Telemetry & QC views:
   - QC Weekly Telemetry SxE (how QC is presented)
   - Telemetry dashboards and meta-metrics (once structured).

This path builds a **SxE requirements pack** that can be turned into wireframes and UI specs.

### 3.4 Ops / Risk / Governance

Focus: safety, limits, evaluation, and governance loops.

**Suggested itinerary:**

1. **Step 12 – DRA (Dynamic Risk & Allocation)**
   - All child pages, especially risk envelopes, allocation rules, and limit-setting.

2. **Step 13 – SEL (Systemic Experience & Learning)**
   - How the system learns from outcomes and feeds back into policies and models.

3. **MSA & MSI**
   - Structural constraints for risk and execution (MSA – 5)
   - Relationship to SEL and DRA (MSI – 5)

4. Telemetry & QC cluster:
   - QC Weekly Telemetry V1
   - Telemetry schema and example payloads
   - CI guard workflows and escalation logic.

5. **Step 04 – Preface Timeline**
   - To understand how risk posture changes across rollout phases (paper, canary, live).

6. Optionally, **Step 14 – Deep Telemetry & Meta-Metrics**
   - For higher-order meta-metrics around IFNS behaviour over time.

This path aligns operational risk, QC, and learning with the rest of the system.

---

## 4. Cross-references between key documents

To avoid treating documents as islands, keep these links in mind:

- **Step 05 (OGF)** ⇄ **Step 06 (Architecture)**
  - OGF explains *what roles exist*; Architecture explains *how those roles are realized*.

- **DIL / MI / MSA / MSI** ⇄ **Indicator System Phases 1–6**
  - Steps 07–11 describe roles and concepts; the Indicator System Phases describe concrete indicator/feature
    bundles and runtimes.

- **DRA / SEL** ⇄ **Telemetry & QC**
  - Risk and learning outcomes should always be mirrored in telemetry and QC views.

- **Step 03 & Step 14** ⇄ **All SxE sections**
  - These two steps define the global SxE philosophy; other steps’ SxE subsections inherit from here.

As more split kits are added (Telemetry/QC, Runtime Calendars, other ML phases), this section can be
expanded with explicit Notion links.

---

## 5. Maintenance notes for editors

When editing or extending the SoT:

1. **Do not re-expand parent pages.**
   - Parents (`01 – Narrative & Intent`) should stay short: intent + child index.

2. **Add new detail in child pages or new children.**
   - If a topic starts to grow too large inside a child page, consider splitting into one more level of children.

3. **Keep cross-references explicit.**
   - When a page depends on a concept defined elsewhere, mention the step/phase by name (e.g., “See Step 10 – MSA – 2. Structural Ontology”).

4. **Avoid “Git-only” references without a SoT mirror.**
   - If a page points to a CSV/JSON/YAML file in Git as source of truth, create a thin SoT representation
     (schema, index, or summary) in Notion and link back to Git, instead of leaving readers with a dead end.

5. **Update this Reading Guide when major structures change.**
   - When you add a new major cluster, phase, or hub, add a short description and recommended itinerary here.

This guide is meant to be a **living map**. Each time the structure of IFNS evolves, this is one of the first
places that should be updated.
