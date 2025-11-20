#!/usr/bin/env python3
import os, json, pathlib, re
from notion_client import Client, errors

ENC="utf-8-sig"
MAP="IFNS_Workspace_DB/config/workspace_companion_map.json"
OUT=MAP

# ---- property helpers
def title(name):      return {name: {"title": {}}}
def rich(name):       return {name: {"rich_text": {}}}
def select(name,ops): return {name: {"select": {"options":[{"name":o} for o in ops]}}}
def mselect(n,ops):   return {n: {"multi_select": {"options":[{"name":o} for o in ops]}}}
def datep(name):      return {name: {"date": {}}}
def urlp(name):       return {name: {"url": {}}}
def people(name):     return {name: {"people": {}}}
def number(name):     return {name: {"number": {"format":"number"}}}
def relation(name,dbid): return {name: {"relation": {"database_id": dbid}}}

# ---- utilities
def db_query(c: Client, database_id: str, **kwargs):
    """SDK-agnostic DB query. Use .databases.query if available; otherwise call request(path, method, body)."""
    if hasattr(c.databases, "query"):
        return c.databases.query(database_id=database_id, **kwargs)
    body = {}
    for k in ("filter","sorts","start_cursor","page_size"):
        if k in kwargs: body[k] = kwargs[k]
    # IMPORTANT: this client expects positional args, and path WITHOUT a leading slash
    return c.request(f"databases/{database_id}/query", "post", body=body)

def db_list_all(c: Client, database_id: str):
    results, cursor = [], None
    while True:
        resp = db_query(c, database_id, start_cursor=cursor) if cursor else db_query(c, database_id)
        results += resp.get("results", [])
        if not resp.get("has_more"): break
        cursor = resp.get("next_cursor")
    return results

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
        obj = c.databases.retrieve(dbid)
        return isinstance(obj, dict) and "properties" in obj
    except errors.APIResponseError:
        return False

def find_child_db_id(c, parent_page_id, candidates):
    kids=c.blocks.children.list(parent_page_id).get("results",[])
    for k in kids:
        if k.get("type")=="child_database":
            t = k["child_database"].get("title")
            if t in candidates:
                return k["id"]
    return None

def create_or_upsert_db(c, parent_page_id, candidates, props, fallback_title):
    dbid = find_child_db_id(c, parent_page_id, candidates)
    if dbid and not is_database(c, dbid):
        dbid = None
    if dbid is None:
        db = c.databases.create(
            parent={"type":"page_id","page_id":parent_page_id},
            title=[{"type":"text","text":{"content":fallback_title}}],
            properties=props
        )
        return db["id"]
    cur = c.databases.retrieve(dbid).get("properties", {})
    add_props = {k:v for k,v in props.items() if k not in cur}
    if add_props:
        c.databases.update(database_id=dbid, properties=add_props)
    return dbid

def seed_rows(c, dbid, rows):
    existing=set()
    for p in db_list_all(c, dbid):
        t = p["properties"]["Name"]["title"]
        existing.add("".join([x.get("plain_text","") for x in t]))
    for r in rows:
        if r["__title__"] in existing: continue
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
    c=Client(auth=token)
    m=json.load(open(MAP,"r",encoding=ENC)); hub=m["hub_page_id"]

    # title variants (cover en-dash, hyphen, accidental double-space)
    admin_candidates = {"Admin  Config Index", "Admin - Config Index", "Admin  Config Index"}
    admin_props = {
      **title("Name"),
      **rich("Key"), **rich("Value"),
      **select("Type", ["bool","int","float","string"]),
      **mselect("Domain", ["mirror","harness","reports"]),
      **rich("Notes")
    }
    admin_db_id = create_or_upsert_db(c, hub, admin_candidates, admin_props, "Admin  Config Index")

    seed_rows(c, admin_db_id, [
      {"__title__":"Auto-refresh enabled","Key":"mirror.auto_refresh.enabled","Value":"true","Type":"bool","Domain":"mirror","Notes":"UI auto refresh"},
      {"__title__":"Auto-refresh interval (s)","Key":"mirror.auto_refresh.interval_s","Value":"3","Type":"int","Domain":"mirror"},
      {"__title__":"Default route","Key":"harness.route.default","Value":"vwap","Type":"string","Domain":"harness"},
      {"__title__":"Replay speed","Key":"harness.replay.speed","Value":"1.0","Type":"float","Domain":"harness"},
      {"__title__":"Min run minutes","Key":"harness.runs.min_minutes","Value":"10","Type":"int","Domain":"harness"},
      {"__title__":"Daily summary enabled","Key":"reports.summary.enabled","Value":"true","Type":"bool","Domain":"reports"}
    ])

    projects_id = create_or_upsert_db(c, hub, {"Projects"}, {
      **title("Name"),
      **select("Status", ["Planned","Active","On hold","Done"]),
      **select("Priority", ["High","Medium","Low"]),
      **people("Owner"), **datep("Start"), **datep("End"),
      **mselect("Tags", ["SoT","UX","Runtime","Telemetry","DB"]),
      **rich("Description"), **relation("Workspace", root_db)
    }, "Projects")

    tasks_id = create_or_upsert_db(c, hub, {"Tasks"}, {
      **title("Name"),
      **select("Status", ["Not Started","In Progress","Blocked","Done"]),
      **select("Priority", ["High","Medium","Low"]),
      **people("Assignee"), **datep("Due"),
      **relation("Project", projects_id),
      **relation("Workspace", root_db),
      **mselect("Tags", ["SoT","UX","Runtime","Telemetry","DB"])
    }, "Tasks")

    decisions_id = create_or_upsert_db(c, hub, {"Decisions"}, {
      **title("Decision"),
      **select("Status", ["Proposed","Approved","Rejected","Changed"]),
      **datep("Date"), **people("Owner"),
      **relation("Project", projects_id),
      **relation("Workspace", root_db), **rich("Notes")
    }, "Decisions")

    approvals_id = create_or_upsert_db(c, hub, {"Approvals"}, {
      **title("Request"),
      **select("Status", ["Pending","Approved","Denied"]),
      **datep("Date"), **rich("RequestedBy"), **rich("ApprovedBy"),
      **relation("Project", projects_id),
      **relation("Decision", decisions_id),
      **relation("Workspace", root_db)
    }, "Approvals")

    handover_id = create_or_upsert_db(c, hub, {"Handover"}, {
      **title("Item"),
      **select("Area", ["Docs","ETL","Runtime","UX/SxE","QC/Telemetry"]),
      **select("Status", ["Pending","Ready","Delivered"]),
      **datep("Due"), **people("Owner"), **urlp("Link"),
      **relation("Project", projects_id),
      **relation("Workspace", root_db)
    }, "Handover")

    svp = ensure_page(c, hub, "Saved Views  Playbook")
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

    m.update({
      "admin_config_db_id":admin_db_id,
      "projects_db_id":projects_id,
      "tasks_db_id":tasks_id,
      "decisions_db_id":decisions_id,
      "approvals_db_id":approvals_id,
      "handover_db_id":handover_id,
      "saved_views_playbook_page_id":svp
    })
    pathlib.Path(OUT).write_text(json.dumps(m,indent=2), encoding=ENC)
    print("OK: Admin Config (verified) + companion DBs + Playbook created & map updated")

if __name__=="__main__":
    main()
