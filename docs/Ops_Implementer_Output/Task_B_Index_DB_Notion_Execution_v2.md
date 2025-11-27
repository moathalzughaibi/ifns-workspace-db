# IFNS Notion Ops – Task B – IFNS_Workspace_DB – Index (DB) – Notion Execution (v2, Registry 2025-11-27)

**Mission**

Bring the **IFNS_Workspace_DB – Index (DB)** to “ready for SxE” status by:

- Ensuring the **Index DB** exists under the correct hub.
- Applying the **schema** from the Task B pack.
- Seeding **sample rows** to show intended usage.
- Creating/aligning a **spec page**.
- Updating the **IFNS – Workspace Registry (V2)** row for the Index DB.

This document assumes you are working against the latest workspace snapshot:

- **Notion export:** `Notion_ifns-workspace-db_2025_11_27.zip`
- **Registry DB:** `IFNS – Workspace Registry (V2)` inside that workspace.

You are not designing the Index from scratch. You are **implementing the architect’s design** from the Task B pack.

---

## 0. Where everything lives

### 0.1 Notion

- **Workspace hub root**
  `IFNS_Workspace_DB`

- **Index DB (target asset)** – preferred / expected path:

  > `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / IFNS_Workspace_DB – Index (DB)`

  There may already be a DB with this or a very similar name; Task B will either **upgrade** it or **create** it.

- **Workspace Registry DB**

  - `IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / IFNS – Workspace Registry (V2)`

  This DB has **one row per asset**, including the Index DB.

---

### 0.2 Git repo (VS Code)

Repo root (local):

- `E:\GitHub\ifns-workspace-db`

Relevant Task B contents (from the 2025-11-26 Ops pack, already placed in your repo under `docs/Ops_Implementer_Output/`):

- `docs/Ops_Implementer_Output/IFNS_Notion_Ops_Where_To_Put_In_Notion_Instructions_v1.md`
- `docs/Ops_Implementer_Output/IFNS_Notion_Ops_Implementer_Guide_v1.md`
- Task B pack:

  ```text
  docs/Ops_Implementer_Output/Task_B_Index_DB/
      IFNS_Workspace_DB_Index_schema.csv
      IFNS_Workspace_DB_Index_sample_rows.csv
      IFNS_Workspace_DB_Index_DB_Spec.md
      Task_B_Index_DB_Execution_Checklist.md
  ```

You will use *this* file as the high-level execution spec for Task B, in combination with the detailed checklist and the global “Where to Put” guide.

---

## 1. One-glance map – Index DB

Use this table as your anchor when working between VS Code, the Registry, and Notion.

| Item            | Source (repo)                                                              | Target in Notion                                                                                 |
|-----------------|---------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| Index DB schema | `docs/Ops_Implementer_Output/Task_B_Index_DB/IFNS_Workspace_DB_Index_schema.csv`        | Properties of `IFNS_Workspace_DB – Index (DB)`                                                   |
| Sample rows     | `docs/Ops_Implementer_Output/Task_B_Index_DB/IFNS_Workspace_DB_Index_sample_rows.csv`   | Rows in `IFNS_Workspace_DB – Index (DB)`                                                         |
| DB spec page    | `docs/Ops_Implementer_Output/Task_B_Index_DB/IFNS_Workspace_DB_Index_DB_Spec.md`        | Spec page under `IFNS_Workspace_DB – Index (DB)` hub (child page)                                |
| Registry row    | `IFNS – Workspace Registry (V2)` (existing row)                                         | Update status + summary for the Index DB asset                                                   |

---

## 2. Confirm the Index DB asset in the Registry

In **`IFNS – Workspace Registry (V2)`**:

1. Filter or search so you see the row where `Path` is:

   ```text
   IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / IFNS_Workspace_DB – Index (DB)
   ```

   (If the name is slightly different, e.g. small punctuation differences, use the closest match that clearly refers to the Index DB.)

2. Confirm at least these fields are present on that row:

   - `Path`
   - `Type_v2`
   - `Scope`
   - `Notion_URL`
   - `Status`
   - `Summary`
   - `Work_Status` (or equivalent “work status” field, if present)

You will **not** create a new row. Task B only **updates** the existing Index DB row.

---

## 3. Create or upgrade the Index DB in Notion

From the Registry row in §2, click `Notion_URL` to open the asset. There are two valid states:

### 3.1 If the Index DB already exists

If you see a Notion database (table or board view) with some columns and rows:

- Treat Task B as a **schema + seed data upgrade**:

  1. Keep the existing DB.
  2. Keep any real rows that already exist.
  3. Apply the schema from `IFNS_Workspace_DB_Index_schema.csv` (see §4).
  4. Import the sample rows from `IFNS_Workspace_DB_Index_sample_rows.csv` (see §5).

### 3.2 If the Index DB does not exist yet

If the Registry row’s URL opens to a regular page or a mostly-empty stub:

1. Under the `Workspace (DB) IFNS (Hub)` page, create a **new database** named:

   ```text
   IFNS_Workspace_DB – Index (DB)
   ```

2. Apply the schema from `IFNS_Workspace_DB_Index_schema.csv` as you define properties (see §4).
3. Import the sample rows CSV as the first set of rows (see §5).
4. Update the Registry row’s `Notion_URL` (if needed) so it points to the new DB.

> The end state should always be: **the Index is a single, well‑structured DB living under the Workspace (DB) IFNS hub.**

---

## 4. Apply the Index schema

Open the schema file in VS Code:

- `docs/Ops_Implementer_Output/Task_B_Index_DB/IFNS_Workspace_DB_Index_schema.csv`

The CSV columns describe each property:

- `Property` – exact Notion property name (e.g., `Path`, `Scope`, `Type_v2`, `Status`, `Owner_Role`, etc.).
- `Type` – Notion property type (Title, Text, Select, Multi-select, Relation, Checkbox, URL, etc.).
- `Required` – whether the property should normally be filled.
- `Notes` – purpose, valid values, or relations.

In the Notion Index DB (new or existing):

1. Open the **Properties** panel.
2. For each row in the schema CSV:

   - If the property does **not** exist yet:
     - Create it with the given name and the matching type.
   - If it exists but with a different type:
     - Change the type where safe (e.g., Text → Select).
   - For `Select` / `Multi-select` fields:
     - Add the suggested options from `Notes` (you can extend later if needed).

3. Ensure **one and only one Title property** exists; typically this is `Name` or `Asset`. If the schema expects a specific Title name, align it.

4. Configure useful default views (example small set):
   - **By Scope** – grouped or filtered by `Scope` (Workspace / SoT / Ops / etc.).
   - **By Type** – grouped by `Type_v2` (DB / Page / Hub / Script / etc.).
   - **All assets** – a simple table listing all rows.

The goal is for the Index DB to be **the main cross‑cutting map of the workspace**, in sync with the Registry.

---

## 5. Import and align sample rows

Now seed the Index DB with sample rows that show the intended usage.

1. In Notion, with the Index DB open, choose **Import → CSV** (or “Merge with CSV”).
2. Select:

   ```text
   IFNS_Workspace_DB_Index_sample_rows.csv
   ```

   from the Task B folder (or from a local copy of the pack).

3. Map CSV columns to properties:
   - Column names in the CSV should match the schema property names.
   - If a column appears that you don’t have as a property yet, go back to §4 and add it.

4. After import:
   - You should see a set of rows covering a representative variety of assets (DBs, hubs, specs, scripts, etc.).
   - Do **not** delete any real rows that already existed; keep them and adjust fields so they match the schema.

> These sample rows are a **bootstrap** to illustrate patterns — they do not replace real content already present in the Index DB.

---

## 6. Create / align the Index DB spec page

The Index DB must have a companion spec page explaining how it works.

### 6.1 Create or update the spec page

1. In VS Code, open:

   ```text
   docs/Ops_Implementer_Output/Task_B_Index_DB/IFNS_Workspace_DB_Index_DB_Spec.md
   ```

2. In Notion, under the **Index DB container** (same hub path as the DB), create or open a page named:

   ```text
   IFNS_Workspace_DB – Index – DB Spec
   ```

   (If a stub page already exists, reuse it.)

3. Paste the **entire body** of `IFNS_Workspace_DB_Index_DB_Spec.md` into that page:

   - If it was a stub → this is a **full body replacement**.
   - If it’s new → this is a **new spec page**.

4. From the Index DB, add a clear reference to this spec page, for example:

   - Add a simple URL property `Spec_URL` on the DB and set it to the spec page URL.
   - Or, if you prefer, later you can use relations once the Index DB manages its own specs.

Result: anyone using the Index DB can click through to “how this database is supposed to work”.

---

## 7. Update the Workspace Registry row for the Index DB

Go back to **`IFNS – Workspace Registry (V2)`**.

1. Locate the **existing row** for the Index DB (same as §2):

   ```text
   Path = IFNS_Workspace_DB / Workspace (DB) IFNS (Hub) / IFNS_Workspace_DB – Index (DB)
   ```

2. Confirm or set the following fields:

   - `Type_v2` = `DB`
   - `Scope` = `Workspace` (or equivalent, depending on your agreed vocabulary)
   - `Status` = `Live` (or `Draft` temporarily if waiting on review)
   - `Summary` – 1–3 sentences, for example:

     > “Workspace-wide index DB listing all IFNS assets with path, scope, type, status and owner role. Used by SxE, Ops and engineers as the master navigation and tracking layer.”

   - `Work_Status` (if present) → set to `Done` when Task B is complete.

3. Ensure `Notion_URL` points to the actual Index DB, not the spec page.

> The Registry and the Index DB reference each other: Registry row describes the asset, Index row for the Registry describes the DB itself.

---

## 8. Definition of “Task B is done”

You can consider **Task B – Index DB** complete when all of the following are true:

1. In Notion, under `Workspace (DB) IFNS (Hub)`, there is a single clearly named DB:

   - `IFNS_Workspace_DB – Index (DB)`

2. That DB:

   - Has properties aligned with `IFNS_Workspace_DB_Index_schema.csv`.
   - Contains the sample rows from `IFNS_Workspace_DB_Index_sample_rows.csv`, plus any real data that was already present.
   - Has at least one or two useful views (e.g., by Scope, by Type_v2).

3. There is a spec page:

   - `IFNS_Workspace_DB – Index – DB Spec` (or a close name),
   - populated with the content of `IFNS_Workspace_DB_Index_DB_Spec.md`,
   - clearly linked from the Index DB (URL property, or later relation).

4. In `IFNS – Workspace Registry (V2)`:

   - The Index DB’s row is present, has `Type_v2 = DB`, `Scope = Workspace`, a meaningful `Summary`, and `Status` set to `Live` (or your final equivalent).
   - `Work_Status` (or similar field) is set to `Done` for this asset.

At that point, **Task B** is done from a Notion perspective, and the Index DB is ready for:

- Task C (Index microhubs) and
- SxE-level review and navigation across the entire IFNS workspace.
