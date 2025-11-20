#!/usr/bin/env python3
import os, json, pathlib
from notion_client import Client, errors

ENC="utf-8-sig"
MAP="IFNS_Workspace_DB/config/workspace_companion_map.json"
OUT=MAP

def title(n): return {n: {"title": {}}}
def rich(n):  return {n: {"rich_text": {}}}
def select(n,ops):  return {n: {"select": {"options":[{"name":o} for o in ops]}}}
def mselect(n,ops): return {n: {"multi_select": {"options":[{"name":o} for o in ops]}}}
def datep(n): return {n: {"date": {}}}
def urlp(n):  return {n: {"url": {}}}
def people(n):return {n: {"people": {}}}
def number(n):return {n: {"number": {"format":"number"}}}
def relation(n,dbid): return {n: {"relation": {"database_id": dbid}}}

def ensure_page(c, parent_id, title):
    kids=c.blocks.children.list(parent_id).get("results",[])
    for k in kids:
        if k.get("type")=="child_page" and k["child_page"].get("title")==title:
            return k["id"]
    p=c.pages.create(parent={"type":"page_id","page_id":parent_id},
                     properties={"title":{"title":[{"type":"text","text":{"content":title}}]}})
    return p["id"]

def is_database(c, dbid):
    try:
        return "properties" in c.databases.retrieve(dbid)
    except errors.APIResponseError:
        return False

def find_child_db_id(c, parent_page_id, titles:set):
    kids=c.blocks.children.list(parent_page_id).get("results",[])
    for k in kids:
        if k.get("type")=="child_database" and k["child_database"].get("title") in titles:
            return k["id"]
    return None

def create_or_upsert_db(c, parent_page_id, titles:set, props:dict, fallback_title:str):
    dbid = find_child_db_id(c, parent_page_id, titles)
    if dbid and not is_database(c, dbid):
        dbid=None
    if dbid is None:
        db=c.databases.create(parent={"type":"page_id","page_id":parent_page_id},
                              title=[{"type":"text","text":{"content":fallback_title}}],
                              properties=props)
        return db["id"]
    # upsert any missing columns
    cur = c.databases.retrieve(dbid)["properties"]
    missing = {k:v for k,v in props.items() if k not in cur}
    if missing:
        c.databases.update(database_id=dbid, properties=missing)
    return dbid

def seed_rows_simple(c, dbid, rows):
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

def main():
    token=os.environ["NOTION_TOKEN"]; root_db=os.environ["WORKSPACE_DB_ID"]
    if not token or not root_db: raise SystemExit("Missing NOTION_TOKEN/WORKSPACE_DB_ID")
    c=Client(auth=token); m=json.load(open(MAP,"r",encoding=ENC)); hub=m["hub_page_id"]

    # Admin  Config Index
    admin_titles={"Admin  Config Index","Admin - Config Index","Admin  Config Index"}
    admin_props={
      **title("Name"), **rich("Key"), **rich("Value"),
      **select("Type",["bool","int","float","string"]),
      **mselect("Domain",["mirror","harness","reports"]), **rich("Notes")
    }
    admin_db_id=create_or_upsert_db(c, hub, admin_titles, admin_props, "Admin  Config Index")
    seed_rows_simple(c, admin_db_id, [
      {"__title__":"Auto-refresh enabled","Key":"mirror.auto_refresh.enabled","Value":"true","Type":"bool","Domain":"mirror","Notes":"UI auto refresh"},
      {"__title__":"Auto-refresh interval (s)","Key":"mirror.auto_refresh.interval_s","Value":"3","Type":"int","Domain":"mirror"},
      {"__title__":"Default route","Key":"harness.route.default","Value":"vwap","Type":"string","Domain":"harness"},
      {"__title__":"Replay speed","Key":"harness.replay.speed","Value":"1.0","Type":"float","Domain":"harness"},
      {"__title__":"Min run minutes","Key":"harness.runs.min_minutes","Value":"10","Type":"int","Domain":"harness"},
      {"__title__":"Daily summary enabled","Key":"reports.summary.enabled","Value":"true","Type":"bool","Domain":"reports"}
    ])

    # Companion DBs
    projects_id=create_or_upsert_db(c, hub, {"Projects"}, {
      **title("Name"), **select("Status",["Planned","Active","On hold","Done"]),
      **select("Priority",["High","Medium","Low"]), **people("Owner"),
      **datep("Start"), **datep("End"), **mselect("Tags",["SoT","UX","Runtime","Telemetry","DB"]),
      **rich("Description"), **relation("Workspace", root_db)
    }, "Projects")

    tasks_id=create_or_upsert_db(c, hub, {"Tasks"}, {
      **title("Name"), **select("Status",["Not Started","In Progress","Blocked","Done"]),
      **select("Priority",["High","Medium","Low"]), **people("Assignee"), **datep("Due"),
      **relation("Project", projects_id), **relation("Workspace", root_db),
      **mselect("Tags",["SoT","UX","Runtime","Telemetry","DB"])
    }, "Tasks")

    decisions_id=create_or_upsert_db(c, hub, {"Decisions"}, {
      **title("Decision"), **select("Status",["Proposed","Approved","Rejected","Changed"]),
      **datep("Date"), **people("Owner"),
      **relation("Project", projects_id), **relation("Workspace", root_db), **rich("Notes")
    }, "Decisions")

    approvals_id=create_or_upsert_db(c, hub, {"Approvals"}, {
      **title("Request"), **select("Status",["Pending","Approved","Denied"]),
      **datep("Date"), **rich("RequestedBy"), **rich("ApprovedBy"),
      **relation("Project", projects_id), **relation("Decision", decisions_id), **relation("Workspace", root_db)
    }, "Approvals")

    handover_id=create_or_upsert_db(c, hub, {"Handover"}, {
      **title("Item"), **select("Area",["Docs","ETL","Runtime","UX/SxE","QC/Telemetry"]),
      **select("Status",["Pending","Ready","Delivered"]), **datep("Due"), **people("Owner"),
      **urlp("Link"), **relation("Project", projects_id), **relation("Workspace", root_db)
    }, "Handover")

    # Saved Views  Playbook (doc)
    svp=ensure_page(c, hub, "Saved Views  Playbook")
    kids=c.blocks.children.list(svp).get("results",[])
    if not kids:
        c.blocks.children.append(svp, children=[
          {"object":"block","heading_2":{"rich_text":[{"type":"text","text":{"content":"How to use the saved views (quick tips)"}}]}},
          {"object":"block","bulleted_list_item":{"rich_text":[{"type":"text","text":{"content":"Projects  filter Status=Active, sort Priority, group by Tags"}}]}},
          {"object":"block","bulleted_list_item":{"rich_text":[{"type":"text","text":{"content":"Tasks  filter StatusDone, sort Due asc, group by Project"}}]}},
          {"object":"block","bulleted_list_item":{"rich_text":[{"type":"text","text":{"content":"Decisions  filter Status=Proposed, group by Project"}}]}},
          {"object":"block","bulleted_list_item":{"rich_text":[{"type":"text","text":{"content":"Approvals  filter Status=Pending, sort Date desc"}}]}},
          {"object":"block","bulleted_list_item":{"rich_text":[{"type":"text","text":{"content":"Handover  filter StatusDelivered, group by Area"}}]}}
        ])

    # map update
    m.update({
      "admin_config_db_id":admin_db_id, "projects_db_id":projects_id,
      "tasks_db_id":tasks_id, "decisions_db_id":decisions_id,
      "approvals_db_id":approvals_id, "handover_db_id":handover_id,
      "saved_views_playbook_page_id":svp
    })
    pathlib.Path(OUT).write_text(json.dumps(m,indent=2), encoding=ENC)
    print("OK: Admin Config (seeded) + companion DBs + Playbook created & map updated  no query dependency")

if __name__=="__main__":
    main()
