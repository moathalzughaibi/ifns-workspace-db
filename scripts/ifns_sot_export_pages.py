#!/usr/bin/env python3
import os, json, pathlib
from notion_client import Client

ENC="utf-8-sig"
MAP="IFNS_Workspace_DB/config/workspace_companion_map.json"
OUT_SOT="docs/ifns/sot/export/sot_docs"
OUT_STEPS="docs/ifns/sot/export/steps"

def to_md(blocks):
    def rt(x): return "".join([t.get("plain_text","") for t in x]) if x else ""
    lines=[]
    for b in blocks:
        t=b.get("type")
        if t=="heading_1": lines.append("# "+rt(b["heading_1"]["rich_text"]))
        elif t=="heading_2": lines.append("## "+rt(b["heading_2"]["rich_text"]))
        elif t=="paragraph": lines.append(rt(b["paragraph"]["rich_text"]))
        elif t=="bulleted_list_item": lines.append("- "+rt(b["bulleted_list_item"]["rich_text"]))
        elif t=="numbered_list_item": lines.append("1. "+rt(b["numbered_list_item"]["rich_text"]))
        elif t=="callout": lines.append("> " + rt(b["callout"]["rich_text"]))
        elif t=="divider": lines.append("\n---\n")
    return "\n".join(lines).strip()+"\n"

def dump_children(c, page_id):
    items=[]; cur=None
    while True:
        resp=c.blocks.children.list(page_id,start_cursor=cur) if cur else c.blocks.children.list(page_id)
        items+=resp.get("results",[])
        if not resp.get("has_more"): break
        cur=resp.get("next_cursor")
    return items

def export_children_pages(c, parent_id, out_dir):
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    kids = dump_children(c, parent_id)
    for k in kids:
        if k.get("type")!="child_page": continue
        title=k["child_page"]["title"]
        md=to_md(dump_children(c, k["id"]))
        (pathlib.Path(out_dir)/f"{title}.md").write_text(md,encoding=ENC)
        print("Exported ", title)

def main():
    c=Client(auth=os.environ["NOTION_TOKEN"])
    m=json.load(open(MAP,"r",encoding=ENC)); hub=m["hub_page_id"]
    kids=dump_children(c, hub)
    # find our four section pages
    ids={}
    for k in kids:
        if k.get("type")=="child_page":
            t=k["child_page"]["title"]
            ids[t]=k["id"]
    if "SoT Docs" in ids:          export_children_pages(c, ids["SoT Docs"], OUT_SOT)
    if "14-Step Spine" in ids:     export_children_pages(c, ids["14-Step Spine"], OUT_STEPS)

if __name__=="__main__":
    main()
