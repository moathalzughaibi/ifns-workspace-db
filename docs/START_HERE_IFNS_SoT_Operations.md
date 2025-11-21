# START HERE — IFNS SoT & Workspace Operations (Read Me First)

**Audience:** Any new agent touching IFNS (Notion ↔ Git ↔ Runtime).  
**Goal:** Make Notion the **Source of Truth (SoT)** and keep Git a faithful mirror—without loops.

---

## 0) SoT Contract (non‑negotiable)
- **Notion = SoT** for specs, schemas, catalogs, calendars, policies, and approvals.
- **Git = mirror** (exports from Notion + automation scripts).
- **Runtime = downstream**. Any change that affects schema/logic is reflected in Notion first, then mirrored to Git.

> If Notion and Git disagree, **Notion wins** (then re‑sync Git).

---

## 1) Required Access (before you start)
- Notion integration: **IFNS_Workspace_hup** (Full access) to the Teamspace and to the Hub page.
- Root Workspace DB ID (saved in env as `WORKSPACE_DB_ID`):  
  Example: `2b0b22c770d980578b64eb9a7a394901`.
- Repo: `E:\GitHub\ifns-workspace-db` (or Codespaces). Python venv active.

---

## 2) One‑time Env Setup (Windows PowerShell)
```powershell
cd E:\GitHub\ifns-workspace-db
.\.venv\Scripts\Activate.ps1
.\local_env\workspace_env.ps1
python -c "import os; print('TOKEN?', bool(os.getenv('NOTION_TOKEN')),'DB',os.getenv('WORKSPACE_DB_ID'))"
```
Expected: `TOKEN? True` and the correct DB ID.

---

## 3) Canonical Verification Checks (run in order)
1) **Root DB reachable**
```powershell
python -c "import os; from notion_client import Client; c=Client(auth=os.environ['NOTION_TOKEN']); d=c.databases.retrieve(os.environ['WORKSPACE_DB_ID']); print('root ok:', d['object'])"
```
Expected: `root ok: database`.

2) **Hub page is a PAGE**
```powershell
python -c "import json,os; from notion_client import Client; m=json.load(open(r'IFNS_Workspace_DB/config/workspace_companion_map.json',encoding='utf-8-sig')); c=Client(auth=os.environ['NOTION_TOKEN']); print('hub:', c.pages.retrieve(m['hub_page_id'])['object'])"
```
Expected: `hub: page`.

3) **Create+delete scratch DB (permission smoke‑test)**
```powershell
python -c "import os,json; from notion_client import Client; m=json.load(open(r'IFNS_Workspace_DB/config/workspace_companion_map.json',encoding='utf-8-sig')); c=Client(auth=os.environ['NOTION_TOKEN']); h=m['hub_page_id']; s=c.databases.create(parent={'type':'page_id','page_id':h}, title=[{'type':'text','text':{'content':'ZZZ Scratch (delete)'}}], properties={'Name':{'title':{}}}); print('db:',s['object']); c.blocks.delete(s['id']); print('deleted')"
```
Expected: `db: database` then `deleted`.

If any check fails, see **§7 Troubleshooting**.

---

## 4) Build the Workspace Companions (SoT DBs)
Creates under **Hub → SoT DBs** (with fallback to Hub):
- **Admin – Config Index (SoT)** (seeded)
- **Projects / Tasks / Decisions / Approvals / Handover (SoT)**

```powershell
python .\scriptsuild_workspace_hub_v3.py
```
Re‑run is safe (idempotent).

**Verify:**
```powershell
python -c "import os,json; from notion_client import Client; m=json.load(open(r'IFNS_Workspace_DB/config/workspace_companion_map.json',encoding='utf-8-sig')); c=Client(auth=os.environ['NOTION_TOKEN']); print('host=',c.pages.retrieve(m['db_host_page_id'])['object'],'admin=',c.databases.retrieve(m['admin_config_db_id'])['object'])"
```

---

## 5) Import the SoT Kits (14 Steps + Core ML P6 + QC Weekly)
- Files live under `docs/` (see naming in **§8 Naming & Layout**).
- Use the Notion importer script (coming with this repo) to:
  - Create **Step NN – <Title>** page,
  - Create child pages (Narrative & Intent, NN.1, NN.2, …),
  - Paste ```markdown``` blocks as page content.
- **Always** link the step pages back to companion DB views (Projects/Decisions/Approvals).

> If the importer is unavailable, import manually but keep naming strict.

---

## 6) Definition of Done (per change-set)
- All **six SoT DBs** exist and are reachable; Admin defaults seeded.
- New/updated **SoT pages** (Steps, Phase 6, QC Weekly) imported in Notion.
- **Repo mirror** updated (`docs/…`, scripts, map JSON) and pushed.
- **Verification checks** in §3 pass.
- **Error Ledger** updated (if new issue was encountered).

---

## 7) Troubleshooting (most common)
- **404/403 on DB/HUB:** share Teamspace + Hub page to **IFNS_Workspace_hup** (Full access).
- **PowerShell tries to execute Python text:** only run `python .\script.py` or `python -c "…"`. No heredocs.
- **Map missing keys (KeyError):** the builder failed before persisting; re-run after fixing the permission.
- **Titles breaking create:** use ASCII only; avoid en‑dash and double spaces.

Full list: `docs/IFNS_Error_Ledger.md`.

---

## 8) Naming & Layout (strict)
- **Root page:** `IFNS_Workspace_DB – Hub` (Notion)
- **SoT DB host page:** `SoT DBs`
- **DB titles (ASCII):** `Admin - Config Index (SoT)`, `Projects (SoT)`, `Tasks (SoT)`, `Decisions (SoT)`, `Approvals (SoT)`, `Handover (SoT)`
- **Steps:** `Step 07 – DIL` with child pages `01 – Narrative & Intent`, `07.1 – <Title>`, `07.2 – <Title>`, …
- **Repo paths:**  
  `docs/START_HERE_IFNS_SoT_Operations.md` (this file)  
  `docs/IFNS_Error_Ledger.md`  
  SoT kits in `docs/`

---

## 9) Escalation
- **Only** escalate if: permission blockers, structural contradictions, or API hard limits.
- Provide: last 20 lines of the failing command, and your current `workspace_companion_map.json`.

---

## 10) Quick Commit Snippet
```powershell
git add docs\START_HERE_IFNS_SoT_Operations.md docs\IFNS_Error_Ledger.md IFNS_Workspace_DB\config\workspace_companion_map.json scripts\*.py
git commit -m "Docs+Ops: START HERE guide; Error Ledger; SoT DBs map/scripts"
git push
```
