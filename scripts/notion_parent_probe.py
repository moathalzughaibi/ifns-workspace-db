#!/usr/bin/env python3
import os
import json
from notion_client import Client, errors

MAP = r"IFNS_Workspace_DB/config/workspace_companion_map.json"
m = json.load(open(MAP, encoding="utf-8-sig"))
hub = m.get("hub_page_id")
c = Client(auth=os.environ["NOTION_TOKEN"])

print("HUB_ID:", hub)
try:
    obj = c.pages.retrieve(hub)
    print("hub.object:", obj.get("object"))
except Exception as e:
    print("pages.retrieve failed:", repr(e))
    raise SystemExit(1)

# try creating a tiny scratch DB
try:
    db = c.databases.create(
        parent={"type": "page_id", "page_id": hub},
        title=[{"type": "text", "text": {"content": "ZZZ Scratch (delete)"}}],
        properties={"Name": {"title": {}}},
    )
    print("scratch.create:", db.get("object"), db.get("id"))
except errors.APIResponseError as e:
    print("databases.create failed (API):", e.code, e.message)
except Exception as e:
    print("databases.create failed:", repr(e))
