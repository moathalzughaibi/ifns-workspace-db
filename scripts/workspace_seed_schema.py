#!/usr/bin/env python3
import os, datetime
from notion_client import Client

def get_db(notion, dbid):
    return notion.databases.retrieve(dbid)

def title_prop_key(db):
    for k, p in db["properties"].items():
        if p.get("type") == "title":
            return k
    return "Name"  # fallback

def ensure_schema(notion, dbid):
    # Add handy properties (idempotent)
    notion.databases.update(
        database_id=dbid,
        properties={
            "Status":      {"status": {}},
            "Owner":       {"people": {}},
            "Due":         {"date": {}},
            "Type":        {"select": {}},
            "Repo Path":   {"url": {}},
            "Notes":       {"rich_text": {}}
        }
    )

def upsert_sample_rows(notion, dbid, title_key):
    # Create 2 example rows if DB is empty
    cur = notion.databases.query(database_id=dbid)
    if len(cur.get("results", [])) > 0:
        print("Rows already exist; skipping seed.")
        return

    today = datetime.date.today().isoformat()
    samples = [
        {
            title_key: {"title": [{"type":"text","text":{"content":"Workspace bootstrap"}}]},
            "Status":  {"status": {"name":"In Review"}},
            "Type":    {"select": {"name":"Setup"}},
            "Due":     {"date": {"start": today}},
            "Repo Path": {"url":"https://github.com/moathalzughaibi/ifns-workspace-db"},
            "Notes":   {"rich_text":[{"type":"text","text":{"content":"Initial DB schema + exporter smoke."}}]}
        },
        {
            title_key: {"title": [{"type":"text","text":{"content":"Add Projects/Tasks DBs"}}]},
            "Status":  {"status": {"name":"Planned"}},
            "Type":    {"select": {"name":"Design"}},
            "Notes":   {"rich_text":[{"type":"text","text":{"content":"Next: Projects, Tasks, Decisions, Approvals, Handover."}}]}
        }
    ]
    for props in samples:
        notion.pages.create(parent={"database_id": dbid}, properties=props)
    print("Seeded 2 sample rows.")

def main():
    token = os.environ.get("NOTION_TOKEN")
    dbid  = os.environ.get("WORKSPACE_DB_ID") or os.environ.get("IFNS_Workspace_DB")
    assert token and dbid, "Missing NOTION_TOKEN or WORKSPACE_DB_ID/IFNS_Workspace_DB"
    notion = Client(auth=token)

    db = get_db(notion, dbid)
    tkey = title_prop_key(db)
    ensure_schema(notion, dbid)
    upsert_sample_rows(notion, dbid, tkey)
    print("Schema ensured and seed done.")

if __name__ == "__main__":
    main()
