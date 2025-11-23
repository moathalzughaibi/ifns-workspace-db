import os
from notion_client import Client

c = Client(auth=os.environ["NOTION_TOKEN"])
hits = c.search(query="")  # list everything, filter locally
for o in hits.get("results", []):
    if o.get("object") == "database":
        title = (o.get("title") or [{"plain_text": "(untitled)"}])[0]["plain_text"]
        print(f"{title} -> {o['id']}")
