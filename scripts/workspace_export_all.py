#!/usr/bin/env python3
import os, json, csv
from notion_client import Client

ENC="utf-8-sig"

def list_rows(notion, dbid):
    rows=[]; cursor=None
    while True:
        resp=notion.databases.query(database_id=dbid, start_cursor=cursor) if cursor else notion.databases.query(database_id=dbid)
        rows += resp.get("results",[])
        cursor = resp.get("next_cursor")
        if not resp.get("has_more"): break
    return rows

def flatten(page):
    out={"id":page["id"]}
    for name, prop in page["properties"].items():
        t=prop.get("type")
        if t=="title": out[name]="".join(x["plain_text"] for x in prop["title"]) if prop["title"] else ""
        elif t=="rich_text": out[name]="".join(x["plain_text"] for x in prop["rich_text"]) if prop["rich_text"] else ""
        elif t=="select": out[name]=prop["select"]["name"] if prop["select"] else ""
        elif t=="status": out[name]=prop["status"]["name"] if prop["status"] else ""
        elif t=="multi_select": out[name]=";".join(o["name"] for o in prop["multi_select"])
        elif t=="people": out[name]=";".join(p["name"] for p in prop["people"]) if prop["people"] else ""
        elif t=="date": out[name]=prop["date"]["start"] if prop["date"] else ""
        elif t=="checkbox": out[name]="true" if prop["checkbox"] else "false"
        elif t=="url": out[name]=prop["url"] or ""
        elif t=="relation": out[name]=";".join(r["id"] for r in prop["relation"]) if prop["relation"] else ""
        else: out[name]=""
    return out

def main():
    token=os.environ.get("NOTION_TOKEN")
    root=os.environ.get("WORKSPACE_DB_ID") or os.environ.get("IFNS_Workspace_DB")
    assert token and root, "Set NOTION_TOKEN and WORKSPACE_DB_ID/IFNS_Workspace_DB"
    notion=Client(auth=token)

    cfg_path="IFNS_Workspace_DB/config/workspace_companion_map.json"
    ids={}
    if os.path.exists(cfg_path):
        ids=json.load(open(cfg_path,"r",encoding=ENC))
    # also export the root workspace DB itself
    ids={"IFNS_Workspace_DB": root, **ids}

    os.makedirs("sync/workspace", exist_ok=True)
    for name, dbid in ids.items():
        pages = list_rows(notion, dbid)
        data = [flatten(p) for p in pages]
        out = f"sync/workspace/{name}.csv"
        if data:
            cols=sorted(data[0].keys())
            with open(out,"w",newline="",encoding=ENC) as f:
                w=csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(data)
        else:
            with open(out,"w",newline="",encoding=ENC) as f:
                csv.writer(f).writerow(["id"])
        print(f"Exported {len(data)}  {out}")

if __name__=="__main__":
    main()
