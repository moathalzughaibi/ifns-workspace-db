#!/usr/bin/env python3
import os
import csv
from notion_client import Client


def flat(page):
    out = {"id": page["id"]}
    for k, p in page["properties"].items():
        t = p.get("type")
        if t == "title":
            out[k] = "".join(x["plain_text"] for x in p["title"]) if p["title"] else ""
        elif t == "rich_text":
            out[k] = (
                "".join(x["plain_text"] for x in p["rich_text"])
                if p["rich_text"]
                else ""
            )
        elif t == "select":
            out[k] = p["select"]["name"] if p["select"] else ""
        elif t == "status":
            out[k] = p["status"]["name"] if p["status"] else ""
        elif t == "multi_select":
            out[k] = ";".join(o["name"] for o in p["multi_select"])
        elif t == "people":
            out[k] = ";".join(peep["name"] for peep in p["people"])
        elif t == "date":
            out[k] = p["date"]["start"] if p["date"] else ""
        elif t == "checkbox":
            out[k] = "true" if p["checkbox"] else "false"
        elif t == "url":
            out[k] = p["url"] or ""
        else:
            out[k] = ""
    return out


def main():
    token = os.environ.get("NOTION_TOKEN")
    dbid = os.environ.get("WORKSPACE_DB_ID") or os.environ.get("IFNS_Workspace_DB")
    assert token and dbid, "Missing NOTION_TOKEN or WORKSPACE_DB_ID/IFNS_Workspace_DB"
    notion = Client(auth=token)

    db = notion.databases.retrieve(dbid)
    name = db["title"][0]["plain_text"] if db["title"] else "WorkspaceDB"
    rows = []
    cursor = None
    while True:
        resp = (
            notion.databases.query(database_id=dbid, start_cursor=cursor)
            if cursor
            else notion.databases.query(database_id=dbid)
        )
        rows += resp.get("results", [])
        cursor = resp.get("next_cursor")
        if not resp.get("has_more"):
            break

    data = [flat(p) for p in rows]
    os.makedirs("sync/workspace", exist_ok=True)
    out = f"sync/workspace/{name.replace(' ','_')}.csv"
    if data:
        cols = sorted(data[0].keys())
        with open(out, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(data)
    else:
        with open(out, "w", newline="", encoding="utf-8-sig") as f:
            csv.writer(f).writerow(["id"])
    print(f"Exported {len(data)} rows  {out}")


if __name__ == "__main__":
    main()
