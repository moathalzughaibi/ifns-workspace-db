#!/usr/bin/env python3
import os
import re
import sys
import json
import pathlib
from typing import List, Tuple
from notion_client import Client

ENC = "utf-8-sig"
ROOT = pathlib.Path(".").resolve()
DOCS = ROOT / "docs"
MAP = ROOT / "IFNS_Workspace_DB" / "config" / "workspace_companion_map.json"
LEDGER = ROOT / "scripts" / "append_ledger.py"


def fail(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    try:
        if LEDGER.exists():
            import subprocess

            subprocess.run(
                ["python", str(LEDGER)], input=msg.encode("utf-8"), check=False
            )
    except Exception:
        pass
    sys.exit(2)


def env_client() -> Client:
    tok = os.getenv("NOTION_TOKEN")
    if not tok:
        fail("NOTION_TOKEN missing (run .\\local_env\\workspace_env.ps1)")
    return Client(auth=tok)


def load_map():
    if not MAP.exists():
        fail("Map missing (run build_workspace_hub_v3.py first)")
    try:
        return json.loads(MAP.read_text(encoding=ENC))
    except Exception as e:
        fail(f"Map read failed: {e!r}")


def list_child_pages(c: Client, parent_page_id: str) -> dict:
    out, cursor = {}, None
    while True:
        resp = (
            c.blocks.children.list(parent_page_id, start_cursor=cursor)
            if cursor
            else c.blocks.children.list(parent_page_id)
        )
        for b in resp.get("results", []):
            if b.get("type") == "child_page":
                out[b["child_page"]["title"]] = b["id"]
        cursor = resp.get("next_cursor")
        if not resp.get("has_more"):
            break
    return out


def ensure_child_page(c: Client, parent_page_id: str, title: str) -> str:
    pages = list_child_pages(c, parent_page_id)
    if title in pages:
        return pages[title]
    p = c.pages.create(
        parent={"type": "page_id", "page_id": parent_page_id},
        properties={"title": {"title": [{"type": "text", "text": {"content": title}}]}},
    )
    return p["id"]


def rt_chunks(text: str, chunk=1800):
    return [
        {"type": "text", "text": {"content": text[i : i + chunk]}}
        for i in range(0, len(text), chunk)
    ]


def replace_page_body_with_code(c: Client, page_id: str, blocks: List[str]):
    # wipe
    cursor = None
    ids = []
    while True:
        resp = (
            c.blocks.children.list(page_id, start_cursor=cursor)
            if cursor
            else c.blocks.children.list(page_id)
        )
        ids += [b["id"] for b in resp.get("results", [])]
        cursor = resp.get("next_cursor")
        if not resp.get("has_more"):
            break
    for bid in ids:
        c.blocks.delete(bid)
    # append
    children = [
        {
            "object": "block",
            "type": "code",
            "code": {"language": "markdown", "rich_text": rt_chunks(md)},
        }
        for md in blocks
    ]
    if children:
        c.blocks.children.append(page_id, children=children)


def extract_markdown_fences(text: str) -> List[str]:
    fences = re.findall(
        r"```(?:markdown)?\s*\r?\n(.*?)```", text, flags=re.DOTALL | re.IGNORECASE
    )
    return [s.strip() for s in fences if s.strip()]


def title_from_step_file(stem: str) -> Tuple[str, str]:
    m = re.match(r"Step_(\d{1,2})_([A-Za-z0-9\-]+)", stem)
    if not m:
        fail(f"Unrecognized step filename: {stem}")
    n = f"{int(m.group(1)):02d}"
    token = m.group(2)
    return f"Step {n}  {token}", n


def import_step_kit(c: Client, hub: str, path: pathlib.Path):
    step_title, step_num = title_from_step_file(path.stem)
    blocks = extract_markdown_fences(path.read_text(encoding=ENC))
    if not blocks:
        fail(f"No ```markdown``` blocks in {path.name}")
    steps_host = ensure_child_page(c, hub, "SoT  Steps")
    step_page = ensure_child_page(c, steps_host, step_title)
    parent_id = ensure_child_page(c, step_page, "01  Narrative & Intent")
    replace_page_body_with_code(c, parent_id, [blocks[0]])
    for i, blk in enumerate(blocks[1:], start=1):
        child = ensure_child_page(c, step_page, f"{step_num}.{i}  Section {i}")
        replace_page_body_with_code(c, child, [blk])
    print(f"Imported {path.name}  {step_title} ({len(blocks)} blocks)")


def import_core_ml_p6(c: Client, hub: str, path: pathlib.Path):
    blocks = extract_markdown_fences(path.read_text(encoding=ENC))
    host = ensure_child_page(c, hub, "Core ML  Indicator System (Phases)")
    p6 = ensure_child_page(c, host, "Phase 6  Implementation & Runtime Templates")
    if blocks:
        replace_page_body_with_code(c, p6, [blocks[0]])
    for i, blk in enumerate(blocks[1:], start=1):
        child = ensure_child_page(c, p6, f"P6.{i}  Section {i}")
        replace_page_body_with_code(c, child, [blk])
    print(f"Imported Core ML P6: {len(blocks)} blocks")


def import_qc_weekly(c: Client, hub: str, path: pathlib.Path):
    blocks = extract_markdown_fences(path.read_text(encoding=ENC))
    host = ensure_child_page(c, hub, "Telemetry & QC (V2 hub)")
    qc = ensure_child_page(c, host, "QC Weekly Telemetry V1")
    if blocks:
        replace_page_body_with_code(c, qc, [blocks[0]])
    for i, blk in enumerate(blocks[1:], start=1):
        child = ensure_child_page(c, qc, f"QC.{i}  Section {i}")
        replace_page_body_with_code(c, child, [blk])
    print(f"Imported QC Weekly: {len(blocks)} blocks")


def main():
    c = env_client()
    m = load_map()
    hub = m.get("hub_page_id")
    if not hub:
        fail("hub_page_id missing in map")
    if c.pages.retrieve(hub).get("object") != "page":
        fail("Hub is not a page")

    if not DOCS.exists():
        fail("docs/ folder not found")

    # recursive discovery
    step_kits = []
    for pat in [
        "Step_*_Narrative_Split_Kit.md",
        "Step_*_*_Narrative_Split_Kit.md",
        "Step_*_*_Split_Kit.md",
    ]:
        step_kits.extend(DOCS.rglob(pat))
    core_ml = list(DOCS.rglob("Core_ML_Phase6_Runtime_Templates_Split_Kit.md"))
    qc_weekly = list(DOCS.rglob("QC_Weekly_Telemetry_V1_Spec_Kit.md"))

    if not (step_kits or core_ml or qc_weekly):
        fail("No SoT kits found in docs/")

    for p in sorted(step_kits):
        import_step_kit(c, hub, p)
    if core_ml:
        import_core_ml_p6(c, hub, core_ml[0])
    if qc_weekly:
        import_qc_weekly(c, hub, qc_weekly[0])

    print("Import completed")


if __name__ == "__main__":
    main()
