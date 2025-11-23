#!/usr/bin/env python3
# scripts/seed_admin_defaults.py
import os
import json
from notion_client import Client

ENC = "utf-8-sig"
MAP = r"IFNS_Workspace_DB/config/workspace_companion_map.json"

DEFAULTS = [
    (
        "mirror.auto_refresh.enabled",
        "true",
        "bool",
        "mirror",
        "Auto-refresh in Awareness Mirror",
    ),
    (
        "mirror.auto_refresh.interval_s",
        "3",
        "number",
        "mirror",
        "Mirror refresh interval (s)",
    ),
    ("harness.route.default", "vwap", "text", "harness", "Default execution route"),
    ("harness.replay.speed", "1.0", "number", "harness", "Replay speed multiplier"),
    ("harness.runs.min_minutes", "10", "number", "harness", "Minimum demo run minutes"),
    ("reports.summary.enabled", "true", "bool", "reports", "Emit daily summary NDJSON"),
]


def main():
    tok = os.getenv("NOTION_TOKEN")
    assert tok, "NOTION_TOKEN missing"
    c = Client(auth=tok)
    m = json.load(open(MAP, encoding=ENC))
    dbid = m["Admin_Config_Index"]

    # Ensure schema (Name title already exists)
    props = {
        "Value": {"rich_text": {}},
        "Type": {
            "select": {
                "options": [{"name": "bool"}, {"name": "number"}, {"name": "text"}]
            }
        },
        "Scope": {
            "select": {
                "options": [
                    {"name": "mirror"},
                    {"name": "harness"},
                    {"name": "reports"},
                ]
            }
        },
        "Notes": {"rich_text": {}},
    }
    c.databases.update(database_id=dbid, properties=props)

    # helper: find page by Name
    def find(name):
        q = c.databases.query(
            database_id=dbid, filter={"property": "Name", "title": {"equals": name}}
        )
        return q["results"][0]["id"] if q["results"] else None

    for name, val, typ, scope, notes in DEFAULTS:
        pid = find(name)
        data = {
            "parent": {"type": "database_id", "database_id": dbid},
            "properties": {
                "Name": {"title": [{"type": "text", "text": {"content": name}}]},
                "Value": {"rich_text": [{"type": "text", "text": {"content": val}}]},
                "Type": {"select": {"name": typ}},
                "Scope": {"select": {"name": scope}},
                "Notes": {"rich_text": [{"type": "text", "text": {"content": notes}}]},
            },
        }
        if pid:
            c.pages.update(page_id=pid, properties=data["properties"])
            print("updated:", name)
        else:
            c.pages.create(**data)
            print("created:", name)

    print("Admin defaults: OK")


if __name__ == "__main__":
    main()
