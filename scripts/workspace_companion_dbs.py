#!/usr/bin/env python3
import os, json, sys
from notion_client import Client

ENC="utf-8-sig"
HUB_TITLE = "Workspace (DB)  IFNS"

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

def find_page(notion, title):
    r = notion.search(query=title, filter={"value":"page","property":"object"})
    for o in r.get("results", []):
        if o.get("object")=="page" and o.get("properties",{}).get("title",{}).get("title"):
            if o["properties"]["title"]["title"][0]["plain_text"] == title:
                return o["id"]

def ensure_parent_page(notion):
    # 1) explicit env id wins
    pid = os.environ.get("IFNS_HUB_PAGE_ID")
    if pid: return pid
    # 2) try by title
    pid = find_page(notion, HUB_TITLE)
    if pid: return pid
    # 3) fail clearly (internal integrations cant create workspace-level pages)
    sys.exit("No parent page found. Set IFNS_HUB_PAGE_ID or create a page titled '%s' and rerun." % HUB_TITLE)

def ensure_companions(notion, parent_page_id):
    ids={}
    for name,spec in COMPANIONS.items():
        # reuse db if it already exists by title
        found=None
        resp = notion.search(query=name, filter={"value":"database","property":"object"})
        for o in resp.get("results", []):
            if o.get("object")=="database" and o.get("title") and o["title"][0]["plain_text"]==name:
                found=o["id"]; break
        if not found:
            created = notion.databases.create(
                parent={"type":"page_id","page_id":parent_page_id},
                title=[{"type":"text","text":{"content":name}}],
                properties=spec["properties"]
            )
            ids[name]=created["id"]
        else:
            ids[name]=found
    return ids

def main():
    token=os.environ.get("NOTION_TOKEN")
    root=os.environ.get("WORKSPACE_DB_ID") or os.environ.get("IFNS_Workspace_DB")
    assert token and root, "Set NOTION_TOKEN and WORKSPACE_DB_ID/IFNS_Workspace_DB"
    notion=Client(auth=token)

    parent_page_id = ensure_parent_page(notion)
    ids = ensure_companions(notion, parent_page_id)

    # Tasks  Projects relation (both ways)
    notion.databases.update(database_id=ids["Tasks"],    properties={"Project":{"relation":{"database_id":ids["Projects"]}}})
    notion.databases.update(database_id=ids["Projects"], properties={"Tasks":{"relation":{"database_id":ids["Tasks"]}}})

    os.makedirs("IFNS_Workspace_DB/config", exist_ok=True)
    with open("IFNS_Workspace_DB/config/workspace_companion_map.json","w",encoding=ENC) as f:
        json.dump(ids,f,indent=2)
    print("Companion DBs ready:", ids, "Parent page:", parent_page_id)

if __name__=="__main__":
    main()
