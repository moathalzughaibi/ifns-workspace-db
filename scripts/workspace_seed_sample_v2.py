#!/usr/bin/env python3
import os
import json
from notion_client import Client

ENC = "utf-8-sig"
MAP = "IFNS_Workspace_DB/config/workspace_companion_map.json"


def t(s):
    return [{"type": "text", "text": {"content": s}}]


def find_title_key(props):
    for k, p in props.items():
        if p.get("type") == "title":
            return k
    return "Name"


def find_status_key(props):
    # prefer literal "Status" if exists, else first status/select prop
    if "Status" in props:
        return "Status"
    for k, p in props.items():
        if p.get("type") in ("status", "select"):
            return k
    return None


def find_relation_to(props, target_db_id):
    # find a relation prop that points to target_db_id
    for k, p in props.items():
        if p.get("type") == "relation":
            rel = p.get("relation") or {}
            if rel.get("database_id") == target_db_id:
                return k
    return None


def main():
    c = Client(auth=os.environ["NOTION_TOKEN"])
    m = json.load(open(MAP, "r", encoding=ENC))

    P = m["Projects"]
    T = m["Tasks"]
    D = m["Decisions"]
    A = m["Approvals"]
    H = m["Handover"]

    # Introspect each DB
    proj_db = c.databases.retrieve(P)
    proj_props = proj_db.get("properties", {})
    task_db = c.databases.retrieve(T)
    task_props = task_db.get("properties", {})
    dec_db = c.databases.retrieve(D)
    dec_props = dec_db.get("properties", {})
    appr_db = c.databases.retrieve(A)
    appr_props = appr_db.get("properties", {})
    hand_db = c.databases.retrieve(H)
    hand_props = hand_db.get("properties", {})

    # Resolve keys
    proj_title = find_title_key(proj_props)
    proj_status = find_status_key(proj_props)

    task_title = find_title_key(task_props)
    task_status = find_status_key(task_props)
    task_proj_rel = find_relation_to(task_props, P)

    dec_title = find_title_key(dec_props)
    # dec_status = (unused)

    appr_title = find_title_key(appr_props)
    # appr_status = (unused)

    hand_title = find_title_key(hand_props)
    hand_status = find_status_key(hand_props)

    # Create one Project
    p_props = {proj_title: {"title": t("IFNS  Workspace bring-up")}}
    if proj_status:
        p_props[proj_status] = {"select": {"name": "Active"}}
    p = c.pages.create(parent={"database_id": P}, properties=p_props)
    pid = p["id"]

    # Create one Task linked to the Project
    t_props = {task_title: {"title": t("Wire saved views & seed exporter")}}
    if task_status:
        t_props[task_status] = {"select": {"name": "Doing"}}
    if task_proj_rel:
        t_props[task_proj_rel] = {"relation": [{"id": pid}]}
    c.pages.create(parent={"database_id": T}, properties=t_props)

    # One Decision
    d_props = {dec_title: {"title": t("Set SoT = Notion")}}
    c.pages.create(parent={"database_id": D}, properties=d_props)

    # One Approval
    a_props = {appr_title: {"title": t("Approve workspace structure")}}
    c.pages.create(parent={"database_id": A}, properties=a_props)

    # One Handover
    h_props = {hand_title: {"title": t("Workspace handover packet")}}
    if hand_status:
        h_props[hand_status] = {"select": {"name": "Draft"}}
    c.pages.create(parent={"database_id": H}, properties=h_props)

    print("Seeded demo rows using introspected keys.")


if __name__ == "__main__":
    main()
