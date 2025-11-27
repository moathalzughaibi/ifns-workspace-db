# IFNS – Ops Phase 1 – Microcopy & UI Polish Notes (v1)

Scope: Small, **non‑structural** improvements you can make directly in Notion.
Goal: Make the Ops area feel “SxE‑finished” without touching schemas or scripts.

> All of these are optional. None of them are required for correctness.

---

## 1. Workspace hub – “Workspace (DB) IFNS (Hub)”

**Page:** `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub)`

### 1.1 Page title and icon

- Keep title: `Workspace (DB) IFNS (Hub)` (already consistent with packs).
- Suggested icon: a simple 📚 or 🧩 (library / modules).

### 1.2 Top‑of‑page description

At the very top of the hub, add a short description block such as:

> **What this hub is**
> This hub is the operational entry point for IFNS. It holds the core workspace databases (Projects, Tasks, Decisions, Approvals, Handover) and the navigation links to their specs and microhubs.

> **How to use it**
> Start here when you want to *organise work* on IFNS (projects, approvals, decisions) rather than edit ML logic. From here you can jump to the registry, Ops DBs, and SxE specs.

This aligns with the microhub text and gives SxE a stable “elevator pitch” for the page.

### 1.3 Grouping links into sections

In the hub page, group links into small headings, for example:

- `## Core Ops DBs`
  - Projects
  - Tasks
  - Decisions
  - Approvals
  - Handover

- `## Workspace standards & registry`
  - IFNS_Workspace_Standards_V2
  - IFNS – Workspace Registry (V2)

- `## Index & navigation`
  - IFNS_Workspace_DB – Index (DB)
  - Index microhub(s)

This makes the page less like a flat link dump and more like a structured “home screen”.

---

## 2. Ops DBs – front‑page descriptions

For each Ops DB, add a 1–2 line description at the top of the Notion DB page (above the table).

### 2.1 Projects

Suggested text:

> **Purpose**: Track IFNS‑level projects (epics, streams, major milestones) with owners, status, and links to tasks/decisions.
> **Use**: Every non‑trivial initiative gets a row here; Tasks roll up into Projects where relevant.

### 2.2 Tasks

Suggested text:

> **Purpose**: Capture concrete, actionable work items related to IFNS (including SxE, Ops, and ML tasks).
> **Use**: Prefer Tasks for day‑to‑day work; relate them to Projects, Decisions, and Approvals when needed.

### 2.3 Decisions

Suggested text:

> **Purpose**: Record decisions that change how IFNS behaves (architecture, scope, risk posture, ops processes).
> **Use**: Each row is one decision with a clear “Decision” field, date, and owner. Link to affected Projects and specs.

### 2.4 Approvals

Suggested text:

> **Purpose**: Track formal approvals / sign‑offs (e.g. “SxE approved for Ops Phase 1”, “Risk signed off on a new indicator set”).
> **Use**: When a decision or spec needs a named approver, create an approval row and link it back to that asset.

### 2.5 Handover

Suggested text:

> **Purpose**: Capture handover events (e.g. between agents, teams, or phases) with dates, scope, and links to underlying work.
> **Use**: Before someone steps off IFNS, create a handover row and attach the relevant projects/tasks/specs.

---

## 3. Index DB views & microhubs

### 3.1 Index DB (Workspace_DB – Index (DB))

On the Index DB page, define a couple of standard views:

1. **Ops – Workspace assets**
   - Filter by Scope / Type_v2 / Owner_Role to show Ops/Workspace assets.
   - Group by `Type_v2` (DB, Hub, Spec).

2. **Quant/ML assets**
   - Filter to Quant/ML scope.
   - Group by family (Indicator System, Telemetry, Feature Views, etc.).

3. **SxE review queue**
   - Filter where `Work_Status` is not `Done` and Scope is in [Ops, Quant/ML].

These views align with how SxE will navigate during reviews.

### 3.2 Microhub content tone

Where Task C has appended microhub text, you can lightly tune wording:

- Make headings consistent:
  - `## Overview`
  - `## How to use this index`
  - `## Linked assets (from Registry)`
- For scanning, consider converting bullets like:
  - “Start here when you need to understand this slice of IFNS…”
  Into more direct forms:
  - “**Use this page when:** you need to understand this slice of IFNS or find its key assets quickly.”

This is optional polish; the structure is already correct.

---

## 4. Step 01 – “00 Related operations”

**Location:** `SoT Steps` → `Step 01 Preface` → `00 Related operations`.

From automation, this page now holds ~28 blocks from `SoT_Step01_00_Related_Operations_new.md`.

### 4.1 Framing block at the top

Add a short framing block above the long content, e.g.:

> **What this page is**
> This page lists the operations and assets that Step 01 depends on (or impacts), so SxE can see the blast radius before approving changes.

> **How to use it**
> Skim this page before editing Step 01 specs. If you change something here, consider which projects, DBs, or specs must be updated or re‑reviewed.

### 4.2 Optional sub‑headings

If the long narrative feels dense, add a few H2s (without changing the underlying paragraphs):

- `## Direct Step 01 dependencies`
- `## Downstream assets affected by Step 01`
- `## Ops touchpoints (Projects/Tasks/Approvals)`

You can do this directly in Notion by inserting headings around the paragraphs, without needing to touch the source MD or scripts.

---

## 5. Short spec intros (sampling guidance)

The 22 short specs now have intros. To make them feel consistent:

1. Pick 3–5 short specs that SxE cares about most.
2. For each intro:
   - Keep it to **2–3 sentences max**.
   - First sentence: **what this spec is**.
   - Second sentence: **when to use it**.
   - Optional third: **what not to do here** (if important).

If you find one intro too long or too vague, tighten it directly in Notion. The automation has already done the “attach the intro” step; microcopy can be edited safely by hand.

---

## 6. Registry / status alignment

Finally, ensure the Workspace Registry reflects reality:

- For the 6 Ops DBs, set `Work_Status` (or equivalent) to `Done`.
- For microhubs and Step 01, if they feel SxE‑ready after your review, mark them as `Done` as well.

This keeps the registry as the ground truth of “what is live and ready” without changing any schemas or scripts.
