#!/usr/bin/env python3
import os
import json
from notion_client import Client, errors

MAP = r"IFNS_Workspace_DB/config/workspace_companion_map.json"


def load_map():
    # tolerate BOM
    with open(MAP, encoding="utf-8-sig") as f:
        return json.load(f)


def try_update(c, dbid, payloads):
    for idx, props in enumerate(payloads, start=1):
        try:
            c.databases.update(database_id=dbid, properties=props)
            print(f"fixed[{idx}]:", dbid)
            return True
        except errors.APIResponseError as e:
            print(f"try[{idx}] fail:", dbid, e.code, getattr(e, "message", ""))
    return False


def main():
    tok = os.getenv("NOTION_TOKEN")
    dbroot = os.getenv("WORKSPACE_DB_ID")
    assert tok and dbroot, "Missing NOTION_TOKEN/WORKSPACE_DB_ID"
    c = Client(auth=tok)

    m = load_map()
    targets = [
        m.get(k)
        for k in (
            "Admin_Config_Index",
            "Projects",
            "Tasks",
            "Decisions",
            "Approvals",
            "Handover",
        )
    ]
    targets = [t for t in targets if t]

    # 3 payload variants (new, legacy, dual)
    def p_new(dbroot):
        return {
            "Workspace": {
                "type": "relation",
                "relation": {
                    "database_id": dbroot,
                    "type": "single_property",
                    "single_property": {},
                },
            }
        }

    def p_legacy(dbroot):
        return {"Workspace": {"relation": {"database_id": dbroot}}}

    def p_dual(dbroot):
        return {
            "Workspace": {
                "type": "relation",
                "relation": {
                    "database_id": dbroot,
                    "type": "dual_property",
                    "dual_property": {},
                },
            }
        }

    for dbid in targets:
        ok = try_update(c, dbid, [p_new(dbroot), p_legacy(dbroot), p_dual(dbroot)])
        if not ok:
            print("FAILED:", dbid)
    print("done")


if __name__ == "__main__":
    main()
