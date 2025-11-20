#!/usr/bin/env python3
import os, json, pathlib
from notion_client import Client, errors

ENC="utf-8-sig"
MAP="IFNS_Workspace_DB/config/workspace_companion_map.json"
OUT=MAP

def title(n):      return {n: {"title": {}}}
def rich(n):       return {n: {"rich_text": {}}}
def select(n,ops): return {n: {"select": {"options":[{"name":o} for o in ops]}}}
def mselect(n,ops):return {n: {"multi_select": {"options":[{"name":o} for o in ops]}}}
def datep(n):      return {n: {"date": {}}}
def urlp(n):       return {n: {"url": {}}}
def people(n):     return {n: {"people": {}}}
def number(n):     return {n: {"number": {"format":"number"}}}
def relation(n,dbid): return {n: {"relation": {"database_id": dbid}}}

def ensure_workspace_hub_page(c, saved_id=None, title_text="IFNS_Workspace_DB – Hub"):
    if saved_id:
        try:
            obj=c.pages.retrieve(saved_id)
            if obj.get("object")=="page":
                return saved_id
        except errors.APIResponseError:
            pass
    p=c.pages.create(parent={"type":"workspace","workspace":True},
        properties={"title":{"title":[{"type":"text","text":{"content":title_text}}]}})
    return p["id"]

def create_database(c, parent_page_id, title_text, props):
    db=c.databases.create(parent={"type":"page_id","page_id":parent_page_id},
                          title=[{"type":"text","text":{"content":title_text}}],
                          properties=props)
    if db.get("object")!="database" or "properties" not in db:
        raise RuntimeError(f"Create failed for {title_text}")
    return db["id"]

def ensure_doc_page(c, parent_page_id, title):
    kids=c.blocks.children.list(parent_page_id).get("results",[])
    for k in kids:
        if k.get("type")=="child_page" and k["child_page"].get("title")==title:
            return k["id"]
    p=c.pages.create(parent={"type":"page_id","page_id":parent_page_id},
        properties={"title":{"title":[{"type":"text","text":{"content":title}}]}})
    return p["id"]

def seed_admin_rows(c, dbid):
    rows=[
      {"Name":{"title":[{"type":"text","text":{"content":"Auto-refresh enabled"}}]},
       "Key":{"rich_text":[{"type":"text","text":{"content":"mirror.auto_refresh.enabled"}}]},
       "Value":{"rich_text":[{"type":"text","text":{"content":"true"}}]},
       "Type":{"select":{"name":"bool"}},
       "Domain":{"multi_select":[{"name":"mirror"}]},
       "Notes":{"rich_text":[{"type":"text","text":{"content":"UI auto refresh"}}]}},
      {"Name":{"title":[{"type":"text","text":{"content":"Auto-refresh interval (s)"}}]},
       "Key":{"rich_text":[{"type":"text","text":{"content":"mirror.auto_refresh.interval_s"}}]},
       "Value":{"rich_text":[{"type":"text","text":{"content":"3"}}]},
       "Type":{"select":{"name":"int"}},
       "Domain":{"multi_select":[{"name":"mirror"}]}},
      {"Name":{"title":[{"type":"text","text":{"content":"Default route"}}]},
       "Key":{"rich_text":[{"type":"text","text":{"content":"harness.route.default"}}]},
       "Value":{"rich_text":[{"type":"text","text":{"content":"vwap"}}]},
       "Type":{"select":{"name":"string"}},
       "Domain":{"multi_select":[{"name":"harness"}]}},
      {"Name":{"title":[{"type":"text","text":{"content":"Replay speed"}}]},
       "Key":{"rich_text":[{"type":"text","text":{"content":"harness.replay.speed"}}]},
       "Value":{"rich_text":[{"type":"text","text":{"content":"1.0"}}]},
       "Type":{"select":{"name":"float"}},
       "Domain":{"multi_select":[{"name":"harness"}]}},
      {"Name":{"title":[{"type":"text","text":{"content":"Min run minutes"}}]},
       "Key":{"rich_text":[{"type":"text","text":{"content":"harness.runs.min_minutes"}}]},
       "Value":{"rich_text":[{"type":"text","text":{"content":"10"}}]},
       "Type":{"select":{"name":"int"}},
       "Domain":{"multi_select":[{"name":"harness"}]}},
      {"Name":{"title":[{"type":"text","text":{"content":"Daily summary enabled"}}]},
       "Key":{"rich_text":[{"type":"text","text":{"content":"reports.summary.enabled"}}]},
       "Value":{"rich_text":[{"type":"text","text":{"content":"true"}}]},
       "Type":{"select":{"name":"bool"}},
       "Domain":{"multi_select":[{"name":"reports"}]}}
    ]
    for r in rows:
        c.pages.create(parent={"type":"database_id","database_id":dbid}, properties=r)

def main():
    token=os.environ["NOTION_TOKEN"]; root_db=os.environ["WORKSPACE_DB_ID"]
    if not token or not root_db: raise SystemExit("Missing NOTION_TOKEN/WORKSPACE_DB_ID")
    c=Client(auth=token)
    m=json.load(open(MAP,"r",encoding=ENC))

    hub=ensure_workspace_hub_page(c, m.get("hub_page_id"), "IFNS_Workspace_DB  Hub")
    m["hub_page_id"]=hub

    admin_title    = "Admin  Config Index (SoT)"
    projects_title = "Projects (SoT)"
    tasks_title    = "Tasks (SoT)"
    decisions_title= "Decisions (SoT)"
    approvals_title= "Approvals (SoT)"
    handover_title = "Handover (SoT)"

    admin_props={**title("Name"), **rich("Key"), **rich("Value"),
                 **select("Type",["bool","int","float","string"]),
                 **mselect("Domain",["mirror","harness","reports"]), **rich("Notes")}
    admin_db_id=create_database(c, hub, admin_title, admin_props)
    seed_admin_rows(c, admin_db_id)

    projects_id=create_database(c, hub, projects_title, {
      **title("Name"), **select("Status",["Planned","Active","On hold","Done"]),
      **select("Priority",["High","Medium","Low"]), **people("Owner"),
      **datep("Start"), **datep("End"), **mselect("Tags",["SoT","UX","Runtime","Telemetry","DB"]),
      **rich("Description"), **relation("Workspace", root_db)
    })
    tasks_id=create_database(c, hub, tasks_title, {
      **title("Name"), **select("Status",["Not Started","In Progress","Blocked","Done"]),
      **select("Priority",["High","Medium","Low"]), **people("Assignee"), **datep("Due"),
      **relation("Project", projects_id), **relation("Workspace", root_db),
      **mselect("Tags",["SoT","UX","Runtime","Telemetry","DB"])
    })
    decisions_id=create_database(c, hub, decisions_title, {
      **title("Decision"), **select("Status",["Proposed","Approved","Rejected","Changed"]),
      **datep("Date"), **people("Owner"), **relation("Project", projects_id),
      **relation("Workspace", root_db), **rich("Notes")
    })
    approvals_id=create_database(c, hub, approvals_title, {
      **title("Request"), **select("Status",["Pending","Approved","Denied"]),
      **datep("Date"), **rich("RequestedBy"), **rich("ApprovedBy"),
      **relation("Project", projects_id), **relation("Decision", decisions_id),
      **relation("Workspace", root_db)
    })
    handover_id=create_database(c, hub, handover_title, {
      **title("Item"), **select("Area",["Docs","ETL","Runtime","UX/SxE","QC/Telemetry"]),
      **select("Status",["Pending","Ready","Delivered"]), **datep("Due"), **people("Owner"),
      **urlp("Link"), **relation("Project", projects_id), **relation("Workspace", root_db)
    })

    svp=ensure_doc_page(c, hub, "Saved Views  Playbook")

    m.update({
      "admin_config_db_id":admin_db_id, "projects_db_id":projects_id,
      "tasks_db_id":tasks_id, "decisions_db_id":decisions_id,
      "approvals_db_id":approvals_id, "handover_db_id":handover_id,
      "saved_views_playbook_page_id":svp
    })
    pathlib.Path(OUT).write_text(json.dumps(m,indent=2), encoding=ENC)
    print("OK: Workspace Hub + SoT DBs + Playbook created; map updated")
if __name__=="__main__":
    main()
