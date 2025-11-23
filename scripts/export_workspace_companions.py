#!/usr/bin/env python3
import os
import json
import csv
import pathlib
from notion_client import Client

ENC = "utf-8-sig"
MAP = r"IFNS_Workspace_DB/config/workspace_companion_map.json"
OUT = pathlib.Path("sync/workspace")
OUT.mkdir(parents=True, exist_ok=True)


def rt2txt(rt):
    return "".join([t["text"]["content"] for t in rt]) if rt else ""


def sel2txt(s):
    return s["name"] if s else ""


def ppl2txt(p):
    return ", ".join([u["name"] for u in p]) if p else ""


def rel2txt(r):
    return ", ".join([x["id"] for x in r]) if r else ""


def date2txt(d):
    return d["start"] if d else ""


def flatten(props):
    out = {}
    for k, v in props.items():
        t = v["type"]
        if t == "title":
            out[k] = rt2txt(v["title"])
        elif t == "rich_text":
            out[k] = rt2txt(v["rich_text"])
        elif t == "select":
            out[k] = sel2txt(v["select"])
        elif t == "multi_select":
            out[k] = ";".join([x["name"] for x in v["multi_select"]])
        elif t == "people":
            out[k] = ppl2txt(v["people"])
        elif t == "relation":
            out[k] = rel2txt(v["relation"])
        elif t == "date":
            out[k] = date2txt(v["date"])
        elif t == "checkbox":
            out[k] = str(v["checkbox"])
        elif t == "number":
            out[k] = str(v["number"]) if v["number"] is not None else ""
        else:
            out[k] = ""  # files, formula, rollup -> skip/blank
    return out


def dump_db(c, dbid, name):
    rows = []
    cursor = None
    while True:
        resp = (
            c.databases.query(database_id=dbid, start_cursor=cursor)
            if cursor
            else c.databases.query(database_id=dbid)
        )
        for r in resp["results"]:
            rows.append(flatten(r["properties"]) | {"_page_id": r["id"]})
        cursor = resp.get("next_cursor")
        if not resp.get("has_more"):
            break
    if not rows:
        return
    cols = sorted({k for r in rows for k in r.keys()})
    with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print("exported:", name, len(rows))


def main():
    tok = os.getenv("NOTION_TOKEN")
    assert tok, "NOTION_TOKEN missing"
    c = Client(auth=tok)
    m = json.load(open(MAP, encoding=ENC))
    targets = [
        ("admin_config_index", m["Admin_Config_Index"]),
        ("projects", m["Projects"]),
        ("tasks", m["Tasks"]),
        ("decisions", m["Decisions"]),
        ("approvals", m["Approvals"]),
        ("handover", m["Handover"]),
    ]
    for name, dbid in targets:
        dump_db(c, dbid, name)
    print("done")


if __name__ == "__main__":
    main()
