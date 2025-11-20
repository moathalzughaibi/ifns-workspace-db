#!/usr/bin/env python3
import os, json
from notion_client import Client
ENC="utf-8-sig"; MAP="IFNS_Workspace_DB/config/workspace_companion_map.json"
def t(s): return [{"type":"text","text":{"content":s}}]
def main():
    c=Client(auth=os.environ["NOTION_TOKEN"])
    m=json.load(open(MAP,"r",encoding=ENC))
    P=m["Projects"]; T=m["Tasks"]; D=m["Decisions"]; A=m["Approvals"]; H=m["Handover"]
    p=c.pages.create(parent={"database_id":P},
                     properties={"Name":{"title":t("IFNS  Workspace bring-up")},
                                 "Status":{"select":{"name":"Active"}}})
    pid=p["id"]
    c.pages.create(parent={"database_id":T},
                   properties={"Name":{"title":t("Wire saved views & seed exporter")},
                               "Status":{"select":{"name":"Doing"}},
                               "Assignee":{"people":[]},
                               "Project":{"relation":[{"id":pid}]}})
    c.pages.create(parent={"database_id":D},
                   properties={"Name":{"title":t("Set SoT = Notion")},
                               "Impact":{"select":{"name":"High"}}})
    c.pages.create(parent={"database_id":A},
                   properties={"Name":{"title":t("Approve workspace structure")},
                               "Action":{"select":{"name":"approve"}}})
    c.pages.create(parent={"database_id":H},
                   properties={"Name":{"title":t("Workspace handover packet")},
                               "Status":{"select":{"name":"Draft"}}})
    print("Seeded demo rows.")
if __name__=="__main__": main()
