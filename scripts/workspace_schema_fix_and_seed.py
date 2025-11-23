#!/usr/bin/env python3
import os
import datetime
from notion_client import Client
from notion_client.errors import APIResponseError


def title_key(db):
    for k, p in db["properties"].items():
        if p.get("type") == "title":
            return k
    return "Name"


def ensure_status_like(notion, dbid):
    db = notion.databases.retrieve(dbid)
    props = db["properties"].keys()

    # If "Status" already exists, use it
    if "Status" in props:
        return ("Status", "status")

    # Try to add a real Status (status type). If Notion rejects, add "State" (select).
    try:
        notion.databases.update(
            database_id=dbid,
            properties={
                "Status": {
                    "status": {
                        "options": [
                            {"name": "Planned"},
                            {"name": "In Review"},
                            {"name": "Approved"},
                            {"name": "Done"},
                        ]
                    }
                }
            },
        )
        return ("Status", "status")
    except APIResponseError:
        pass

    notion.databases.update(
        database_id=dbid,
        properties={
            "State": {
                "select": {
                    "options": [
                        {"name": "Planned"},
                        {"name": "In Review"},
                        {"name": "Approved"},
                        {"name": "Done"},
                    ]
                }
            }
        },
    )
    return ("State", "select")


def ensure_other_props(notion, dbid):
    notion.databases.update(
        database_id=dbid,
        properties={
            "Owner": {"people": {}},
            "Due": {"date": {}},
            "Type": {"select": {}},
            "Repo Path": {"url": {}},
            "Notes": {"rich_text": {}},
        },
    )


def upsert_seed(notion, dbid, title_prop, status_prop_name):
    # Only seed if DB has no rows
    cur = notion.databases.query(database_id=dbid)
    if cur.get("results"):
        return
    today = datetime.date.today().isoformat()
    samples = [
        {
            title_prop: {
                "title": [{"type": "text", "text": {"content": "Workspace bootstrap"}}]
            },
            status_prop_name: (
                {"status": {"name": "In Review"}}
                if status_prop_name == "Status"
                else {"select": {"name": "In Review"}}
            ),
            "Type": {"select": {"name": "Setup"}},
            "Due": {"date": {"start": today}},
            "Repo Path": {
                "url": "https://github.com/moathalzughaibi/ifns-workspace-db"
            },
            "Notes": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "Initial DB schema + exporter smoke."},
                    }
                ]
            },
        },
        {
            title_prop: {
                "title": [
                    {"type": "text", "text": {"content": "Add Projects/Tasks DBs"}}
                ]
            },
            status_prop_name: (
                {"status": {"name": "Planned"}}
                if status_prop_name == "Status"
                else {"select": {"name": "Planned"}}
            ),
            "Type": {"select": {"name": "Design"}},
            "Notes": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Next: Projects, Tasks, Decisions, Approvals, Handover."
                        },
                    }
                ]
            },
        },
    ]
    for props in samples:
        notion.pages.create(parent={"database_id": dbid}, properties=props)


def main():
    token = os.environ.get("NOTION_TOKEN")
    dbid = os.environ.get("WORKSPACE_DB_ID") or os.environ.get("IFNS_Workspace_DB")
    assert token and dbid, "Set NOTION_TOKEN and WORKSPACE_DB_ID/IFNS_Workspace_DB"
    notion = Client(auth=token)

    db = notion.databases.retrieve(dbid)
    tkey = title_key(db)
    status_name, kind = ensure_status_like(notion, dbid)
    ensure_other_props(notion, dbid)
    upsert_seed(notion, dbid, tkey, status_name)
    print(f"Schema ensured. Using '{status_name}' ({kind}). Seed done.")


if __name__ == "__main__":
    main()
