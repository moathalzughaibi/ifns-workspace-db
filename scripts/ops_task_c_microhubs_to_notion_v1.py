# ops_task_c_microhubs_to_notion_v1.py
# Rebuild Task C: push Index micro-hubs into Notion by page title
#
# Behavior:
# - For each *.md file under docs/Ops_Implementer_Output/Task_C_Index_Microhubs
#   - Take the first '# ' heading as the target page title.
#   - Use Notion search API to find a page with that title.
#   - Append the markdown content as paragraph blocks to that page.
#
# This avoids stale 32-char IDs in the .md files.
#
# Requirements:
# - NOTION_TOKEN must be in the environment (run local_env\workspace_env.ps1 first)
# - notion-client must be installed in the active Python env.

import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from notion_client import Client
except ImportError as e:
    print(
        "[ERROR] Could not import notion_client. Is it installed in this environment?"
    )
    print(e)
    sys.exit(1)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
if NOTION_TOKEN is None:
    print("[ERROR] NOTION_TOKEN is missing. Did you run local_env\\workspace_env.ps1?")
    sys.exit(1)

notion = Client(auth=NOTION_TOKEN)

ROOT = Path("docs/Ops_Implementer_Output/Task_C_Index_Microhubs")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
SUMMARY_PATH = LOG_DIR / "ops_task_c_microhubs_to_notion_v1_summary.md"
FULL_LOG_PATH = LOG_DIR / f"ops_task_c_microhubs_to_notion_v1_{timestamp}_full.log"


def log(line: str) -> None:
    with FULL_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\\n")


def md_to_blocks(md_text: str):
    """Simple Markdown -> Notion blocks (paragraph-only for safety)."""
    blocks = []
    for line in md_text.splitlines():
        if line.strip():
            blocks.append(
                {
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": line}}]
                    },
                }
            )
        else:
            blocks.append({"type": "paragraph", "paragraph": {"rich_text": []}})
    return blocks


def extract_title(md_text: str):
    for line in md_text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return None


def find_page_id_by_title(title: str):
    """Use Notion search API to find a page with the given title."""
    try:
        res = notion.search(
            query=title,
            filter={"property": "object", "value": "page"},
            page_size=10,
        )
    except Exception as e:
        log(f"[ERROR] search('{title}') -> {e}")
        return None

    results = res.get("results", [])
    if not results:
        return None

    # Prefer exact title match if possible
    for page in results:
        props = page.get("properties", {})
        title_prop = None
        for key, val in props.items():
            if val.get("type") == "title":
                title_prop = val
                break
        if title_prop:
            plain = "".join(
                [t.get("plain_text", "") for t in title_prop.get("title", [])]
            ).strip()
            if plain == title:
                return page["id"]

    # Fallback: first result
    return results[0]["id"]


processed = []
skipped = []
failed = []

if not ROOT.exists():
    msg = f"[WARN] Microhubs root folder does not exist: {ROOT}"
    print(msg)
    log(msg)
else:
    for md_path in sorted(ROOT.rglob("*.md")):
        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception as e:
            msg = f"[ERROR] {md_path} - read error: {e}"
            print(msg)
            log(msg)
            failed.append((str(md_path), f"read error: {e}"))
            continue

        title = extract_title(text)
        if not title:
            msg = f"[SKIP] {md_path} - no H1 title found"
            print(msg)
            log(msg)
            skipped.append((str(md_path), "no H1 title"))
            continue

        page_id = find_page_id_by_title(title)
        if not page_id:
            msg = f"[SKIP] {md_path} - no page found for title '{title}'"
            print(msg)
            log(msg)
            skipped.append((str(md_path), f"no page for title '{title}'"))
            continue

        blocks = md_to_blocks(text)

        try:
            notion.blocks.children.append(page_id, children=blocks)
            msg = f"[OK] {md_path} -> {title} ({page_id})"
            print(msg)
            log(msg)
            processed.append((str(md_path), title))
        except Exception as e:
            msg = f"[ERROR] {md_path} -> {e}"
            print(msg)
            log(msg)
            failed.append((str(md_path), str(e)))

# Write summary
with SUMMARY_PATH.open("w", encoding="utf-8") as f:
    f.write("# Ops Task C - Micro-Hubs -> Notion Push (by title) - Summary\\n\\n")
    f.write(f"- Root folder: `{ROOT}`\\n")
    f.write(f"- Timestamp: {timestamp}\\n\\n")

    f.write("## Processed (OK)\\n")
    for p, title in processed:
        f.write(f"- {p} -> {title}\\n")
    f.write("\\n")

    f.write("## Skipped\\n")
    for p, reason in skipped:
        f.write(f"- {p} - {reason}\\n")
    f.write("\\n")

    f.write("## Failed\\n")
    for p, err in failed:
        f.write(f"- {p} - {err}\\n")
    f.write("\\n")

print(f"[DONE] Summary -> {SUMMARY_PATH}")
print(f"[DONE] Full log -> {FULL_LOG_PATH}")
