#!/usr/bin/env python3
import os
import json
from notion_client import Client, errors

ENC = "utf-8-sig"
MAP = r"IFNS_Workspace_DB/config/workspace_companion_map.json"
tok = os.getenv("NOTION_TOKEN")
assert tok, "NOTION_TOKEN missing"
c = Client(auth=tok)
m = json.load(open(MAP, encoding=ENC))
targets = [("Hub", m["hub_page_id"])]
for k in (
    "Admin_Config_Index",
    "Projects",
    "Tasks",
    "Decisions",
    "Approvals",
    "Handover",
):
    targets.append((k, m[k]))
for name, idv in targets:
    try:
        obj = c.pages.retrieve(idv) if name == "Hub" else c.databases.retrieve(idv)
        print(name, " OK")
    except errors.APIResponseError as e:
        print(name, " FAIL:", e.code)
print("done")
