#!/usr/bin/env python3
import os, json, sys
from notion_client import Client
from notion_client.errors import APIResponseError

ENC="utf-8-sig"; HUB_ROW_TITLE="Workspace (DB)  IFNS (Hub)"
COMPANIONS={
 "Projects":{"properties":{"Name":{"title":{}},"State":{"select":{"options":[{"name":"Planned"},{"name":"Active"},{"name":"Blocked"},{"name":"Done"}]}},
  "Owner":{"people":{}},"Due":{"date":{}},"Repo":{"url":{}},"Notes":{"rich_text":{}}}},
 "Tasks":{"properties":{"Name":{"title":{}},"State":{"select":{"options":[{"name":"Planned"},{"name":"Doing"},{"name":"Blocked"},{"name":"Done"}]}},
  "Assignee":{"people":{}},"Due":{"date":{}},"Repo":{"url":{}},"Notes":{"rich_text":{}}}},
 "Decisions":{"properties":{"Name":{"title":{}},"Project":{"rich_text":{}},"Date":{"date":{}},"Owner":{"people":{}},"Impact":{"select":{"options":[{"name":"Low"},{"name":"Med"},{"name":"High"}]}},
  "Notes":{"rich_text":{}}}},
 "Approvals":{"properties":{"Name":{"title":{}},"Object URL":{"url":{}},"Action":{"select":{"options":[{"name":"approve"},{"name":"reject"}]}},
  "By":{"people":{}},"At":{"date":{}},"Notes":{"rich_text":{}}}},
 "Handover":{"properties":{"Name":{"title":{}},"State":{"select":{"options":[{"name":"Draft"},{"name":"In Review"},{"name":"Approved"}]}},
  "Repo":{"url":{}},"Notes":{"rich_text":{}}}}
}

def title_prop_key(db):
    try:
        for k,p in db.get("properties",{}).items():
            if p.get("type")=="title": return k
    except Exception: pass
    return "Name"

def find_or_create_hub_page(notion, db_id):
    db = notion.databases.retrieve(db_id)
    tkey = title_prop_key(db)
    try:
        if hasattr(notion.databases,"query"):
            q = notion.databases.query(database_id=db_id, filter={"property":tkey,"title":{"equals":HUB_ROW_TITLE}})
            if q.get("results"): return q["results"][0]["id"]
    except Exception: pass
    row = notion.pages.create(parent={"database_id":db_id},
        properties={tkey: {"title":[{"type":"text","text":{"content":HUB_ROW_TITLE}}]}})
    return row["id"]

def create_companions(notion, parent_page_id):
    ids={}
    for name,spec in COMPANIONS.items():
        created = notion.databases.create(parent={"type":"page_id","page_id":parent_page_id},
            title=[{"type":"text","text":{"content":name}}], properties=spec["properties"])
        ids[name]=created["id"]
    return ids

def add_relations(notion, ids):
    try:
        notion.databases.update(database_id=ids["Tasks"],    properties={"Project":{"relation":{"database_id":ids["Projects"]}}})
        notion.databases.update(database_id=ids["Projects"], properties={"Tasks":{"relation":{"database_id":ids["Tasks"]}}})
    except Exception: pass

def main():
    token=os.environ.get("NOTION_TOKEN")
    root=os.environ.get("WORKSPACE_DB_ID") or os.environ.get("IFNS_Workspace_DB")
    assert token and root, "Missing NOTION_TOKEN or WORKSPACE_DB_ID/IFNS_Workspace_DB"
    notion=Client(auth=token)
    hub = find_or_create_hub_page(notion, root)
    ids = create_companions(notion, hub); add_relations(notion, ids)
    os.makedirs("IFNS_Workspace_DB/config",exist_ok=True)
    with open("IFNS_Workspace_DB/config/workspace_companion_map.json","w",encoding=ENC) as f:
        json.dump({"hub_page_id":hub, **ids}, f, indent=2)
    print("Hub page:", hub); print("Companion DBs:", ids)

if __name__=="__main__": main()
