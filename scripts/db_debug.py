from notion_client import Client
import os, sys
tok = os.environ.get("NOTION_TOKEN")
dbid_env = os.environ.get("WORKSPACE_DB_ID") or os.environ.get("IFNS_Workspace_DB")
c = Client(auth=tok)

print("ENV DB:", dbid_env)
# Try retrieve the env DB
ok = True
try:
    r = c.databases.retrieve(dbid_env)
    print("retrieve OK:", r["id"])
except Exception as e:
    ok = False
    print("retrieve FAILED:", e)

# If failed, search for likely databases by title
if not ok:
    hits = c.search(query="IFNS_Workspace_DB", filter={"property":"object","value":"database"})
    print("Search results:")
    for o in hits.get("results",[]):
        ttl = o.get("title",[{"plain_text":"(untitled)"}])[0]["plain_text"]
        print(" -", ttl, "", o["id"])
