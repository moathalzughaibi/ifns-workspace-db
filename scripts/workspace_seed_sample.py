#!/usr/bin/env python3
import os, json
from notion_client import Client

ENC="utf-8-sig"
MAP="IFNS_Workspace_DB/config/workspace_companion_map.json"

def t(text): return [{"type":"text","text":{"content":text}}]

def main():
    token=os.environ["NOTION_TOKEN"]
    root =os.environ.get("WORKSPACE_DB_ID") or os.environ.get("IFNS_Workspace_DB")
    notion=Client(auth=token)

    with open(MAP,"r",encoding=ENC) as f:
        m=json.load(f)

    projects=m["Projects"]; tasks=m["Tasks"]
    decisions=m["Decisions"]; approvals=m["Approvals"]; handover=m["Handover"]

    # 1) Project
    p = notion.pages.create(parent={"database_id":projects},
                            properties={"Name":{"title":t("IFNS  Workspace bring-up")},
                                        "State":{"select":{"name":"Active"}}})
    proj_id = p["id"]

    # 2) Task linked to Project
    notion.pages.create(parent={"database_id":tasks},
                        properties={"Name":{"title":t("Wire saved views & seed exporter")},
                                    "State":{"select":{"name":"Doing"}},
                                    "Project":{"relation":[{"id":proj_id}]}})

    # 3) Decision + Approval + Handover
    notion.pages.create(parent={"database_id":decisions},
                        properties={"Name":{"title":t("Set SoT = Notion")},
                                    "Project":{"rich_text":t("IFNS_Workspace")},
                                    "Impact":{"select":{"name":"High"}}})
    notion.pages.create(parent={"database_id":approvals},
                        properties={"Name":{"title":t("Approve workspace structure")},
                                    "Action":{"select":{"name":"approve"}}})
    notion.pages.create(parent={"database_id":handover},
                        properties={"Name":{"title":t("Workspace handover packet")},
                                    "State":{"select":{"name":"Draft"}}})
    print("Seeded demo rows.")
if __name__=="__main__": main()
