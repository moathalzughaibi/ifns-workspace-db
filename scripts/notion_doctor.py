#!/usr/bin/env python3
import os
import json
import sys
import subprocess
from tenacity import retry, stop_after_attempt, wait_fixed
from notion_client import Client, errors

MAP = r"IFNS_Workspace_DB/config/workspace_companion_map.json"


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    try:
        subprocess.run(
            ["python", "scripts/append_ledger.py"],
            input=msg.encode("utf-8"),
            check=False,
        )
    except Exception:
        pass
    sys.exit(2)


def env_ok():
    if not os.getenv("NOTION_TOKEN"):
        fail("NOTION_TOKEN missing")
    if not os.getenv("WORKSPACE_DB_ID"):
        fail("WORKSPACE_DB_ID missing")


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def _retrieve_db(c, dbid):
    return c.databases.retrieve(dbid)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def _retrieve_page(c, pid):
    return c.pages.retrieve(pid)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def _scratch(c, parent_page_id):
    db = c.databases.create(
        parent={"type": "page_id", "page_id": parent_page_id},
        title=[{"type": "text", "text": {"content": "ZZZ Scratch (delete)"}}],
        properties={"Name": {"title": {}}},
    )
    c.blocks.delete(db["id"])
    return True


def main():
    env_ok()
    c = Client(auth=os.environ["NOTION_TOKEN"])
    root = os.environ["WORKSPACE_DB_ID"]
    try:
        d = _retrieve_db(c, root)
        print("root ok:", d["object"])
    except errors.APIResponseError as e:
        fail(f"Root DB retrieve failed: {e.code} {getattr(e,'message','')}")
    except Exception as e:
        fail(f"Root DB retrieve exception: {e!r}")

    try:
        m = json.load(open(MAP, encoding="utf-8-sig"))
        hub = m["hub_page_id"]
    except Exception as e:
        fail(f"Map read/hub id missing: {e!r}")

    try:
        p = _retrieve_page(c, hub)
        print("hub ok:", p["object"])
        _scratch(c, hub)
        print("scratch ok")
    except errors.APIResponseError as e:
        fail(f"Hub/scratch failed: {e.code} {getattr(e,'message','')}")
    except Exception as e:
        fail(f"Hub/scratch exception: {e!r}")

    print("doctor: PASS")


if __name__ == "__main__":
    main()
