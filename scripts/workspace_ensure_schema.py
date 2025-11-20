from notion_client import Client
import os, json
c=Client(auth=os.environ["NOTION_TOKEN"])
m=json.load(open("IFNS_Workspace_DB/config/workspace_companion_map.json","r",encoding="utf-8-sig"))

CANON = {
 "Projects":{"Status":"select","Owner":"people","Due":"date","Repo":"url","Notes":"rich_text"},
 "Tasks":{"Status":"select","Assignee":"people","Due":"date","Repo":"url","Notes":"rich_text","Project":"relation"},
 "Decisions":{"Date":"date","Owner":"people","Impact":"select","Notes":"rich_text"},
 "Approvals":{"Object URL":"url","Action":"select","By":"people","At":"date","Notes":"rich_text"},
 "Handover":{"Status":"select","Repo":"url","Notes":"rich_text"},
}
def ensure(dbid, want, extras=None):
    db=c.databases.retrieve(dbid)
    props=db.get("properties",{})
    # rename State->Status if present
    if "State" in props and "Status" not in props:
        c.databases.update(database_id=dbid, title=db["title"], properties={"Status":{"select":{}}})
        # values migrate on next edits; we just ensure the key exists now
    # add any missing canonical props
    add={}
    for k,t in want.items():
        if k not in props:
            add[k] = {t:{} if t!="select" else {"options":[{"name":"Planned"},{"name":"Active"},{"name":"Blocked"},{"name":"Done"}]}}
    if add:
        c.databases.update(database_id=dbid, title=db["title"], properties=add)
for name, dbid in m.items():
    if name=="hub_page_id": continue
    want=CANON.get(name,{})
    ensure(dbid,want)
print("Schema ensured.")
