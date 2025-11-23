#!/usr/bin/env python3
# scripts/build_workspace_hub_v4.py
import os
import json
import sys
from notion_client import Client, errors

ENC = "utf-8-sig"
MAP = r"IFNS_Workspace_DB/config/workspace_companion_map.json"


def fail(msg):
    print("ERROR:", msg, file=sys.stderr)
    sys.exit(2)


def client():
    tok = os.getenv("NOTION_TOKEN")
    root = os.getenv("WORKSPACE_DB_ID")
    if not tok or not root:
        fail("Missing NOTION_TOKEN / WORKSPACE_DB_ID")
    return Client(auth=tok), root


def load_map():
    try:
        return json.load(open(MAP, encoding=ENC))
    except FileNotFoundError:
        return {}
    except Exception as e:
        fail(f"map read failed: {e!r}")


def save_map(m):
    os.makedirs(os.path.dirname(MAP), exist_ok=True)
    with open(MAP, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2)


def list_children(c, pid):
    # return {title: (id, type)} for child_page + child_database
    out = {}
    cur = None
    while True:
        resp = (
            c.blocks.children.list(pid, start_cursor=cur)
            if cur
            else c.blocks.children.list(pid)
        )
        for b in resp.get("results", []):
            t = b.get("type")
            if t == "child_page":
                out[b["child_page"]["title"]] = (b["id"], t)
            if t == "child_database":
                out[b["child_database"]["title"]] = (b["id"], t)
        cur = resp.get("next_cursor")
        if not resp.get("has_more"):
            break
    return out


def ensure_page(c, parent_pid, title):
    kids = list_children(c, parent_pid)
    if title in kids and kids[title][1] == "child_page":
        return kids[title][0]
    p = c.pages.create(
        parent={"type": "page_id", "page_id": parent_pid},
        properties={"title": {"title": [{"type": "text", "text": {"content": title}}]}},
    )
    return p["id"]


def ensure_db(c, parent_pid, title, root_db_id):
    kids = list_children(c, parent_pid)
    if title in kids and kids[title][1] == "child_database":
        return kids[title][0], False
    props = {
        "Name": {"title": {}},
        "Workspace": {
            "type": "relation",
            "relation": {
                "database_id": root_db_id,
                "type": "single_property",
                "single_property": {},
            },
        },
    }
    db = c.databases.create(
        parent={"type": "page_id", "page_id": parent_pid},
        title=[{"type": "text", "text": {"content": title}}],
        properties=props,
    )
    return db["id"], True


def ensure_workspace_relation(c, dbid, root_db_id):
    # try new, legacy, dual in order (be lenient)
    payloads = [
        {
            "Workspace": {
                "type": "relation",
                "relation": {
                    "database_id": root_db_id,
                    "type": "single_property",
                    "single_property": {},
                },
            }
        },
        {"Workspace": {"relation": {"database_id": root_db_id}}},
        {
            "Workspace": {
                "type": "relation",
                "relation": {
                    "database_id": root_db_id,
                    "type": "dual_property",
                    "dual_property": {},
                },
            }
        },
    ]
    for props in payloads:
        try:
            c.databases.update(database_id=dbid, properties=props)
            return True
        except errors.APIResponseError:
            continue
    return False


def main():
    c, root = client()
    m = load_map()
    hub = m.get("hub_page_id")
    if not hub:
        fail("hub_page_id missing in map (run v3 once to create Hub)")

    # host page for SoT DBs
    host = m.get("db_host_page_id")
    if not host:
        host = ensure_page(c, hub, "SoT DBs")
        m["db_host_page_id"] = host
        save_map(m)

    for key, title in [
        ("Admin_Config_Index", "Admin - Config Index (SoT)"),
        ("Projects", "Projects (SoT)"),
        ("Tasks", "Tasks (SoT)"),
        ("Decisions", "Decisions (SoT)"),
        ("Approvals", "Approvals (SoT)"),
        ("Handover", "Handover (SoT)"),
    ]:
        dbid = m.get(key)
        created = False
        if not dbid:
            dbid, created = ensure_db(c, host, title, root)
        # always normalize relation
        ensure_workspace_relation(c, dbid, root)
        m[key] = dbid
        print(("created " if created else "ok "), title, "", dbid)

    save_map(m)
    print("hub v4: PASS (idempotent)")


if __name__ == "__main__":
    main()
