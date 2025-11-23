#!/usr/bin/env python3
import os
import json
from notion_client import Client

ENC = "utf-8-sig"
MAP = "IFNS_Workspace_DB/config/workspace_companion_map.json"

DEFAULTS = [
    (
        "mirror.auto_refresh.enabled",
        "mirror",
        "boolean",
        "true",
        "true",
        "global",
        "Mirror autorefresh toggle",
    ),
    (
        "mirror.auto_refresh.interval_s",
        "mirror",
        "number",
        "3",
        "3",
        "global",
        "Auto refresh interval (s)",
    ),
    (
        "harness.route.default",
        "harness",
        "string",
        "vwap",
        "vwap",
        "global",
        "Default execution route",
    ),
    (
        "harness.replay.speed",
        "harness",
        "number",
        "1.0",
        "1.0",
        "demo",
        "Time-scale multiplier",
    ),
    (
        "harness.runs.min_minutes",
        "harness",
        "number",
        "10",
        "10",
        "global",
        "Minimum run length (minutes)",
    ),
    (
        "reports.summary.enabled",
        "reports",
        "boolean",
        "true",
        "true",
        "global",
        "Emit daily summary files",
    ),
]


def t(s):
    return [{"type": "text", "text": {"content": s}}]


def main():
    c = Client(auth=os.environ["NOTION_TOKEN"])
    m = json.load(open(MAP, "r", encoding=ENC))
    hub = m["hub_page_id"]

    # Create DB
    db = c.databases.create(
        parent={"type": "page_id", "page_id": hub},
        title=[{"type": "text", "text": {"content": "Admin Config Index"}}],
        properties={
            "Key": {"title": {}},
            "Group": {
                "select": {
                    "options": [
                        {"name": "mirror"},
                        {"name": "harness"},
                        {"name": "reports"},
                        {"name": "ml"},
                        {"name": "exec"},
                        {"name": "runtime"},
                    ]
                }
            },
            "Type": {
                "select": {
                    "options": [
                        {"name": "string"},
                        {"name": "number"},
                        {"name": "boolean"},
                    ]
                }
            },
            "Value": {"rich_text": {}},
            "Default": {"rich_text": {}},
            "Scope": {
                "select": {
                    "options": [
                        {"name": "global"},
                        {"name": "dev"},
                        {"name": "prod"},
                        {"name": "demo"},
                    ]
                }
            },
            "Notes": {"rich_text": {}},
            "Last_Updated": {"date": {}},
        },
    )
    cfg_id = db["id"]

    # Update map so exporter will include it
    m["Admin_Config_Index"] = cfg_id
    os.makedirs(os.path.dirname(MAP), exist_ok=True)
    json.dump(m, open(MAP, "w", encoding=ENC), indent=2)

    # Seed defaults
    for key, group, typ, val, dflt, scope, notes in DEFAULTS:
        c.pages.create(
            parent={"database_id": cfg_id},
            properties={
                "Key": {"title": t(key)},
                "Group": {"select": {"name": group}},
                "Type": {"select": {"name": typ}},
                "Value": {"rich_text": t(val)},
                "Default": {"rich_text": t(dflt)},
                "Scope": {"select": {"name": scope}},
                "Notes": {"rich_text": t(notes)},
            },
        )
    print("Admin Config Index created + seeded.")


if __name__ == "__main__":
    main()
