#!/usr/bin/env python3
import os
import json
import datetime
from notion_client import Client

ENC = "utf-8-sig"
MAP = r"IFNS_Workspace_DB/config/workspace_companion_map.json"

SEED = [
    {"Name": "Workspace Root DB", "Category": "ids", "Value": "$WORKSPACE_DB_ID"},
    {
        "Name": "Naming  Steps",
        "Category": "naming",
        "Value": "Step NN  <token>; 01  Narrative & Intent; NN.k – Section k",
    },
    {
        "Name": "SLA  Approvals",
        "Category": "sla",
        "Value": "Target 48h pending  breach",
    },
    {
        "Name": "Export  Mirror Path",
        "Category": "mirror",
        "Value": "sync/workspace/*.csv",
    },
]


def ensure_props(c, dbid):
    db = c.databases.retrieve(dbid)
    props = db.get("properties", {})
    need = {}
    if "Category" not in props:
        need["Category"] = {"type": "select", "select": {}}
    if "Updated" not in props:
        need["Updated"] = {"type": "date", "date": {}}
    if need:
        c.databases.update(database_id=dbid, properties=need)


def main():
    tok = os.getenv("NOTION_TOKEN")
    root = os.getenv("WORKSPACE_DB_ID")
    assert tok and root, "Missing NOTION_TOKEN / WORKSPACE_DB_ID"
    c = Client(auth=tok)
    m = json.load(open(MAP, encoding=ENC))
    db = m["Admin_Config_Index"]

    ensure_props(c, db)

    for row in SEED:
        props = {
            "Name": {"title": [{"type": "text", "text": {"content": row["Name"]}}]},
            "Category": {"select": {"name": row["Category"]}},
            "Value": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": row["Value"].replace("$WORKSPACE_DB_ID", root)
                        },
                    }
                ]
            },
            "Updated": {"date": {"start": datetime.date.today().isoformat()}},
        }
        c.pages.create(
            parent={"type": "database_id", "database_id": db}, properties=props
        )
        print("seeded:", row["Name"])
    print("done")


if __name__ == "__main__":
    main()
