# IFNS – Workspace Registry (V2) – Ops Phase 1 Update Plan (v1)

Scope: **Only** update registry rows related to Ops Phase 1 deliverables, so the registry truthfully reflects what is now live in Notion.

Targets to update in `IFNS – Workspace Registry (V2)`:

1. **Six Ops DBs**
2. **Step 01 – “00 Related operations” page**
3. **Key Ops microhubs** (Workspace hub, SoT hub, Telemetry & QC hub)

The goal is to align, for each asset:

- `Type_v2`
- `Scope`
- `Owner_Role`
- `Work_Status`

so that SxE can filter, slice, and trust the registry.

---

## 1. Assets to update

You can paste this table into a temporary Notion page or into Excel while updating the registry.

### 1.1 Core Ops DBs

| # | Asset label (Registry)                               | Expected Type_v2 | Scope     | Owner_Role           | Work_Status | Notes |
|---|------------------------------------------------------|------------------|----------|----------------------|------------|-------|
| 1 | IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Projects (DB)   | DB               | Ops      | Ops_Lead or PM       | Done       | Main project tracker for IFNS Ops and implementation streams. |
| 2 | IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Tasks (DB)      | DB               | Ops      | Ops_Team_Lead        | Done       | Central task board for all IFNS-related work items. |
| 3 | IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Decisions (DB)  | DB               | Ops      | SxE_Director or Governance | Done | Log of decisions that affect IFNS behavior, risk, or architecture. |
| 4 | IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Approvals (DB)  | DB               | Ops      | SxE_Director or Approver | Done | Formal sign‑offs (e.g., “SxE approved Ops Phase 1”). |
| 5 | IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Handover (DB)   | DB               | Ops      | Ops_Lead             | Done       | Captures agent/team handovers and phase boundaries. |
| 6 | IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Workspace_DB – Index (DB) | DB | Ops | Architect / Workspace_Architect | Done | Index DB that points to all workspace assets, used by microhubs & SxE. |

> If the registry currently uses slightly different labels for the DB names, map them logically but keep `Type_v2 = DB` and `Scope = Ops` for these six entries.

### 1.2 Step 01 – Related Operations

| # | Asset label (Registry)                                                  | Expected Type_v2 | Scope     | Owner_Role   | Work_Status | Notes |
|---|-------------------------------------------------------------------------|------------------|-----------|--------------|------------|-------|
| 7 | SoT Steps / Step 01 Preface / 00 Related operations (page)             | Spec or Hub_Page | Ops + SoT | SxE_Director | Done       | Narrative page listing Ops/Registry touchpoints for Step 01. |
| 8 | SoT Steps / Step 01 Preface (parent page)                              | Spec_Hub         | SoT       | SxE_Director | Done or In_review | Parent container for Step 01 specs; status depends on how far SxE considers Step 01 “final”. |

> If Step 01 itself is not yet “final” in SxE’s eyes, you can set `Work_Status = In_review` for the parent page but still mark `00 Related operations` as `Done` (because that slice is genuinely implemented).

### 1.3 Key Ops microhubs

These are content pages (not DBs) where Task C appended microhub narrative.

| # | Asset label (Registry)                                                   | Expected Type_v2 | Scope     | Owner_Role              | Work_Status | Notes |
|---|-------------------------------------------------------------------------|------------------|-----------|-------------------------|------------|-------|
| 9  | IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) – microhub content       | Hub_Page         | Ops       | Workspace_Architect     | Done       | Home hub for Ops DBs and Ops navigation. |
| 10 | IFNS_Workspace_DB / SoT Steps – index/microhub page                    | Hub_Page         | SoT       | Workspace_Architect or SxE_Director | Done | High-level SoT steps index, now enriched via Task C. |
| 11 | IFNS_Workspace_DB / Telemetry & QC (V2 hub) – microhub content         | Hub_Page         | Telemetry | Telemetry_Lead or QC_Lead | Done or Seeded | Telemetry & QC hub; mark Done if SxE agrees the current narrative is sufficient. |
| 12 | Any other clearly Ops-related microhub pages under Workspace hub       | Hub_Page         | Ops       | Workspace_Architect     | Done       | For example: Ops-focused views of the Index DB, if present in Registry. |

> Treat any microhub that is purely navigation/explanation as `Type_v2 = Hub_Page` (or whatever close equivalent exists in your registry standard).

If the registry uses different enums, map as:

- `DB` → database asset (Notion DB).
- `Hub_Page` / `Spec_Hub` → Notion pages whose primary role is navigation / grouping, not low-level specs.
- `Spec` → individual textual specification pages.

---

## 2. Concrete update steps in Notion

You can follow this as a small script for yourself or another agent.

### Step 1 – Open the Workspace Registry

1. In Notion, open `IFNS – Workspace Registry (V2)` (the DB, not just a page link).
2. Switch to a **table view** where you can see at least:
   - `Name` (or equivalent page title)
   - `Type_v2`
   - `Scope`
   - `Owner_Role`
   - `Work_Status`

### Step 2 – Locate the 6 Ops DB rows

For each DB name in section **1.1** above:

1. Use the registry’s search (top-right) to find the row whose name matches (or closely matches) the asset.
2. Confirm it points to the correct Notion DB (click through if needed).
3. Update fields as follows:

   - `Type_v2` → `DB`
   - `Scope`   → `Ops`
   - `Owner_Role` → one of:
     - `Ops_Lead`, `Ops_Team_Lead`, `Architect / Workspace_Architect`, or the closest role you actually use.
   - `Work_Status` → `Done`

4. If there is **no existing row**, create a new one using the same naming pattern as other rows, then set the above fields.

> Optional: Add a short description / notes field linking to the relevant Ops packs (Tasks A/B) so the registry row can be traced back to the source spec.

### Step 3 – Update Step 01 + 00 Related operations

1. In the registry, search for `Step 01 Preface`.
   - Confirm the row links to the `Step 01 Preface` page in Notion.
   - Set:
     - `Type_v2` → `Spec_Hub` (or the closest existing type for “hub spec page”).
     - `Scope`   → `SoT`
     - `Owner_Role` → `SxE_Director` (or whichever SxE role is accountable).
     - `Work_Status` →
       - `Done` if SxE considers Step 01 fully ready; or
       - `In_review` if Step 01 is still being refined.

2. Search for `00 Related operations`.
   - Confirm the row points to the child page under `Step 01 Preface`.
   - Set:
     - `Type_v2` → `Spec` or `Hub_Page` (depending on how you classify narrative relationship maps).
     - `Scope`   → `Ops + SoT` or just `Ops` (choose one consistent value; if you only have a single `Scope` select, use the most appropriate one, typically `Ops`).
     - `Owner_Role` → `SxE_Director` (owns the mapping of Ops ↔ SoT steps).
     - `Work_Status` → `Done` (this specific deliverable has been fully implemented and synced).

### Step 4 – Update key microhub pages

For each of the microhubs in **1.3**:

1. Find the corresponding row in the registry (by name).
2. Set:

   - `Type_v2` → `Hub_Page` or the closest available type for “narrative hub page”.
   - `Scope`   →
     - `Ops` for Workspace hub-related pages.
     - `SoT` for SoT steps hub pages.
     - `Telemetry` for Telemetry & QC hub pages.
   - `Owner_Role` →
     - `Workspace_Architect` (for workspace-wide hubs),
     - `SxE_Director` (for SoT hubs),
     - `Telemetry_Lead` or `QC_Lead` (for Telemetry & QC).

3. `Work_Status` →
   - `Done` for pages that are in the shape you want SxE to see now.
   - If you want to reserve the ability to refine microhub wording later, you can still mark as `Done` and use a separate field (e.g. `Needs_Polish`) if one exists.

---

## 3. Sanity check filters (to confirm the registry reflects reality)

After making the updates, create one or two quick views in the registry to double-check everything:

### View A – Ops DBs only

- Filter:
  - `Type_v2 = DB`
  - `Scope = Ops`
- Expected rows: the **6 core Ops DBs**.
- Scan `Work_Status` column → all should be `Done`.

### View B – Ops hubs & Step 01 related

- Filter:
  - `Scope contains Ops`
  - `Type_v2 in [Hub_Page, Spec, Spec_Hub]`
- You should see:
  - Workspace hub page,
  - Step 01 Preface,
  - 00 Related operations,
  - Any other Ops microhubs that were created in Phase 1.
- Scan `Work_Status` to ensure they’re `Done` or `In_review` according to your decision.

### View C – “Everything Ops that is Done”

- Filter:
  - `Scope = Ops`
  - `Work_Status = Done`
- This gives you a concise list of Ops assets that are ready for SxE and downstream use, including both DBs and key hub pages.

---

## 4. Summary (for your own notes)

Once you finish the updates above, you can safely say:

> “IFNS – Workspace Registry (V2) has been aligned with Ops Phase 1.
> The 6 core Ops DBs, Step 01 → 00 Related operations, and key microhubs are all marked Done with correct Type/Scope/Owner_Role.
> The registry is now a true reflection of what exists in the live Notion workspace for Ops Phase 1.”

If you want, we can also later turn this into:

- A small `Task_Registry_Ops_Phase1_Update_v1.md` in the Ops packs, or
- A checklist page inside Notion itself for future phase alignment.
