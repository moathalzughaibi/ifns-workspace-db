#!/usr/bin/env python3
import sys
import pathlib
import datetime

p = pathlib.Path("docs/IFNS_Error_Ledger.md")
p.parent.mkdir(parents=True, exist_ok=True)
ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
body = sys.stdin.read().strip()
entry = f"## [{ts}] Automated note\n\n{body}\n"
p.write_text(
    p.read_text(encoding="utf-8") + ("\n" if p.exists() else "") + entry,
    encoding="utf-8",
)
print("Appended to", p)
