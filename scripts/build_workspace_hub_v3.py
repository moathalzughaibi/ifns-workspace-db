#!/usr/bin/env python3
import os
import json
import pathlib
import sys
from notion_client import Client, errors

ENC = "utf-8-sig"
MAP = pathlib.Path("IFNS_Workspace_DB/config/workspace_companion_map.json")
MAP.parent.mkdir(parents=True, exist_ok=True)


def load_map():
    return json.loads(MAP.read_text(encoding=ENC)) if MAP.exists() else {}


def save_map(m):
    MAP.write_text(json.dumps(m, indent=2), encoding=ENC)


def apiprint(e: Exception):
    if isinstance(e, errors.APIResponseError):
        print(
            "APIResponseError:",
            e.code,
            getattr(e, "message", ""),
            getattr(e, "body", ""),
            file=sys.stderr,
        )
    else:
        print("Exception:", repr(e), file=sys.stderr)


# props helpers
def t(n):
    return {n: {"title": {}}}


def rt(n):
    return {n: {"rich_text": {}}}


def sel(n, ops):
    return {n: {"select": {"options": [{"name": o} for o in ops]}}}


def msel(n, ops):
    return {n: {"multi_select": {"options": [{"name": o} for o in ops]}}}


def dt(n):
    return {n: {"date": {}}}


def urlp(n):
    return {n: {"url": {}}}


def ppl(n):
    return {n: {"people": {}}}


def rel(n, db):
    return {n: {"relation": {"database_id": db}}}


def ensure_hub(c, hub_id=None):
    if hub_id:
        try:
            if c.pages.retrieve(hub_id).get("object") == "page":
                return hub_id
        except errors.APIResponseError:
            pass
    # create at workspace root
    p = c.pages.create(
        parent={"type": "workspace", "workspace": True},
        properties={
            "title": {
                "title": [
                    {"type": "text", "text": {"content": "IFNS_Workspace_DB - Hub"}}
                ]
            }
        },
    )
    return p["id"]


def ensure_child_page(c, parent_page_id, title):
    # reuse if exists
    kids = c.blocks.children.list(parent_page_id).get("results", [])
    for k in kids:
        if k.get("type") == "child_page" and k["child_page"].get("title") == title:
            return k["id"]
    p = c.pages.create(
        parent={"type": "page_id", "page_id": parent_page_id},
        properties={"title": {"title": [{"type": "text", "text": {"content": title}}]}},
    )
    return p["id"]


def create_db_under(c, parent_page_id, title, props):
    # return (dbid, None) or (None, exception)
    try:
        d = c.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            title=[{"type": "text", "text": {"content": title}}],
            properties=props,
        )
        if d.get("object") == "database" and "properties" in d:
            return d["id"], None
        return None, RuntimeError(f"Unexpected Notion response for {title}")
    except Exception as e:
        return None, e


def seed_admin(c, dbid):
    rows = [
        (
            "Auto-refresh enabled",
            "mirror.auto_refresh.enabled",
            "true",
            "bool",
            ["mirror"],
            "UI auto refresh",
        ),
        (
            "Auto-refresh interval (s)",
            "mirror.auto_refresh.interval_s",
            "3",
            "int",
            ["mirror"],
            "",
        ),
        ("Default route", "harness.route.default", "vwap", "string", ["harness"], ""),
        ("Replay speed", "harness.replay.speed", "1.0", "float", ["harness"], ""),
        ("Min run minutes", "harness.runs.min_minutes", "10", "int", ["harness"], ""),
        (
            "Daily summary enabled",
            "reports.summary.enabled",
            "true",
            "bool",
            ["reports"],
            "",
        ),
    ]
    for name, key, val, typ, dom, notes in rows:
        c.pages.create(
            parent={"type": "database_id", "database_id": dbid},
            properties={
                "Name": {"title": [{"type": "text", "text": {"content": name}}]},
                "Key": {"rich_text": [{"type": "text", "text": {"content": key}}]},
                "Value": {"rich_text": [{"type": "text", "text": {"content": val}}]},
                "Type": {"select": {"name": typ}},
                "Domain": {"multi_select": [{"name": d} for d in dom]},
                **(
                    {
                        "Notes": {
                            "rich_text": [{"type": "text", "text": {"content": notes}}]
                        }
                    }
                    if notes
                    else {}
                ),
            },
        )


def main():
    token = os.getenv("NOTION_TOKEN")
    root_db = os.getenv("WORKSPACE_DB_ID")
    if not token or not root_db:
        print("Missing NOTION_TOKEN or WORKSPACE_DB_ID", file=sys.stderr)
        sys.exit(2)
    c = Client(auth=token)
    m = load_map()

    # 1) hub
    hub = ensure_hub(c, m.get("hub_page_id"))
    m["hub_page_id"] = hub
    # 2) host child page (SoT DBs)
    host = ensure_child_page(c, hub, "SoT DBs")
    # assert both are pages
    assert c.pages.retrieve(hub)["object"] == "page", "Hub is not a page"
    assert c.pages.retrieve(host)["object"] == "page", "Host is not a page"

    # 3) Try create Admin DB under host; if fails, retry under hub
    admin_props = {
        **t("Name"),
        **rt("Key"),
        **rt("Value"),
        **sel("Type", ["bool", "int", "float", "string"]),
        **msel("Domain", ["mirror", "harness", "reports"]),
        **rt("Notes"),
    }
    admin_id, err = create_db_under(c, host, "Admin - Config Index (SoT)", admin_props)
    if err:
        apiprint(err)
        print("Retrying Admin DB under Hub ...", file=sys.stderr)
        admin_id, err = create_db_under(
            c, hub, "Admin - Config Index (SoT)", admin_props
        )
        if err:
            apiprint(err)
            sys.exit(3)
    seed_admin(c, admin_id)

    # 4) Create the companion DBs (prefer host; fallback to hub if needed)
    def mk(title, props):
        dbid, e = create_db_under(c, host, title, props)
        if e:
            apiprint(e)
            print(f"Retrying {title} under Hub ...", file=sys.stderr)
            dbid, e = create_db_under(c, hub, title, props)
            if e:
                apiprint(e)
                sys.exit(4)
        return dbid

    projects_id = mk(
        "Projects (SoT)",
        {
            **t("Name"),
            **sel("Status", ["Planned", "Active", "On hold", "Done"]),
            **sel("Priority", ["High", "Medium", "Low"]),
            **ppl("Owner"),
            **dt("Start"),
            **dt("End"),
            **msel("Tags", ["SoT", "UX", "Runtime", "Telemetry", "DB"]),
            **rt("Description"),
            **rel("Workspace", root_db),
        },
    )

    tasks_id = mk(
        "Tasks (SoT)",
        {
            **t("Name"),
            **sel("Status", ["Not Started", "In Progress", "Blocked", "Done"]),
            **sel("Priority", ["High", "Medium", "Low"]),
            **ppl("Assignee"),
            **dt("Due"),
            **rel("Project", projects_id),
            **rel("Workspace", root_db),
            **msel("Tags", ["SoT", "UX", "Runtime", "Telemetry", "DB"]),
        },
    )

    decisions_id = mk(
        "Decisions (SoT)",
        {
            **t("Decision"),
            **sel("Status", ["Proposed", "Approved", "Rejected", "Changed"]),
            **dt("Date"),
            **ppl("Owner"),
            **rel("Project", projects_id),
            **rel("Workspace", root_db),
            **rt("Notes"),
        },
    )

    approvals_id = mk(
        "Approvals (SoT)",
        {
            **t("Request"),
            **sel("Status", ["Pending", "Approved", "Denied"]),
            **dt("Date"),
            **rt("RequestedBy"),
            **rt("ApprovedBy"),
            **rel("Project", projects_id),
            **rel("Decision", decisions_id),
            **rel("Workspace", root_db),
        },
    )

    handover_id = mk(
        "Handover (SoT)",
        {
            **t("Item"),
            **sel("Area", ["Docs", "ETL", "Runtime", "UX/SxE", "QC/Telemetry"]),
            **sel("Status", ["Pending", "Ready", "Delivered"]),
            **dt("Due"),
            **ppl("Owner"),
            **urlp("Link"),
            **rel("Project", projects_id),
            **rel("Workspace", root_db),
        },
    )

    # 5) Save map and print
    m.update(
        {
            "db_host_page_id": host,
            "admin_config_db_id": admin_id,
            "projects_db_id": projects_id,
            "tasks_db_id": tasks_id,
            "decisions_db_id": decisions_id,
            "approvals_db_id": approvals_id,
            "handover_db_id": handover_id,
        }
    )
    save_map(m)
    print("DONE")
    print("hub:", hub)
    print("host:", host)
    print("admin:", admin_id)
    print("projects:", projects_id)
    print("tasks:", tasks_id)
    print("decisions:", decisions_id)
    print("approvals:", approvals_id)
    print("handover:", handover_id)


if __name__ == "__main__":
    main()
