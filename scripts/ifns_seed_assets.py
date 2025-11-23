#!/usr/bin/env python3
"""
scripts/ifns_seed_assets.py

One-time / idempotent seeding of IFNS indicator & runtime assets into Notion.

- Creates IFNS section pages under the Hub page:
    * IFNS – Indicators Library
    * IFNS – Feature Schema & Policy
    * IFNS – Feature Views & QC
    * IFNS – Runtime & Telemetry
    * IFNS – Legacy Deep Spec

- For each target in reports/IFNS_Notion_Targets.csv:
    * If notion_target_type == "db":
        - Ensures a Notion database exists under the right section page.
        - If the DB is empty, imports CSV rows as pages.
        - Registers the DB id in workspace_companion_map.json under the key = notion_target_name.
    * If notion_target_type == "page":
        - Ensures a section sub-page exists under Legacy Deep Spec (e.g. "Conceptual & Operational Frameworks").
        - For each doc, creates a child page with the markdown content as a single paragraph (if not already present).
    * If notion_target_type == "file":
        - Creates a child page under the parent page and pastes the file contents as text.

Requirements:
- NOTION_TOKEN and WORKSPACE_DB_ID must be set (via local_env/workspace_env.ps1).
- MAP must already contain "hub_page_id" (created by build_workspace_hub_v4.py).

This script is designed to be safe to re-run:
- Section pages are re-used if they already exist.
- Databases are re-used if already created (by key).
- CSV import is skipped if the target DB already has at least one row.
- Doc/file pages are skipped if a child page with the same title already exists.
"""
import csv
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from notion_client import Client, APIResponseError  # type: ignore

ENC = "utf-8-sig"
MAP_PATH = Path("IFNS_Workspace_DB/config/workspace_companion_map.json")
TARGETS_PATH = Path("reports/IFNS_Notion_Targets.csv")


SECTION_NAMES = [
    "IFNS – Indicators Library",
    "IFNS – Feature Schema & Policy",
    "IFNS – Feature Views & QC",
    "IFNS – Runtime & Telemetry",
    "IFNS – Legacy Deep Spec",
]


def fail(msg: str) -> None:
    print("ERROR:", msg, file=sys.stderr)
    sys.exit(2)


def load_map() -> Dict[str, str]:
    if not MAP_PATH.is_file():
        fail(f"Map file missing: {MAP_PATH}")
    with MAP_PATH.open(encoding=ENC) as f:
        return json.load(f)


def save_map(m: Dict[str, str]) -> None:
    with MAP_PATH.open("w", encoding=ENC) as f:
        json.dump(m, f, indent=2)


def get_client() -> Client:
    tok = os.getenv("NOTION_TOKEN")
    if not tok:
        fail("NOTION_TOKEN is missing; run local_env/workspace_env.ps1 first.")
    return Client(auth=tok)


def list_child_blocks(c: Client, parent_id: str) -> List[dict]:
    """Return all child blocks for a given page."""
    results: List[dict] = []
    cursor = None
    while True:
        if cursor:
            resp = c.blocks.children.list(parent_id, start_cursor=cursor)
        else:
            resp = c.blocks.children.list(parent_id)
        results.extend(resp.get("results", []))
        cursor = resp.get("next_cursor")
        if not resp.get("has_more"):
            break
    return results


def list_child_pages(c: Client, parent_id: str) -> Dict[str, str]:
    """Return {title: page_id} for child_page blocks under parent."""
    out: Dict[str, str] = {}
    for b in list_child_blocks(c, parent_id):
        t = b.get("type")
        if t == "child_page":
            title = b[t].get("title") or ""
            out[title] = b["id"]
    return out


def ensure_section_page(c: Client, hub_page_id: str, title: str) -> str:
    kids = list_child_pages(c, hub_page_id)
    if title in kids:
        return kids[title]
    p = c.pages.create(
        parent={"type": "page_id", "page_id": hub_page_id},
        properties={"title": {"title": [{"type": "text", "text": {"content": title}}]}},
    )
    pid = p["id"]
    print("created section page:", title, pid)
    return pid


def ensure_section_pages(c: Client, hub_page_id: str) -> Dict[str, str]:
    """Ensure the 5 IFNS section pages exist; return {title: page_id}."""
    sections: Dict[str, str] = {}
    existing = list_child_pages(c, hub_page_id)
    for title in SECTION_NAMES:
        if title in existing:
            sections[title] = existing[title]
        else:
            sections[title] = ensure_section_page(c, hub_page_id, title)
    return sections


def parse_targets() -> Tuple[List[dict], List[dict], List[dict]]:
    """Return (tables, docs, files) from IFNS_Notion_Targets.csv."""
    if not TARGETS_PATH.is_file():
        fail(f"Targets file missing: {TARGETS_PATH}")
    tables: List[dict] = []
    docs: List[dict] = []
    files: List[dict] = []
    with TARGETS_PATH.open(encoding=ENC, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ttype = row.get("notion_target_type")
            asset = row.get("asset_type")
            if not ttype:
                continue
            if asset == "table" and ttype == "db":
                tables.append(row)
            elif asset == "doc" and ttype == "page":
                docs.append(row)
            elif ttype == "file":
                files.append(row)
            else:
                # ignore others for now
                continue
    return tables, docs, files


def group_by_db_target(table_rows: List[dict]) -> Dict[Tuple[str, str], List[dict]]:
    """Group tables by (parent_page_name, notion_target_name)."""
    grouped: Dict[Tuple[str, str], List[dict]] = {}
    for row in table_rows:
        parent = row["notion_parent_page"]
        name = row["notion_target_name"]
        key = (parent, name)
        grouped.setdefault(key, []).append(row)
    return grouped


def group_docs(docs_rows: List[dict]) -> Dict[Tuple[str, str], List[dict]]:
    """Group docs by (parent_page_name, notion_target_name)."""
    grouped: Dict[Tuple[str, str], List[dict]] = {}
    for row in docs_rows:
        parent = row["notion_parent_page"]
        name = row["notion_target_name"]
        key = (parent, name)
        grouped.setdefault(key, []).append(row)
    return grouped


def load_csv_headers(repo_root: Path, rows: List[dict]) -> List[str]:
    """Return a union of CSV header columns across all rows (CSV files only)."""
    cols: List[str] = []
    seen = set()
    for row in rows:
        rel = row["new_rel_path"].replace("\\", "/")
        if not rel.lower().endswith(".csv"):
            continue
        path = repo_root / rel
        if not path.is_file():
            print(
                "WARN: CSV file missing when scanning headers:", path, file=sys.stderr
            )
            continue
        with path.open(encoding=ENC, newline="") as f:
            reader = csv.reader(f)
            try:
                hdr = next(reader)
            except StopIteration:
                continue
        for col in hdr:
            col = col.strip()
            if col and col not in seen:
                seen.add(col)
                cols.append(col)
    return cols


def ensure_ifns_db(
    c: Client,
    m: Dict[str, str],
    parent_page_id: str,
    db_key: str,
    db_title: str,
    headers: List[str],
) -> str:
    """Ensure a Notion database exists for this IFNS target.

    db_key is the key used in workspace_companion_map.json (typically notion_target_name).
    db_title is the visible DB title in Notion.
    headers is a list of CSV column names to create as rich_text properties.
    """
    dbid = m.get(db_key)
    if dbid:
        return dbid

    # Build properties: Name (title) + Source_File + Source_Row_Index + all header columns.
    props: Dict[str, dict] = {
        "Name": {"title": {}},
        "Source_File": {"rich_text": {}},
        "Source_Row_Index": {"number": {}},
    }
    for col in headers:
        if col == "Name":
            continue
        # Notion property keys must be <= 2000 chars; keep original name otherwise.
        props[col] = {"rich_text": {}}

    db = c.databases.create(
        parent={"type": "page_id", "page_id": parent_page_id},
        title=[{"type": "text", "text": {"content": db_title}}],
        properties=props,
    )
    dbid = db["id"]
    m[db_key] = dbid
    print("created IFNS DB:", db_title, "->", dbid)
    return dbid


def db_has_rows(c: Client, dbid: str) -> bool:
    """Return True if the database has at least one page."""
    resp = c.databases.query(database_id=dbid, page_size=1)
    return bool(resp.get("results"))


def import_csv_into_db(
    c: Client,
    dbid: str,
    db_title: str,
    repo_root: Path,
    rows: List[dict],
    headers: List[str],
) -> None:
    """Import CSV rows into the given database (only CSV files)."""
    if not headers:
        print("No headers found for", db_title, "- skipping import.")
        return

    name_field = None
    # Prefer a column that looks like a name/id:
    for candidate in ["Name", "name", "id", "ID", "indicator_key", "symbol"]:
        if candidate in headers:
            name_field = candidate
            break
    if not name_field:
        # fallback to first header
        name_field = headers[0]

    for row in rows:
        rel = row["new_rel_path"].replace("\\", "/")
        file_name = row["file_name"]
        if not rel.lower().endswith(".csv"):
            # Do not attempt to import non-CSV into rows; these will be handled as separate files.
            continue
        path = repo_root / rel
        if not path.is_file():
            print("WARN: CSV file missing during import:", path, file=sys.stderr)
            continue

        print("  importing from", path)
        with path.open(encoding=ENC, newline="") as f:
            reader = csv.DictReader(f)
            for idx, r in enumerate(reader, start=1):
                name_val = (r.get(name_field) or "").strip()
                if not name_val:
                    name_val = f"{db_title} row {idx}"

                props: Dict[str, dict] = {
                    "Name": {
                        "title": [
                            {
                                "type": "text",
                                "text": {"content": name_val[:2000]},
                            }
                        ]
                    },
                    "Source_File": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": file_name},
                            }
                        ]
                    },
                    "Source_Row_Index": {"number": idx},
                }

                for col in headers:
                    if col == "Name":
                        continue
                    val = r.get(col)
                    if val is None:
                        continue
                    sval = str(val).strip()
                    if not sval:
                        continue
                    props[col] = {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": sval[:2000]},
                            }
                        ]
                    }

                try:
                    c.pages.create(parent={"database_id": dbid}, properties=props)
                except APIResponseError as e:
                    print(
                        f"ERROR creating page in {db_title} from {file_name} row {idx}: {e}",
                        file=sys.stderr,
                    )


def ensure_legacy_section_page(
    c: Client, legacy_root_id: str, section_title: str
) -> str:
    """Ensure a section page exists under Legacy Deep Spec."""
    kids = list_child_pages(c, legacy_root_id)
    if section_title in kids:
        return kids[section_title]
    p = c.pages.create(
        parent={"type": "page_id", "page_id": legacy_root_id},
        properties={
            "title": {"title": [{"type": "text", "text": {"content": section_title}}]}
        },
    )
    pid = p["id"]
    print("created legacy section:", section_title, pid)
    return pid


def ensure_child_page(c: Client, parent_page_id: str, title: str, content: str) -> None:
    """Create a child page under parent_page_id with a single paragraph if it doesn't already exist."""
    kids = list_child_pages(c, parent_page_id)
    if title in kids:
        return
    c.pages.create(
        parent={"type": "page_id", "page_id": parent_page_id},
        properties={"title": {"title": [{"type": "text", "text": {"content": title}}]}},
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": content[:1900] or "(empty)"},
                        }
                    ]
                },
            }
        ],
    )
    print("  created legacy child page:", title)


def main() -> None:
    repo_root = Path(".").resolve()

    # Safety checks
    m = load_map()
    hub = m.get("hub_page_id")
    if not hub:
        fail("hub_page_id missing in map; run build_workspace_hub_v4.py first.")

    c = get_client()

    # 1) Ensure section pages
    sections = ensure_section_pages(c, hub)
    print("IFNS sections:", sections)

    # 2) Parse targets
    tables, docs, files = parse_targets()
    table_groups = group_by_db_target(tables)
    doc_groups = group_docs(docs)

    # 3) Handle DB targets (tables)
    for (parent_name, target_name), rows in table_groups.items():
        section_page_id = sections.get(parent_name)
        if not section_page_id:
            print(
                f"WARN: parent page {parent_name!r} not in sections; skipping {target_name}",
                file=sys.stderr,
            )
            continue

        # Build database title from target_name (keep it English & concise)
        db_title = target_name.replace("_", " ")
        headers = load_csv_headers(repo_root, rows)
        dbid = ensure_ifns_db(c, m, section_page_id, target_name, db_title, headers)

        # Only import if DB is empty (idempotent-ish)
        if db_has_rows(c, dbid):
            print("DB already has rows; skipping import for", db_title, dbid)
            continue

        print("Importing rows into", db_title, "(", target_name, ")")
        import_csv_into_db(c, dbid, db_title, repo_root, rows, headers)

    # 4) Handle legacy docs (pages)
    # Find legacy root
    legacy_root = sections.get("IFNS – Legacy Deep Spec")
    if not legacy_root:
        print("WARN: Legacy Deep Spec root not found; skipping docs.", file=sys.stderr)
    else:
        for (parent_name, section_title), rows in doc_groups.items():
            # parent_name should always be "IFNS – Legacy Deep Spec"
            section_page_id = ensure_legacy_section_page(c, legacy_root, section_title)
            for row in rows:
                rel = row["new_rel_path"].replace("\\", "/")
                path = repo_root / rel
                if not path.is_file():
                    print("WARN: missing doc file:", path, file=sys.stderr)
                    continue
                # derive a page title from file_name (strip extension, replace underscores)
                file_name = row["file_name"]
                base = os.path.splitext(file_name)[0]
                title = base.replace("_", " ")
                with path.open(encoding=ENC) as f:
                    content = f.read()
                ensure_child_page(c, section_page_id, title, content)

    # 5) Handle file targets (runtime schemas etc.)
    for row in files:
        parent_name = row["notion_parent_page"]
        section_page_id = sections.get(parent_name)
        if not section_page_id:
            print(
                f"WARN: parent page {parent_name!r} not in sections; skipping file {row['file_name']}",
                file=sys.stderr,
            )
            continue
        rel = row["new_rel_path"].replace("\\", "/")
        path = repo_root / rel
        if not path.is_file():
            print("WARN: missing file asset:", path, file=sys.stderr)
            continue
        file_name = row["file_name"]
        title = os.path.splitext(file_name)[0].replace("_", " ")
        with path.open(encoding=ENC, errors="ignore") as f:
            content = f.read()
        ensure_child_page(c, section_page_id, title, content)

    # 6) Save updated map (with new DB ids)
    save_map(m)
    print("ifns_seed_assets: PASS")


if __name__ == "__main__":
    main()
