#!/usr/bin/env python3
import json
import pathlib

p = pathlib.Path(".vscode") / "tasks.json"
p.parent.mkdir(parents=True, exist_ok=True)
base = {"version": "2.0.0", "tasks": []}
if p.exists():
    try:
        base = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        pass
tasks = base.setdefault("tasks", [])


def upsert(label, command):
    for t in tasks:
        if t.get("label") == label:
            t["type"] = "shell"
            t["command"] = command
            return
    tasks.append({"label": label, "type": "shell", "command": command})


upsert(
    "Export & Commit mirrors",
    "powershell -ExecutionPolicy Bypass -File .\\scripts\\export_and_commit.ps1",
)
upsert(
    "Verify SoT Pages",
    'powershell -ExecutionPolicy Bypass -File .\\scripts\\run_and_capture.ps1 -Command "python .\\scripts\\check_sot_landing.py" -Tag "check_sot"',
)

p.write_text(json.dumps(base, indent=2), encoding="utf-8")
print("tasks updated")
