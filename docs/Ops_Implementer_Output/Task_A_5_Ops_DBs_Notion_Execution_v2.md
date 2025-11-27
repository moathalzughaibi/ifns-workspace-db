# IFNS Notion Ops – Task A – 5 Ops DBs – Notion Execution (v2, Registry 2025‑11‑27)

**Mission**

Turn the five existing “bare” Ops databases —

- **Projects**
- **Tasks**
- **Decisions**
- **Approvals**
- **Handover**

from 1‑row skeletons into usable operational DBs, using:

- the design pack: **Task_A_5_Ops_DBs** (schemas, sample rows, specs), and
- the latest workspace snapshot **Notion_ifns-workspace-db_2025_11_27** with **IFNS – Workspace Registry (V2)**.

You are not redesigning IFNS. You are **upgrading the schema + docs + registry** for these 5 DBs.

---

## 0. Where everything lives

### 0.1 Notion

- **Workspace hub**
  `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub)`

- **Ops DBs (targets for Task A)**

  - `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Projects`
  - `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Tasks`
  - `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Decisions`
  - `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Approvals`
  - `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Handover`

  Each of these is already a Notion database with columns **Name** + **Workspace** and 1 seed row.

- **Workspace Registry DB**

  - `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / IFNS – Workspace Registry (V2)`

  This DB has one row per workspace asset. You will use it to **locate DBs** and then **update their metadata**.

---

### 0.2 Git repo (VS Code)

Repo root (local):

- `E:\GitHub\ifns-workspace-db`

Relevant contents (already present in the 2025‑11‑27 snapshot):

- `docs/Ops_Implementer_Output/IFNS_Notion_Ops_Implementer_Output_2025_11_26.zip`
  → zipped design packs for **Tasks A–D**.
- `docs/Ops_Implementer_Output/IFNS_Notion_Ops_Where_To_Put_In_Notion_Instructions_v1.md`
  → global “where does each file go” map.
- `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs_Notion_Execution_v2.md`
  → **this file** (place it here in the repo).

After you unzip the pack, you should see:

- `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/`
  - `Projects_schema.csv`
  - `Tasks_schema.csv`
  - `Decisions_schema.csv`
  - `Approvals_schema.csv`
  - `Handover_schema.csv`
  - `Projects_sample_rows.csv`
  - `Tasks_sample_rows.csv`
  - `Decisions_sample_rows.csv`
  - `Approvals_sample_rows.csv`
  - `Handover_sample_rows.csv`
  - `Projects_DB_Spec.md`
  - `Tasks_DB_Spec.md`
  - `Decisions_DB_Spec.md`
  - `Approvals_DB_Spec.md`
  - `Handover_DB_Spec.md`
  - `Phase1_Dbs_Implementation_Guide.md` (reference only)

---

## 1. One‑glance map – 5 DBs

Use this table as your anchor when working between VS Code, the Registry, and Notion.

| # | DB        | Registry.Path (row to edit)                                                    | Schema CSV (repo)                                                      | Sample rows CSV (repo)                                                     | DB Spec file (repo)                                                          |
|:-:|-----------|--------------------------------------------------------------------------------|------------------------------------------------------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| 1 | Projects  | `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Projects`                    | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Projects_schema.csv`    | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Projects_sample_rows.csv`    | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Projects_DB_Spec.md`           |
| 2 | Tasks     | `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Tasks`                       | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Tasks_schema.csv`       | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Tasks_sample_rows.csv`       | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Tasks_DB_Spec.md`              |
| 3 | Decisions | `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Decisions`                   | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Decisions_schema.csv`   | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Decisions_sample_rows.csv`   | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Decisions_DB_Spec.md`          |
| 4 | Approvals | `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Approvals`                   | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Approvals_schema.csv`   | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Approvals_sample_rows.csv`   | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Approvals_DB_Spec.md`          |
| 5 | Handover  | `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Handover`                    | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Handover_schema.csv`    | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Handover_sample_rows.csv`    | `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Handover_DB_Spec.md`           |

---

## 2. Registry first – find and open the right DBs

### 2.1 Filter the Registry (once)

In **`IFNS – Workspace Registry (V2)`**:

1. Create a temporary view or filter:
   - `Scope` = `Workspace`
   - `Type_v2` = `DB`
2. Scan the Path column and confirm you have these 5 rows:

   - `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Projects`
   - `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Tasks`
   - `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Decisions`
   - `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Approvals`
   - `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / Handover`

There should be **exactly one row per path**.

### 2.2 Open the DBs from the Registry

For each of the 5 rows:

1. Click the `Notion_URL` field to open the DB.
2. Verify you are seeing a small table with:
   - Columns: `Name`, `Workspace`.
   - A small number of seed rows (e.g., “IFNS Workspace bring‑up”, “Approve workspace structure”…).
3. Keep the Registry view open in a separate tab – you will come back to it in section 5.

---

## 3. Apply the schemas (properties) in Notion

You will now **upgrade the properties** of each DB to match the CSV schema.

> Work DB by DB (Projects → Tasks → Decisions → Approvals → Handover).
> The pattern is the same every time.

### 3.1 Read the schema in VS Code

For the DB you are working on (example: Projects):

1. In VS Code, open the corresponding `*_schema.csv`, e.g.
   `docs/Ops_Implementer_Output/Task_A_5_Ops_DBs/Projects_schema.csv`.
2. Read the columns:
   - **Property** – exact Notion property name.
   - **Type** – Notion property type (Title, Text, Select, Multi‑select, Person, Date, Relation, etc.).
   - **Required** – whether this property should normally be filled.
   - **Description / Notes** – what it is for; suggested options for Select/Multi‑select.

Keep this file visible while editing the DB in Notion.

### 3.2 Create / align properties

In the Notion DB:

1. Open the **Properties** panel.
2. For each row in the schema CSV:

   - If the property already exists:
     - Ensure the name matches exactly.
     - Change the **type** to match the schema (e.g., Text → Select, Select → Multi‑select).
     - For `Status` / `Priority` / similar:
       - Add the suggested options from the `Notes` column (you can add more later if needed).

   - If the property does **not** exist:
     - Add a new property with the given name and type.
     - Use the description to choose sensible default options/format.

3. Keep **`Name`** as the primary Title property in every DB.

#### 3.2.1 Relations between the 5 Ops DBs

Some schema rows have `Type` like `Relation: Projects`, `Relation: Tasks`, etc. For these:

- Create a **Relation** property.
- When Notion asks “Which database?”, select the corresponding Ops DB under the same hub:

  - `Relation: Projects` → `Projects` DB.
  - `Relation: Tasks` → `Tasks` DB.
  - `Relation: Decisions` → `Decisions` DB.
  - `Relation: Approvals` → `Approvals` DB.
  - `Relation: Handover` → `Handover` DB.

> These relations make the 5 DBs behave like one system:
> projects ↔ tasks ↔ decisions ↔ approvals ↔ handover.

#### 3.2.2 Relations that depend on the Index DB (Task B)

Some schema rows use `Type` values like **`Relation: Index DB`** or **`Relation: Specs`**.

- These are meant to point to **`IFNS_Workspace_DB – Index (DB)`**, which is created in **Task B**.
- For Task A you have **two acceptable options**:
  1. **Preferred:** Leave these properties for later.
     - Note them as TODOs in your own checklist.
  2. If the Index DB already exists in your workspace, you may configure them now, pointing the relation to that DB.

Do **not** invent a temporary target DB just to satisfy the relation type.

### 3.3 Clean default views

For each DB, create or adjust at least one **main table view**:

- Name: **`Main`** or **`All`**.
- Visible columns (suggestion):

  - **Projects:** Name, Status, Owner_Role, Project_Owner, Area, Priority, Start_Date, Target_End_Date.
  - **Tasks:** Name, Status, Task_Type, Assignee, Project, Due_Date.
  - **Decisions:** Name, Status, Decision_Type, Decision_Owner, Decision_Date, Related_Assets / Related_Project.
  - **Approvals:** Name, Status, Approval_Type, Approver, Related_Decision, Due_Date.
  - **Handover:** Name, Status, Handover_Owner, Related_Project, Target_Date.

You can add **secondary views** later (e.g., Kanban by Status for Tasks), but they are not required to complete Task A.

---

## 4. Import and align sample rows

### 4.1 Check existing rows

Before importing:

- Keep any existing **real** rows (e.g., genuine projects or tasks).
- Treat current placeholder rows as either:
  - real items (rename them to fit schema), or
  - bootstrap examples you can keep alongside the new samples.

### 4.2 Import sample rows from CSV

For each DB:

1. In the Notion DB, use **“Merge with CSV”** or **Import → CSV**.
2. Select the corresponding `*_sample_rows.csv` from the repo (or from a local copy of the pack):
   - Example for Projects: `Projects_sample_rows.csv`.
3. Map CSV columns to the properties you created:
   - Property names in the CSV match the schema (Name, Status, Owner_Role, etc.).
   - If a column does not exist yet, go back to §3.2 and add it.

Guidelines:

- Sample rows are **safe examples** to show intended usage.
- Tags like `bootstrap` / `workspace` / `governance` are deliberate.
- Do **not** delete real data to make room for samples.

After import, you should see several well‑formed example rows per DB.

---

## 5. Attach DB spec pages

Each Ops DB needs a short spec page under its hub explaining how it is used.

For each DB:

1. In VS Code, open the matching `*_DB_Spec.md` file (see the table in §1).
2. In Notion, under the corresponding hub path, create a child page with the same title as the first `#` heading in the spec:
   - `Projects — Operational DB Spec`
   - `Tasks — Operational DB Spec`
   - `Decisions — Operational DB Spec`
   - `Approvals — Operational DB Spec`
   - `Handover — Operational DB Spec`
3. Paste the full body of the `*_DB_Spec.md` file into that page.
4. From the DB (Projects/Tasks/…), add a simple link or relation to its spec page (for example, a “Spec_Page” URL field or a relation via the future Index DB).

Result: every Ops DB has a clear, human‑readable “how to use this” page attached to it.

---

## 6. Update Workspace Registry rows (Task A scope)

Once the 5 DBs are upgraded and seeded, return to **`IFNS – Workspace Registry (V2)`**.

For each of the 5 rows listed in §2.1:

1. **Confirm technical fields**
   - `Type_v2` → should be `DB`. If not, set it.
   - `Scope` → should be `Workspace`.
   - `V2_Scope` → leave as‑is (typically `In_V2`).

2. **Set Status**
   - Set `Status` to `Live`.
     - If you want a softer label until internal review, you may temporarily use `Draft`, but the target state after review is `Live`.

3. **Write a clear Summary** (overwrite if needed)
   Use 1–3 sentences per row. Examples you can adapt:

   - **Projects**
     “Operational projects DB tracking IFNS projects, owners, areas, priorities and key dates. Used by Ops, PM and Notion admin to manage work streams.”

   - **Tasks**
     “Operational tasks DB linked to Projects, Decisions, Approvals and Handover. Used for day‑to‑day execution, My Tasks views and follow‑up.”

   - **Decisions**
     “Operational decisions DB recording key IFNS decisions, their impact and linked assets. Feeds governance, audit trails and downstream tasks.”

   - **Approvals**
     “Operational approvals DB capturing required approvals for projects, tasks and handovers. Supports governance and blocking logic.”

   - **Handover**
     “Operational handover DB describing ownership changes and handover packets for IFNS assets. Ensures continuity when owners or teams change.”

4. **Work status flag (if present)**
   - If the Registry has a property like `Work_Status` or similar, set it to `Done` for these 5 rows.

> Do **not** create new rows for these DBs. Task A only updates the existing registry entries.

---

## 7. Definition of “Task A is done”

You can consider **Task A – 5 Ops DBs** complete when **all** of the following are true:

1. In Notion, each of the 5 DBs:
   - Has properties matching its schema CSV (except Index‑dependent relations, which may be deferred).
   - Contains the sample rows from the `*_sample_rows.csv` plus any real rows you already had.
   - Has at least one clean main view suitable for daily use.

2. Each DB has a child spec page in the workspace with the content from its `*_DB_Spec.md` file.

3. In `IFNS – Workspace Registry (V2)`:
   - The 5 rows for Projects/Tasks/Decisions/Approvals/Handover have:
     - `Type_v2 = DB`
     - `Scope = Workspace`
     - `Status = Live` (or equivalent final label)
     - A non‑empty, meaningful `Summary`.

4. You have no TODOs outstanding for Task A except:
   - Relations that explicitly depend on `IFNS_Workspace_DB – Index (DB)` (to be finalized in Task B).

At that point, the 5 Ops DBs are ready for SxE and future automation, and you can move on to **Task B – Index DB**.
