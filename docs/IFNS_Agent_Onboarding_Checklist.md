# IFNS Agent Onboarding Checklist (15â€‘Minute Read)

**Read this before touching anything.**

- [ ] I have **Notion** access and the integration **IFNS_Workspace_hup** has Full access to the Teamspace and Hub.
- [ ] I loaded the env in PowerShell: `.\local_env\workspace_env.ps1` (TOKEN and DB show as set).
- [ ] Root DB retrieve PASS (see START HERE Â§3).
- [ ] Hub page retrieve PASS; scratch DB create+delete PASS.
- [ ] I can run `python .\scriptsuild_workspace_hub_v3.py` without errors.
- [ ] I reviewed **SoT Contract** (Notion > Git > Runtime) and will follow it.
- [ ] I understand the **naming** rules for Steps/DBs and where to place pages.
- [ ] I know where the **Error Ledger** lives and how to add a new entry.
- [ ] I will not use heredocs or run Python code directly in PSâ€”only `.py` or `-c` oneâ€‘liners.
- [ ] I will escalate only for permissions/structural blockers, with last 20 log lines attached.

### VS Code tasks (added)
- Export & Commit mirrors
- Verify SoT Pages
