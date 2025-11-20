#!/usr/bin/env python3
import os, json, csv
from notion_client import Client
import httpx
ENC="utf-8-sig"

def db_query_safe(client, dbid, cursor=None):
    try:
        if hasattr(client.databases,"query"):
            return client.databases.query(database_id=dbid, start_cursor=cursor) if cursor else client.databases.query(database_id=dbid)
    except Exception: pass
    headers={"Authorization":f"Bearer {os.environ['NOTION_TOKEN']}",
             "Notion-Version":"2022-06-28","Content-Type":"application/json"}
    payload={"start_cursor":cursor} if cursor else {}
    r=httpx.post(f"https://api.notion.com/v1/databases/{dbid}/query",headers=headers,json=payload,timeout=60.0)
    r.raise_for_status(); return r.json()

def list_rows(notion, dbid):
    out, cur=[], None
    while True:
        resp=db_query_safe(notion, dbid, cur)
        out+=resp.get("results",[]); cur=resp.get("next_cursor")
        if not resp.get("has_more"): break
    return out

def flatten(page):
    row={"id":page["id"]}
    for name,prop in page.get("properties",{}).items():
        t=prop.get("type")
        if t=="title": row[name]="".join(x["plain_text"] for x in prop["title"]) if prop["title"] else ""
        elif t=="rich_text": row[name]="".join(x["plain_text"] for x in prop["rich_text"]) if prop["rich_text"] else ""
        elif t=="select": row[name]=prop["select"]["name"] if prop["select"] else ""
        elif t=="status": row[name]=prop["status"]["name"] if prop["status"] else ""
        elif t=="multi_select": row[name]=";".join(o["name"] for o in prop["multi_select"])
        elif t=="people": row[name]=";".join(p["name"] for p in prop["people"]) if prop["people"] else ""
        elif t=="date": row[name]=prop["date"]["start"] if prop["date"] else ""
        elif t=="checkbox": row[name]="true" if prop["checkbox"] else "false"
        elif t=="url": row[name]=prop["url"] or ""
        elif t=="relation": row[name]=";".join(r["id"] for r in prop["relation"]) if prop["relation"] else ""
        else: row[name]=""
    return row

def main():
    token=os.environ.get("NOTION_TOKEN"); root=os.environ.get("WORKSPACE_DB_ID") or os.environ.get("IFNS_Workspace_DB")
    assert token and root, "Missing NOTION_TOKEN or WORKSPACE_DB_ID/IFNS_Workspace_DB"
    notion=Client(auth=token)
    ids={"IFNS_Workspace_DB":root}
    cfg="IFNS_Workspace_DB/config/workspace_companion_map.json"
    if os.path.exists(cfg): ids.update(json.load(open(cfg,"r",encoding=ENC)))
    os.makedirs("sync/workspace",exist_ok=True)
    for name,dbid in ids.items():
        data=[flatten(p) for p in list_rows(notion, dbid)]
        out=f"sync/workspace/{name}.csv"
        if data:
            cols=sorted({k for d in data for k in d.keys()})
            with open(out,"w",newline="",encoding=ENC) as f:
                w=csv.DictWriter(f, fieldnames=list(cols)); w.writeheader(); w.writerows(data)
        else:
            with open(out,"w",newline="",encoding=ENC) as f: csv.writer(f).writerow(["id"])
        print(f"Exported {len(data)}  {out}")

if __name__=="__main__": main()
