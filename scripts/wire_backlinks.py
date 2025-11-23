#!/usr/bin/env python3
import os
import json
from notion_client import Client

ENC = "utf-8-sig"
MAP = r"IFNS_Workspace_DB/config/workspace_companion_map.json"

DB_PLAYBOOK_TITLES = [
    "Admin - Config Index (SoT) — Saved Views Playbook",
    "Projects (SoT) — Saved Views Playbook",
    "Tasks (SoT)  Saved Views Playbook",
    "Decisions (SoT) — Saved Views Playbook",
    "Approvals (SoT) — Saved Views Playbook",
    "Handover (SoT) — Saved Views Playbook",
]


def list_child_pages(c, parent_id):
    out, cur = {}, None
    while True:
        resp = (
            c.blocks.children.list(parent_id, start_cursor=cur)
            if cur
            else c.blocks.children.list(parent_id)
        )
        for b in resp.get("results", []):
            if b.get("type") == "child_page":
                out[b["child_page"]["title"]] = b["id"]
        cur = resp.get("next_cursor")
        if not resp.get("has_more"):
            break
    return out


def ensure_child_page(c, parent_id, title):
    kids = list_child_pages(c, parent_id)
    if title in kids:
        return kids[title]
    p = c.pages.create(
        parent={"type": "page_id", "page_id": parent_id},
        properties={"title": {"title": [{"type": "text", "text": {"content": title}}]}},
    )
    return p["id"]


def wipe_children(c, page_id):
    ids, cur = [], None
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

    # find hosts: SoT  Steps & Saved Views Playbooks
    hub_children = list_child_pages(c, hub)
    steps_host = hub_children.get("SoT  Steps")
    playbooks_host = hub_children.get("Saved Views Playbooks")
    assert steps_host, "SoT  Steps not found under Hub"
    assert playbooks_host, "Saved Views Playbooks not found under Hub"

    # map playbook title  page id
    playbook_pages = list_child_pages(c, playbooks_host)
    link_ids = []
    for title in DB_PLAYBOOK_TITLES:
        pid = playbook_pages.get(title)
        if pid:
            link_ids.append((title, pid))

    # process each Step page
    step_pages = list_child_pages(c, steps_host)
    for step_title, step_pid in sorted(step_pages.items()):
        if not step_title.startswith("Step "):
            continue
        rel_ops_pid = ensure_child_page(c, step_pid, "00  Related operations")
        wipe_children(c, rel_ops_pid)

        children = []
        children.append(
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "icon": {"emoji": ""},
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Operational shortcuts  open these DB playbooks and save your personal views in Notion."
                            },
                        }
                    ],
                },
            }
        )
        for title, pid in link_ids:
            children.append(
                {
                    "object": "block",
                    "type": "link_to_page",
                    "link_to_page": {"type": "page_id", "page_id": pid},
                }
            )

        c.blocks.children.append(rel_ops_pid, children=children)
        print("wired:", step_title)
    print("done")


if __name__ == "__main__":
    main()
