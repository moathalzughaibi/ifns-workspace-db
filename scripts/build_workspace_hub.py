#!/usr/bin/env python3
import os, json, pathlib
from notion_client import Client, errors

ENC = "utf-8-sig"
MAP = pathlib.Path("IFNS_Workspace_DB/config/workspace_companion_map.json")

def ensure_dir(p: pathlib.Path):
    p.parent.mkdir(parents=True, exist_ok=True)

def read_map() -> dict:
    if MAP.exists():
        return json.loads(MAP.read_text(encoding=ENC))
    return {"hub_page_id": ""}

def write_map(m: dict):
    ensure_dir(MAP)
    MAP.write_text(json.dumps(m, indent=2), encoding=ENC)

# property helpers
def title(n):      return {n: {"title": {}}}
def rich(n):       return {n: {"rich_text": {}}}
def select(n,ops): return {n: {"select": {"options":[{"name":o} for o in ops]}}}
def mselect(n,ops):return {n: {"multi_select": {"options":[{"name":o} for o in ops]}}}
def datep(n):      return {n: {"date": {}}}
def urlp(n):       return {n: {"url": {}}}
def people(n):     return {n: {"people": {}}}
def relation(n,db):return {n: {"relation": {"database_id": db}}}

def ensure_workspace_hub_page(notion, saved_id=None, title="IFNS_Workspace_DB - Hub"):
    # reuse if valid
    if saved_id:
        try:
            obj = notion.pages.retrieve(saved_id)
            if obj.get("object") == "page":
                return saved_id
        except errors.APIResponseError:
            pass
    # else create top-level page (workspace parent)
    page = notion.pages.create(
        parent={"type":"workspace","workspace":True},
        properties={"title":{"title":[{"type":"text","text":{"content":title}}]}}
    )
    return page["id"]

def create_db(notion, parent_page_id, title_text, props):
    db = notion.databases.create(
        parent={"type":"page_id","page_id":parent_page_id},
        title=[{"type":"text","text":{"content":title_text}}],
        properties=props
    )
    if db.get("object") != "database" or "properties" not in db:
        raise RuntimeError(f"Create failed for {title_text}")
    return db["id"]

def seed_admin(notion, dbid):
    rows = [
      ("Auto-refresh enabled","mirror.auto_refresh.enabled","true","bool",["mirror"],"UI auto refresh"),
      ("Auto-refresh interval (s)","mirror.auto_refresh.interval_s","3","int",["mirror"],""),
      ("Default route","harness.route.default","vwap","string",["harness"],""),
      ("Replay speed","harness.replay.speed","1.0","float",["harness"],""),
      ("Min run minutes","harness.runs.min_minutes","10","int",["harness"],""),
      ("Daily summary enabled","reports.summary.enabled","true","bool",["reports"],""),
    ]
    for name,key,val,typ,dom,notes in rows:
        notion.pages.create(parent={"type":"database_id","database_id":dbid},
          properties={
            "Name":{"title":[{"type":"text","text":{"content":name}}]},
            "Key":{"rich_text":[{"type":"text","text":{"content":key}}]},
            "Value":{"rich_text":[{"type":"text","text":{"content":val}}]},
            "Type":{"select":{"name":typ}},
            "Domain":{"multi_select":[{"name":d} for d in dom]},
            "Notes":{"rich_text":[{"type":"text","text":{"content":notes}}]} if notes else {}
          })

def main():
    token=os.environ.get("NOTION_TOKEN"); root_db=os.environ.get("WORKSPACE_DB_ID")
    if not token or not root_db:
        raise SystemExit("Missing NOTION_TOKEN or WORKSPACE_DB_ID")

    notion = Client(auth=token)
    m = read_map()

    # 1) Hub PAGE (top-level)
    hub = ensure_workspace_hub_page(notion, m.get("hub_page_id"), "IFNS_Workspace_DB - Hub")
    m["hub_page_id"] = hub

    # 2) Databases (ASCII titles  no double spaces, no en-dash)
    admin_title    = "Admin - Config Index (SoT)"
    projects_title = "Projects (SoT)"
    tasks_title    = "Tasks (SoT)"
    decisions_title= "Decisions (SoT)"
    approvals_title= "Approvals (SoT)"
    handover_title = "Handover (SoT)"

    admin_props = {
      **title("Name"), **rich("Key"), **rich("Value"),
      **select("Type",["bool","int","float","string"]),
      **mselect("Domain",["mirror","harness","reports"]),
      **rich("Notes")
    }
    admin_id = create_db(notion, hub, admin_title, admin_props)
    seed_admin(notion, admin_id)

    projects_id = create_db(notion, hub, projects_title, {
      **title("Name"),
      **select("Status",["Planned","Active","On hold","Done"]),
      **select("Priority",["High","Medium","Low"]),
      **people("Owner"), **datep("Start"), **datep("End"),
      **mselect("Tags",["SoT","UX","Runtime","Telemetry","DB"]),
      **rich("Description"), **relation("Workspace", root_db)
    })
    tasks_id = create_db(notion, hub, tasks_title, {
      **title("Name"),
      **select("Status",["Not Started","In Progress","Blocked","Done"]),
      **select("Priority",["High","Medium","Low"]),
      **people("Assignee"), **datep("Due"),
      **relation("Project", projects_id), **relation("Workspace", root_db),
      **mselect("Tags",["SoT","UX","Runtime","Telemetry","DB"])
    })
    decisions_id = create_db(notion, hub, decisions_title, {
      **title("Decision"),
      **select("Status",["Proposed","Approved","Rejected","Changed"]),
      **datep("Date"), **people("Owner"),
      **relation("Project", projects_id), **relation("Workspace", root_db),
      **rich("Notes")
    })
    approvals_id = create_db(notion, hub, approvals_title, {
      **title("Request"),
      **select("Status",["Pending","Approved","Denied"]),
      **datep("Date"), **rich("RequestedBy"), **rich("ApprovedBy"),
      **relation("Project", projects_id), **relation("Decision", decisions_id),
      **relation("Workspace", root_db)
    })
    handover_id = create_db(notion, hub, handover_title, {
      **title("Item"),
      **select("Area",["Docs","ETL","Runtime","UX/SxE","QC/Telemetry"]),
      **select("Status",["Pending","Ready","Delivered"]),
      **datep("Due"), **people("Owner"), **urlp("Link"),
      **relation("Project", projects_id), **relation("Workspace", root_db)
    })

    # 3) Small doc page
    svp = notion.pages.create(parent={"type":"page_id","page_id":hub},
      properties={"title":{"title":[{"type":"text","text":{"content":"Saved Views - Playbook"}}]}})["id"]

    # 4) Persist IDs
    m.update({
      "admin_config_db_id":admin_id,
      "projects_db_id":projects_id,
      "tasks_db_id":tasks_id,
      "decisions_db_id":decisions_id,
      "approvals_db_id":approvals_id,
      "handover_db_id":handover_id,
      "saved_views_playbook_page_id":svp
    })
    write_map(m)

    print("DONE",
          "\nHub page:", hub,
          "\nAdmin DB:", admin_id,
          "\nProjects/Tasks/Decisions/Approvals/Handover:",
          projects_id, tasks_id, decisions_id, approvals_id, handover_id,
          "\nSaved Views Page:", svp)
if __name__ == "__main__":
    main()
