# IFNS – Ops Phase 1 (Tasks A–D) – Verification Checklist (SxE v1)

Use this checklist to decide if **Phase 1 – Ops** is 100% complete in Notion.

You only tick items when you have actually checked the live Notion workspace.

---

## 1. Ops Databases – Task A + Task B (6 DBs)

All under:

> `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub)`

### 1.1 Presence

[ ] `Projects` DB exists under the hub
[ ] `Tasks` DB exists under the hub
[ ] `Decisions` DB exists under the hub
[ ] `Approvals` DB exists under the hub
[ ] `Handover` DB exists under the hub
[ ] `IFNS_Workspace_DB – Index (DB)` exists under the hub

### 1.2 Schema (spot–check)

For each DB above:

[ ] Properties match the intent of the schema (titles, types, key selects) from the Task A/B packs.
[ ] Main view is usable (Name, Status, Owner/Assignee, key dates & links visible).

(You do **not** need to check every property; confirm that core fields and relations exist and look correct.)

### 1.3 Basic data

[ ] Each DB has at least a few **real rows** or **seed/sample rows** that look like serious IFNS data (not just one placeholder).

If any DB is clearly empty or wrong, note its name and fix later using:

- `Task_A_5_Ops_DBs_Notion_Execution_v2.md`
- `Task_B_Index_DB_Notion_Execution_v2.md`

---

## 2. Index Microhubs – Task C

Using the **Index DB** as the backbone, confirm that key microhubs exist.

Examples of expected microhubs (exact names may differ slightly):

[ ] An Ops–focused microhub page, with linked views of the Index DB filtered for Ops/Workspace assets.
[ ] A Quant/ML microhub page, with linked views filtered for Quant/ML assets.
[ ] A Solid/Architecture microhub page, with linked views filtered for Solid/Architect assets.

For each microhub page you find:

[ ] It contains at least one **linked database view** of the Index DB.
[ ] Filters/grouping on that view make sense for the slice (Scope, Type_v2, Owner_Role, etc.).

If a microhub you expect is missing, use:

- `Ops_Task_C_Microhubs_Execution_Report_v1.md`

to see where it was supposed to be created, then create the page and add a filtered Index view.

---

## 3. Related Ops + 22 Short Specs – Task D

### 3.1 22 short specs

Using:

- `Task_D_22_Short_Specs_Targets_Filled_v1.json`
- `Task_D_Short_Spec_Intros_Execution_Report_v1.md`

for reference, spot-check:

[ ] A sample of 3–5 of the 22 target spec pages → each has a clear **intro/summary block** at the top.
[ ] Those intros look consistent in style and structure (even if wording differs by spec).

You do **not** need to read every word or all 22 pages now; this is a **sanity check** to confirm Task D landed.

If you later find a spec with no intro, you can fix it using the Task D pack.

### 3.2 Related Ops / navigation callouts

On a few key Ops / DB / spec pages (your choice, but at least 3):

[ ] There is a “Related Operations” / “Where to go next” area or callout.
[ ] The links in that area point to reasonable follow-up assets (DBs, microhubs, or specs).

If those callouts are clearly missing everywhere, consider re-running or patching from:

- `Ops_Task_D_Step01_Related_Operations_Execution_Report_v1.md`

---

## 4. Registry alignment

Open:

> `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / IFNS – Workspace Registry (V2)`

### 4.1 Ops DB rows

For the 6 Ops DBs (Projects, Tasks, Decisions, Approvals, Handover, Index):

[ ] Each asset has exactly one row in the Registry.
[ ] `Type_v2` is `DB`.
[ ] `Scope` is appropriate (usually `Workspace`).
[ ] `Status` is `Live` (or your agreed final label).
[ ] `Summary` is non-empty and roughly matches how the DB is actually used.

### 4.2 Work status

If the Registry has a `Work_Status` or similar field:

[ ] `Work_Status` is `Done` for the 6 Ops DB assets listed above.

---

## 5. Final Phase 1 decision

Once you are comfortable ticking the boxes above (they do **not** all have to be perfect, but no major gaps), you can mark **Phase 1 – Ops** as:

> **Status:** Done (SxE–ready)

If you find gaps, list them briefly under one of these headings for follow-up:

- Missing / broken DB:
- Missing / broken microhub:
- Missing / broken short spec intro:
- Registry mismatch:

Once those are fixed, this checklist can be reused to confirm the fixes.
