import os
import json
from notion_client import Client, errors

m = json.load(
    open(r"IFNS_Workspace_DB/config/workspace_companion_map.json", encoding="utf-8-sig")
)
hub = m["hub_page_id"]
c = Client(auth=os.environ["NOTION_TOKEN"])


def show(e):
    if isinstance(e, errors.APIResponseError):
        print(
            "APIResponseError:",
            e.code,
            getattr(e, "message", ""),
            getattr(e, "body", ""),
        )
    else:
        print("Exception:", repr(e))


try:
    obj = c.pages.retrieve(hub)
    print("hub object:", obj.get("object"))
except Exception as e:
    show(e)
    raise

try:
    db = c.databases.create(
        parent={"type": "page_id", "page_id": hub},
        title=[{"type": "text", "text": {"content": "ZZZ Scratch (delete)"}}],
        properties={"Name": {"title": {}}},
    )
    print("create ok:", db.get("object"), db.get("id"))
except Exception as e:
    show(e)
    raise
