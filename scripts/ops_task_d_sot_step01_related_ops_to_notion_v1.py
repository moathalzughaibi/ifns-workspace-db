# ops_task_d_sot_step01_related_ops_to_notion_v1.py
# Simplified & robust implementation:
# - Uses the known parent page ID for "Step 01  Preface"
# - Creates or reuses a child page "00 Related operations"
# - Pushes content from SoT_Step01_00_Related_Operations_new.md

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
    print("[ERROR] NOTION_TOKEN is missing. Run local_env\\workspace_env.ps1 first.")
    sys.exit(1)

notion = Client(auth=NOTION_TOKEN)

# Page ID printed when we created "Step 01  Preface"
STEP01_PREFACE_PAGE_ID = "2b8b22c7-70d9-81a7-9598-d8cdf0858daf"

SRC_MD = Path(
    "docs/Ops_Implementer_Output/Task_D_SoT_Step01_Related_Operations/SoT_Step01_00_Related_Operations_new.md"
)
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

SUMMARY_PATH = LOG_DIR / "ops_task_d_sot_step01_related_ops_to_notion_v1_summary.md"
FULL_LOG_PATH = (
    LOG_DIR / f"ops_task_d_sot_step01_related_ops_to_notion_v1_{timestamp}_full.log"
)


def log(line: str) -> None:
    print(line)
    with FULL_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\\n")


def md_to_blocks(md_text: str):
    """Very simple Markdown -> Notion blocks (paragraph-only)."""
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


def ensure_source_exists():
    if not SRC_MD.exists():
        log(f"[ERROR] Source MD file not found: {SRC_MD}")
        sys.exit(1)
    try:
        text = SRC_MD.read_text(encoding="utf-8")
    except Exception as e:
        log(f"[ERROR] Could not read source MD file: {e}")
        sys.exit(1)
    return text


def find_existing_child_page(parent_block_id: str, title: str):
    """Look for an existing child_page with the given title under the parent."""
    try:
        res = notion.blocks.children.list(parent_block_id, page_size=100)
    except Exception as e:
        log(f"[ERROR] children.list({parent_block_id}) -> {e}")
        return None

    for block in res.get("results", []):
        if block.get("type") == "child_page":
            child_title = block.get("child_page", {}).get("title", "")
            if child_title == title:
                return block["id"]
    return None


def create_child_page(parent_page_id: str, title: str):
    try:
        page = notion.pages.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            properties={
                "title": {
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": title},
                        }
                    ]
                }
            },
        )
        log(f"[INFO] Created child page '{title}' under Step 01  Preface: {page['id']}")
        return page["id"]
    except Exception as e:
        log(f"[ERROR] Failed to create child page '{title}': {e}")
        return None


def append_blocks_to_page(page_id: str, blocks):
    try:
        notion.blocks.children.append(page_id, children=blocks)
        log(f"[INFO] Appended {len(blocks)} blocks to page {page_id}")
    except Exception as e:
        log(f"[ERROR] Failed to append blocks to page {page_id}: {e}")
        sys.exit(1)


def main():
    log(f"[INFO] Using source file: {SRC_MD}")
    md_text = ensure_source_exists()
    blocks = md_to_blocks(md_text)

    target_title = "00 Related operations"
    log(
        f"[INFO] Looking for existing child page '{target_title}' under Step 01  Preface ..."
    )
    existing_id = find_existing_child_page(STEP01_PREFACE_PAGE_ID, target_title)

    if existing_id:
        log(f"[INFO] Found existing page '{target_title}': {existing_id}")
        target_page_id = existing_id
    else:
        log("[INFO] No existing child page found. Creating a new one ...")
        target_page_id = create_child_page(STEP01_PREFACE_PAGE_ID, target_title)
        if not target_page_id:
            log("[ERROR] Could not create '00 Related operations' page. Aborting.")
            sys.exit(1)

    append_blocks_to_page(target_page_id, blocks)

    with SUMMARY_PATH.open("w", encoding="utf-8") as f:
        f.write("# Ops Task D - SoT Step 01 Related Ops -> Notion (v1) - Summary\\n\\n")
        f.write(f"- Source: `{SRC_MD}`\\n")
        f.write(f"- Parent page id (Step 01  Preface): `{STEP01_PREFACE_PAGE_ID}`\\n")
        f.write(f"- Target page: `{target_title}` (id: {target_page_id})\\n")
        f.write(f"- Blocks appended: {len(blocks)}\\n")
        f.write(f"- Timestamp: {timestamp}\\n")

    log(f"[DONE] Summary -> {SUMMARY_PATH}")
    log(f"[DONE] Full log -> {FULL_LOG_PATH}")


if __name__ == "__main__":
    main()
