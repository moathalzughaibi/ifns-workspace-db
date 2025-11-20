from notion_client import Client
import os, json
c=Client(auth=os.environ["NOTION_TOKEN"])
m=json.load(open("IFNS_Workspace_DB/config/workspace_companion_map.json","r",encoding="utf-8-sig"))
for name, dbid in m.items():
    if name=="hub_page_id": continue
    db=c.databases.retrieve(dbid)
    props={k:v["type"] for k,v in db.get("properties",{}).items()}
    print(f"{name}: {props}")
