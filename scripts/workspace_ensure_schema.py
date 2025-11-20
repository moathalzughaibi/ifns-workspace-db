#!/usr/bin/env python3
import os, json
from notion_client import Client

ENC="utf-8-sig"
MAP="IFNS_Workspace_DB/config/workspace_companion_map.json"

# Canonical schema (property  Notion type); select options included where useful
CANON = {
  "Projects": {
    "Status":   {"type":"select","select":{"options":[{"name":"Planned"},{"name":"Active"},{"name":"Blocked"},{"name":"Done"}]}},
    "Owner":    {"type":"people"},
    "Due":      {"type":"date"},
    "Repo":     {"type":"url"},
    "Notes":    {"type":"rich_text"},
  },
  "Tasks": {
    "Status":   {"type":"select","select":{"options":[{"name":"Planned"},{"name":"Doing"},{"name":"Blocked"},{"name":"Done"}]}},
    "Assignee": {"type":"people"},
    "Due":      {"type":"date"},
    "Repo":     {"type":"url"},
    "Notes":    {"type":"rich_text"},
    "Project":  {"type":"relation"},  # DB id filled at runtime
  },
  "Decisions": {
    "Date":     {"type":"date"},
    "Owner":    {"type":"people"},
    "Impact":   {"type":"select","select":{"options":[{"name":"Low"},{"name":"Med"},{"name":"High"}]}},
    "Notes":    {"type":"rich_text"},
  },
  "Approvals": {
    "Object URL":{"type":"url"},
    "Action":   {"type":"select","select":{"options":[{"name":"approve"},{"name":"reject"}]}},
    "By":       {"type":"people"},
    "At":       {"type":"date"},
    "Notes":    {"type":"rich_text"},
  },
  "Handover": {
    "Status":   {"type":"select","select":{"options":[{"name":"Draft"},{"name":"In Review"},{"name":"Approved"}]}},
    "Repo":     {"type":"url"},
    "Notes":    {"type":"rich_text"},
  },
}

def ensure_schema():
    tok = os.environ.get("NOTION_TOKEN")
    if not tok:
        raise SystemExit("Missing NOTION_TOKEN")
    c = Client(auth=tok)

    with open(MAP,"r",encoding=ENC) as f:
        m = json.load(f)
    # Resolve IDs
    projects_id = m["Projects"]
    tasks_id    = m["Tasks"]

    # Prepare relation target for TasksProject
    canon_tasks = dict(CANON["Tasks"])
    canon_tasks["Project"] = {"type":"relation","relation":{"database_id":projects_id}}
    canon = dict(CANON)
    canon["Tasks"] = canon_tasks

    # Ensure each DB has all canonical props (create only missing ones)
    for name, dbid in m.items():
        if name == "hub_page_id":  # skip page id
            continue
        want = canon.get(name, {})
        if not want:
            continue

        db = c.databases.retrieve(dbid)
        existing = set((db.get("properties") or {}).keys())
        add = {}
        # soft-rename StateStatus (if present) by creating Status; user can migrate values later
        if "State" in existing and "Status" not in existing and "Status" in want:
            add["Status"] = want["Status"]

        for prop, schema in want.items():
            if prop not in existing:
                add[prop] = schema

        if add:
            c.databases.update(database_id=dbid, properties=add)
            print(f"[UPDATED] {name}: added {list(add.keys())}")
        else:
            print(f"[OK] {name}: schema already compliant")

if __name__ == "__main__":
    ensure_schema()
