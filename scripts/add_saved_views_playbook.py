#!/usr/bin/env python3
# scripts/add_saved_views_playbook.py
import os
import json
from notion_client import Client

ENC = "utf-8-sig"
MAP = r"IFNS_Workspace_DB/config/workspace_companion_map.json"

RECIPES = {
    "Projects (SoT)": """# Views to create
- **By Status (Kanban):** Group by Status  Order: Active, On Hold, Done
- **By Owner:** Filter: Owner = me()
- **Quarter Plan:** Filter: Target Quarter = current; Sort: Priority desc""",
    "Tasks (SoT)": """# Views to create
- **My Open:** Assignee = me() AND Status  {Todo, In Progress}
- **Due This Week:** Due within next 7 days
- **Blocked:** Blocked = true""",
    "Decisions (SoT)": """# Views to create
- **Pending:** Status = Pending; Sort: Raised date desc
- **By Step:** Group by Step (0714)
- **Closed:** Status  {Approved, Rejected}""",
    "Approvals (SoT)": """# Views to create
- **Awaiting My Approval:** Approver = me() AND Status = Awaiting
- **Overdue:** SLA breach = true""",
    "Handover (SoT)": """# Views to create
- **Open Handovers:** Status  {Open, In Progress}
- **By Receiver:** Group by Receiver
- **Completed:** Status = Done""",
}


def ensure_page(c, parent_page_id, title):
    # find child page by title or create
    cur = None
    while True:
        resp = (
            c.blocks.children.list(parent_page_id, start_cursor=cur)
            if cur
            else c.blocks.children.list(parent_page_id)
        )
        for b in resp.get("results", []):
            if b["type"] == "child_page" and b["child_page"]["title"] == title:
                return b["id"]
        cur = resp.get("next_cursor")
        if not resp.get("has_more"):
            break
    p = c.pages.create(
        parent={"type": "page_id", "page_id": parent_page_id},
        properties={"title": {"title": [{"type": "text", "text": {"content": title}}]}},
    )
    return p["id"]


def replace_with_md(c, page_id, md_text):
    # wipe children
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
    c.blocks.children.append(
        page_id,
        children=[
            {
                "object": "block",
                "type": "code",
                "code": {
                    "language": "markdown",
                    "rich_text": [{"type": "text", "text": {"content": md_text}}],
                },
            }
        ],
    )


def main():
    tok = os.getenv("NOTION_TOKEN")
    assert tok, "NOTION_TOKEN missing"
    c = Client(auth=tok)
    m = json.load(open(MAP, encoding=ENC))
    hub = m["hub_page_id"]
    # create hub page
    play = ensure_page(c, hub, "Saved Views Playbook")
    # one page per DB
    for key, title in [
        ("Projects", "Projects (SoT)"),
        ("Tasks", "Tasks (SoT)"),
        ("Decisions", "Decisions (SoT)"),
        ("Approvals", "Approvals (SoT)"),
        ("Handover", "Handover (SoT)"),
    ]:
        pid = ensure_page(c, play, title)
        replace_with_md(c, pid, RECIPES.get(title, "# Views to create\n- (fill in)"))
        print("playbook:", title)
    print("Playbook: OK")


if __name__ == "__main__":
    main()
