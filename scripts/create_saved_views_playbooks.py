#!/usr/bin/env python3
import os
import json
from notion_client import Client

ENC = "utf-8-sig"
MAP = r"IFNS_Workspace_DB/config/workspace_companion_map.json"

TIPS = {
    "Projects (SoT)": [
        "- By Status: Open  In Progress  Done",
        "- By Owner: Group by Assignee",
        "- By Step: Filter to a specific Step nn",
        "- Overdue: Due date < Today AND Status != Done",
    ],
    "Tasks (SoT)": [
        "- My Open: Assignee = me AND Status  {Open, In Progress}",
        "- This Week: Due within 7 days",
        "- By Project: Group by Project relation",
    ],
    "Decisions (SoT)": [
        "- Open: Status = Open",
        "- Approved / Rejected: Status  {Approved, Rejected}",
        "- By Step: Group by Step",
    ],
    "Approvals (SoT)": [
        "- Pending: Status = Pending",
        "- SLA breach: Pending and Requested > 48h",
        "- By Requester",
    ],
    "Handover (SoT)": [
        "- Active: Status  {Preparing, In Transfer}",
        "- Completed",
        "- By Receiver",
    ],
    "Admin - Config Index (SoT)": [
        "- All Config Items",
        "- By Category (runtime, naming, sla, ids)",
    ],
}


def find_child_page(c, parent_id, title):
    cursor = None
    while True:
        resp = (
            c.blocks.children.list(parent_id, start_cursor=cursor)
            if cursor
            else c.blocks.children.list(parent_id)
        )
        for b in resp.get("results", []):
            if b["type"] == "child_page" and b["child_page"]["title"] == title:
                return b["id"]
        cursor = resp.get("next_cursor")
        if not resp.get("has_more"):
            return None


def ensure_child_page(c, parent_id, title):
    pid = find_child_page(c, parent_id, title)
    if pid:
        return pid
    p = c.pages.create(
        parent={"type": "page_id", "page_id": parent_id},
        properties={"title": {"title": [{"type": "text", "text": {"content": title}}]}},
    )
    return p["id"]


def wipe_children(c, page_id):
    cur = None
    ids = []
    while True:
        resp = (
            c.blocks.children.list(page_id, start_cursor=cur)
            if cur
            else c.blocks.children.list(page_id)
        )
        ids += [b["id"] for b in resp.get("results", [])]
        cur = resp.get("next_cursor")
        if not resp.get("has_more"):
            break
    for bid in ids:
        c.blocks.delete(bid)


def main():
    tok = os.getenv("NOTION_TOKEN")
    assert tok, "NOTION_TOKEN missing"
    c = Client(auth=tok)
    m = json.load(open(MAP, encoding=ENC))
    hub = m["hub_page_id"]

    titles = [
        ("Admin - Config Index (SoT)", m["Admin_Config_Index"]),
        ("Projects (SoT)", m["Projects"]),
        ("Tasks (SoT)", m["Tasks"]),
        ("Decisions (SoT)", m["Decisions"]),
        ("Approvals (SoT)", m["Approvals"]),
        ("Handover (SoT)", m["Handover"]),
    ]

    host = find_child_page(c, hub, "Saved Views Playbooks")
    if not host:
        host = ensure_child_page(c, hub, "Saved Views Playbooks")

    for title, dbid in titles:
        page_title = f"{title}  Saved Views Playbook"
        pid = ensure_child_page(c, host, page_title)
        wipe_children(c, pid)

        link_block = {
            "object": "block",
            "type": "link_to_page",
            "link_to_page": {"type": "database_id", "database_id": dbid},
        }
        callout_block = {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"emoji": ""},
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Suggested saved views (create them in the UI):"
                        },
                    }
                ],
            },
        }
        bullets = [
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": t}}]
                },
            }
            for t in TIPS.get(
                title,
                ["- Create a Table view and save filters/sorts relevant to your role."],
            )
        ]

        children = [link_block, callout_block] + bullets
        c.blocks.children.append(pid, children=children)
        print("playbook:", page_title)

    print("done")


if __name__ == "__main__":
    main()
