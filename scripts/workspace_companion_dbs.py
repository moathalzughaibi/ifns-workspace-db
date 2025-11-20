#!/usr/bin/env python3
import os, json, pathlib
from notion_client import Client

ENC="utf-8-sig"
MAP="IFNS_Workspace_DB/config/workspace_companion_map.json"   # has hub_page_id
OUT= "IFNS_Workspace_DB/config/workspace_companion_map.json"   # we’ll update in place

# Minimal property shorthands
def title(name):     return {name: {"title": {}}}
def rich(name):      return {name: {"rich_text": {}}}
def select(name,ops):return {name: {"select": {"options":[{"name":o} for o in ops]}}}
def mselect(n,ops):  return {n: {"multi_select": {"options":[{"name":o} for o in ops]}}}
def datep(name):     return {name: {"date": {}}}
def urlp(name):      return {name: {"url": {}}}
def people(name):    return {name: {"people": {}}}
def number(name):    return {name: {"number": {"format":"number"}}}
def relation(name,dbid): return {name: {"relation": {"database_id": dbid}}}

def create_db(c, parent_page_id, title, props):
    # if already exists under parent with same title, return it
    kids=c.blocks.children.list(parent_page_id).get("results",[])
    for k in kids:
        if k.get("type")=="child_database" and k["child_database"].get("title")==title:
            return k["id"]
    db=c.databases.create(
        parent={"type":"page_id","page_id":parent_page_id},
        title=[{"type":"text","text":{"content":title}}],
        properties=props
    )
    return db["id"]

def seed_rows(c, dbid, rows):
    for r in rows:
        props={}
        for k,v in r.items():
            if k=="__title__":
                props["Name"]={"title":[{"type":"text","text":{"content":v}}]}
            elif isinstance(v,str):
                props[k]={"rich_text":[{"type":"text","text":{"content":v}}]}
            elif isinstance(v,bool):
                props[k]={"select":{"name":"true" if v else "false"}}
            elif isinstance(v,(int,float)):
                props[k]={"number":v}
        c.pages.create(parent={"type":"database_id","database_id":dbid}, properties=props)

def ensure_page(c, parent_id, title):
    kids=c.blocks.children.list(parent_id).get("results",[])
    for k in kids:
        if k.get("type")=="child_page" and k["child_page"].get("title")==title:
            return k["id"]
    p=c.pages.create(parent={"type":"page_id","page_id":parent_id},
                     properties={"title":{"title":[{"type":"text","text":{"content":title}}]}})
    return p["id"]

def main():
    token=os.environ["NOTION_TOKEN"]; root_db=os.environ["WORKSPACE_DB_ID"]
    if not token or not root_db: raise SystemExit("Missing NOTION_TOKEN/WORKSPACE_DB_ID")
    c=Client(auth=token)
    m=json.load(open(MAP,"r",encoding=ENC))
    hub=m["hub_page_id"]

    # --- Admin  Config Index ---
    admin_db_id = create_db(
        c, hub, "Admin  Config Index",
        {
          **title("Name"),
          **rich("Key"),
          **rich("Value"),
          **select("Type", ["bool","int","float","string"]),
          **mselect("Domain", ["mirror","harness","reports"]),
          **rich("Notes")
        }
    )
    m["admin_config_db_id"]=admin_db_id

    # seed defaults (you can add more later)
    defaults=[
      {"__title__":"Auto-refresh enabled","Key":"mirror.auto_refresh.enabled","Value":"true","Type":"bool","Domain":"mirror","Notes":"UI auto refresh"},
      {"__title__":"Auto-refresh interval (s)","Key":"mirror.auto_refresh.interval_s","Value":"3","Type":"int","Domain":"mirror"},
      {"__title__":"Default route","Key":"harness.route.default","Value":"vwap","Type":"string","Domain":"harness"},
      {"__title__":"Replay speed","Key":"harness.replay.speed","Value":"1.0","Type":"float","Domain":"harness"},
      {"__title__":"Min run minutes","Key":"harness.runs.min_minutes","Value":"10","Type":"int","Domain":"harness"},
      {"__title__":"Daily summary enabled","Key":"reports.summary.enabled","Value":"true","Type":"bool","Domain":"reports"}
    ]
    seed_rows(c, admin_db_id, defaults)

    # --- Companion DBs (Projects/Tasks/Decisions/Approvals/Handover) ---
    # We also relate them to the Workspace DB (root_db)
    projects_id = create_db(
        c, hub, "Projects",
        {
          **title("Name"),
          **select("Status", ["Planned","Active","On hold","Done"]),
          **select("Priority", ["High","Medium","Low"]),
          **people("Owner"),
          **datep("Start"),
          **datep("End"),
          **mselect("Tags", ["SoT","UX","Runtime","Telemetry","DB"]),
          **rich("Description"),
          **relation("Workspace", root_db)
        }
    )
    tasks_id = create_db(
        c, hub, "Tasks",
        {
          **title("Name"),
          **select("Status", ["Not Started","In Progress","Blocked","Done"]),
          **select("Priority", ["High","Medium","Low"]),
          **people("Assignee"),
          **datep("Due"),
          **relation("Project", projects_id),
          **relation("Workspace", root_db),
          **mselect("Tags", ["SoT","UX","Runtime","Telemetry","DB"])
        }
    )
    decisions_id = create_db(
        c, hub, "Decisions",
        {
          **title("Decision"),
          **select("Status", ["Proposed","Approved","Rejected","Changed"]),
          **datep("Date"),
          **people("Owner"),
          **relation("Project", projects_id),
          **relation("Workspace", root_db),
          **rich("Notes")
        }
    )
    approvals_id = create_db(
        c, hub, "Approvals",
        {
          **title("Request"),
          **select("Status", ["Pending","Approved","Denied"]),
          **datep("Date"),
          **rich("RequestedBy"),
          **rich("ApprovedBy"),
          **relation("Project", projects_id),
          **relation("Decision", decisions_id),
          **relation("Workspace", root_db)
        }
    )
    handover_id = create_db(
        c, hub, "Handover",
        {
          **title("Item"),
          **select("Area", ["Docs","ETL","Runtime","UX/SxE","QC/Telemetry"]),
          **select("Status", ["Pending","Ready","Delivered"]),
          **datep("Due"),
          **people("Owner"),
          **urlp("Link"),
          **relation("Project", projects_id),
          **relation("Workspace", root_db)
        }
    )
    m.update({
      "projects_db_id":projects_id,
      "tasks_db_id":tasks_id,
      "decisions_db_id":decisions_id,
      "approvals_db_id":approvals_id,
      "handover_db_id":handover_id
    })

    # --- Saved Views  Playbook (doc page) ---
    svp = ensure_page(c, hub, "Saved Views  Playbook")
    c.blocks.children.append(svp, children=[
      {"object":"block","heading_2":{"rich_text":[{"type":"text","text":{"content":"How to use the saved views (quick tips)"}}]}},
      {"object":"block","bulleted_list_item":{"rich_text":[{"type":"text","text":{"content":"Projects  filter Status=Active, sort Priority, group by Tags"}}]}},
      {"object":"block","bulleted_list_item":{"rich_text":[{"type":"text","text":{"content":"Tasks  filter StatusDone, sort Due asc, group by Project"}}]}},
      {"object":"block","bulleted_list_item":{"rich_text":[{"type":"text","text":{"content":"Decisions  filter Status=Proposed, group by Project"}}]}},
      {"object":"block","bulleted_list_item":{"rich_text":[{"type":"text","text":{"content":"Approvals  filter Status=Pending, sort Date desc"}}]}},
      {"object":"block","bulleted_list_item":{"rich_text":[{"type":"text","text":{"content":"Handover  filter StatusDelivered, group by Area"}}]}}
    ])
    m["saved_views_playbook_page_id"]=svp

    pathlib.Path(OUT).write_text(json.dumps(m,indent=2), encoding=ENC)
    print("OK: Admin Config DB + companion DBs + Playbook created & map updated")

if __name__=="__main__":
    main()
