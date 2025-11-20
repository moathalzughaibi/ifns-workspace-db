#!/usr/bin/env python3
import os, re, io, json, pathlib, textwrap
from notion_client import Client

ENC="utf-8-sig"
MAP="IFNS_Workspace_DB/config/workspace_companion_map.json"
SOT="IFNS_Workspace_DB/config/.sot_mode.json"
MAN="docs/ifns/sot/build/manifest_v1.json"
MAX_TEXT=1800  # keep well under Notion's 2000-char limit per rich_text

def rt(s): return [{"type":"text","text":{"content":s}}]

def chunk(s, n=MAX_TEXT):
    s = s.replace("\r\n","\n")
    if len(s) <= n:
        return [s]
    out=[]
    for para in s.split("\n"):
        if not para:
            out.append("")
            continue
        while len(para) > n:
            # split on last space before n chars when possible
            cut = para.rfind(" ",0,n)
            if cut < int(n*0.6): cut = n
            out.append(para[:cut].rstrip())
            para = para[cut:].lstrip()
        out.append(para)
    return out

def md_to_blocks(md_text):
    blocks=[]; buf=[]
    def flush():
        if not buf: return
        text = "\n".join(buf)
        for seg in chunk(text):
            blocks.append({"object":"block","paragraph":{"rich_text":rt(seg)}})
        buf.clear()
    for raw in io.StringIO(md_text):
        s=raw.rstrip("\n")
        if s.startswith("# "):
            flush(); blocks.append({"object":"block","heading_1":{"rich_text":rt(s[2:].strip())}})
        elif s.startswith("## "):
            flush(); blocks.append({"object":"block","heading_2":{"rich_text":rt(s[3:].strip())}})
        elif s.strip()=="":
            flush()
        else:
            buf.append(s)
    flush()
    return blocks

def fenced_markdown_blocks(full_md):
    """Return list of (label_or_title, content) for ```markdown blocks"""
    out=[]; lines=full_md.splitlines(); i=0; last_label=None
    while i<len(lines):
        if lines[i].strip().startswith("###"):
            last_label = lines[i].strip("# ").strip()
        if lines[i].strip().lower().startswith("```markdown"):
            j=i+1; buf=[]
            while j<len(lines) and not lines[j].strip().startswith("```"):
                buf.append(lines[j]); j+=1
            title_guess=None
            for b in buf:
                if b.startswith("# "):  title_guess=b[2:].strip(); break
                if b.startswith("## "): title_guess=b[3:].strip(); break
            out.append((title_guess or last_label or "Untitled", "\n".join(buf)))
            i=j
        i+=1
    return out

def ensure_child_page(c, parent_id, title):
    kids=c.blocks.children.list(parent_id).get("results",[])
    for k in kids:
        if k.get("type")=="child_page" and k["child_page"].get("title")==title:
            return k["id"]
    p=c.pages.create(parent={"type":"page_id","page_id":parent_id},
                     properties={"title":{"title":rt(title)}})
    return p["id"]

def clear_children(c, page_id):
    # wipe page content (so re-runs replace, not append)
    kids=c.blocks.children.list(page_id).get("results",[])
    for k in kids:
        try:
            c.blocks.delete(k["id"])
        except Exception:
            pass

def main():
    mode=json.load(open(SOT,"r",encoding=ENC))
    if not mode.get("import_enabled"):
        raise SystemExit("Import disabled by SoT guard. Set import_enabled:true to bootstrap once.")

    m=json.load(open(MAN,"r",encoding=ENC))
    token=os.environ["NOTION_TOKEN"]
    if not token: raise SystemExit("Missing NOTION_TOKEN")
    c=Client(auth=token)

    wmap=json.load(open(MAP,"r",encoding=ENC))
    hub=wmap["hub_page_id"]

    sot_docs_pg    = ensure_child_page(c, hub, "SoT Docs")
    spine_pg       = ensure_child_page(c, hub, "14-Step Spine")
    core_ml_hub_pg = ensure_child_page(c, hub, m["sections"]["Core_ML_Phase6"]["hub_title"])
    tqc_hub_pg     = ensure_child_page(c, hub, m["sections"]["Telemetry_QC"]["hub_title"])

    # SoT Docs
    for doc in m["sections"]["SoT_Docs"]:
        path=doc["file"]; title=doc["notion_title"]
        if not pathlib.Path(path).exists(): continue
        page=ensure_child_page(c, sot_docs_pg, title)
        clear_children(c, page)
        md=open(path,"r",encoding=ENC).read()
        c.blocks.children.append(page, children=md_to_blocks(md))
        print("SoT Doc ", title)

    # 14-Step spine
    for s in m["sections"]["Steps"]:
        path=s["file"]; step_title=s["page_title"]
        if not pathlib.Path(path).exists(): continue
        full=open(path,"r",encoding=ENC).read()
        step_page = ensure_child_page(c, spine_pg, step_title)

        blocks = fenced_markdown_blocks(full)
        parent_blocks = md_to_blocks(blocks[0][1]) if blocks else []
        child_blocks  = [md_to_blocks(b[1]) for b in blocks[1:]] if blocks else []

        p01 = ensure_child_page(c, step_page, "01  Narrative & Intent")
        clear_children(c, p01)
        if parent_blocks:
            c.blocks.children.append(p01, children=parent_blocks)

        mstep=re.match(r"Step (\d{2})", step_title)
        nn = mstep.group(1) if mstep else "NN"
        for i, cb in enumerate(child_blocks, start=1):
            child_title_guess = blocks[i][0] if i<len(blocks) else None
            child_title = f"{nn}.{i}  {child_title_guess or 'Section'}"
            ch = ensure_child_page(c, step_page, child_title)
            clear_children(c, ch)
            c.blocks.children.append(ch, children=cb)
        print(f"Step  {step_title} (children: {len(child_blocks)})")

    # Core ML Phase 6
    cm = m["sections"]["Core_ML_Phase6"]
    if pathlib.Path(cm["file"]).exists():
        phase6 = ensure_child_page(c, core_ml_hub_pg, cm["page_title"])
        clear_children(c, phase6)
        txt=open(cm["file"],"r",encoding=ENC).read()
        note = "Related Steps: " + ", ".join([f"{n:02d}" for n in cm["related_steps"]])
        c.blocks.children.append(phase6, children=[
            {"object":"block","callout":{"icon":{"type":"emoji","emoji":"ℹ"},"rich_text":rt(note)}}
        ] + md_to_blocks(txt))
        print("Core ML Phase 6  applied")

    # Telemetry & QC
    tq = m["sections"]["Telemetry_QC"]
    if pathlib.Path(tq["file"]).exists():
        qc = ensure_child_page(c, tqc_hub_pg, tq["page_title"])
        clear_children(c, qc)
        txt=open(tq["file"],"r",encoding=ENC).read()
        note = "Related Steps: " + ", ".join([f"{n:02d}" for n in tq["related_steps"]])
        c.blocks.children.append(qc, children=[
            {"object":"block","callout":{"icon":{"type":"emoji","emoji":"ℹ"},"rich_text":rt(note)}}
        ] + md_to_blocks(txt))
        print("Telemetry & QC (V1)  applied")

    print("Apply complete. Lock SoT next.")

if __name__=="__main__":
    main()
