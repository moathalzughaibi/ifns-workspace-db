#!/usr/bin/env python3
import os, json, sys
from notion_client import Client
from notion_client.errors import APIResponseError

ENC="utf-8-sig"
HUB_ROW_TITLE = "Workspace (DB)  IFNS (Hub)"

COMPANIONS = {
  "Projects":{"properties":{"Name":{"title":{}},"State":{"select":{"options":[{"name":"Planned"},{"name":"Active"},{"name":"Blocked"},{"name":"Done"}]}},
                            "Owner":{"people":{}},"Due":{"date":{}},"Repo":{"url":{}},"Notes":{"rich_text":{}}}},
  "Tasks":{"properties":{"Name":{"title":{}},"State":{"select":{"options":[{"name":"Planned"},{"name":"Doing"},{"name":"Blocked"},{"name":"Done"}]}},
                         "Assignee":{"people":{}},"Due":{"date":{}},"Repo":{"url":{}},"Notes":{"rich_text":{}}}},
  "Decisions":{"properties":{"Name":{"title":{}},"Project":{"rich_text":{}},"Date":{"date":{}},"Owner":{"people":{}},
                             "Impact":{"select":{"options":[{"name":"Low"},{"name":"Med"},{"name":"High"}]}},"Notes":{"rich_text":{}}}},
  "Approvals":{"properties":{"Name":{"title":{}},"Object URL":{"url":{}},"Action":{"select":{"options":[{"name":"approve"},{"name":"reject"}]}},
                             "By":{"people":{}},"At":{"date":{}},"Notes":{"rich_text":{}}}},
  "Handover":{"properties":{"Name":{"title":{}},"State":{"select":{"options":[{"name":"Draft"},{"name":"In Review"},{"name":"Approved"}]}},
                            "Repo":{"url":{}},"Notes":{"rich_text":{}}}}
}

def find_title_prop_key(db):
    for k,p in db["properties"].items():
        if p.get("type")=="title": return k
    return "Name"

def find_or_create_hub_page(notion, db_id):
    db = notion.databases.retrieve(db_id)
    title_prop = find_title_prop_key(db)

    # try to find existing row titled HUB_ROW_TITLE
    try:
        r = notion.databases.query(database_id=db_id, filter={"property":title_prop, "title":{"equals":HUB_ROW_TITLE}})
        if r.get("results"):
            return r["results"][0]["id"]
    except APIResponseError:
        pass

    # create a new row (page) inside the database to serve as the hub
    row = notion.pages.create(parent={"database_id": db_id},
                              properties={title_prop: {"title":[{"type":"text","text":{"content":HUB_ROW_TITLE}}]}})
    return row["id"]

def create_companions_under_page(notion, parent_page_id):
    ids={}
    for name, spec in COMPANIONS.items():
        created = notion.databases.create(parent={"type":"page_id","page_id":parent_page_id},
                                          title=[{"type":"text","text":{"content":name}}],
                                          properties=spec["properties"])
        ids[name] = created["id"]
    return ids

def add_relations(notion, ids):
    # Tasks  Projects
    notion.databases.update(database_id=ids["Tasks"],    properties={"Project":{"relation":{"database_id":ids["Projects"]}}})
    notion.databases.update(database_id=ids["Projects"], properties={"Tasks":{"relation":{"database_id":ids["Tasks"]}}})

def main():
    token = os.environ.get("NOTION_TOKEN")
    root_db = os.environ.get("WORKSPACE_DB_ID") or os.environ.get("IFNS_Workspace_DB")
    assert token and root_db, "Set NOTION_TOKEN and WORKSPACE_DB_ID/IFNS_Workspace_DB"
    notion = Client(auth=token)

    hub_page_id = find_or_create_hub_page(notion, root_db)
    ids = create_companions_under_page(notion, hub_page_id)
    add_relations(notion, ids)

    os.makedirs("IFNS_Workspace_DB/config", exist_ok=True)
    with open("IFNS_Workspace_DB/config/workspace_companion_map.json","w",encoding=ENC) as f:
        json.dump({"hub_page_id": hub_page_id, **ids}, f, indent=2)

    print("Hub page:", hub_page_id)
    print("Companion DBs:", ids)

if __name__=="__main__":
    main()
