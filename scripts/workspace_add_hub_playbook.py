#!/usr/bin/env python3
import os
import json
from notion_client import Client

ENC = "utf-8-sig"
MAP = "IFNS_Workspace_DB/config/workspace_companion_map.json"


def rich(txt):
    return [{"type": "text", "text": {"content": txt}}]


def main():
    c = Client(auth=os.environ["NOTION_TOKEN"])
    hub = json.load(open(MAP, "r", encoding=ENC))["hub_page_id"]

    blocks = [
        {"heading_2": {"rich_text": rich("Saved Views playbook")}},
        {
            "paragraph": {
                "rich_text": rich(
                    "Use these filters on the companion DBs (Tasks, Projects, Decisions, Approvals, Handover). Notions API cant create saved views yet, so this is a quick guide to click and save the views in the UI."
                )
            }
        },
        {
            "bulleted_list_item": {
                "rich_text": rich(
                    "Reviewer Inbox  Tasks where Status is Doing/Blocked, Due is within 7 days OR empty; sort by Due  then Last edited ."
                )
            }
        },
        {
            "bulleted_list_item": {
                "rich_text": rich(
                    "Due this week  Tasks where Due is within 7 days; sort by Due ."
                )
            }
        },
        {
            "bulleted_list_item": {
                "rich_text": rich(
                    "Blocked  Tasks where Status = Blocked; group by Assignee."
                )
            }
        },
        {
            "bulleted_list_item": {
                "rich_text": rich(
                    "Pending approvals  Approvals where Action is empty; sort by Created ."
                )
            }
        },
        {
            "bulleted_list_item": {
                "rich_text": rich(
                    "Decisions (recent)  Decisions sorted by Date ; optional filter Impact  {High, Med}."
                )
            }
        },
        {
            "paragraph": {
                "rich_text": rich(
                    "Tip: add a Status property to Projects if you want a Project-level health view (Planned/Active/Blocked/Done)."
                )
            }
        },
    ]
    c.blocks.children.append(block_id=hub, children=blocks)
    print("Hub updated with Saved Views playbook.")


if __name__ == "__main__":
    main()
