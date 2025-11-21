## [2025-11-21 06:46:14] Notion DB build – Admin DB create failed

**Context:** Workspace hub build (v3), SoT DBs creation.
**Checks:** 
- Env ✅  TOKEN True; DB 2b0b22c770d980578b64eb9a7a394901
- Root DB   oot ok: database
- Hub page   hub: page
- Scratch DB under Hub   db: database then deleted

**Errors:**
- Unexpected Notion response for Admin - Config Index (SoT) (host page  retried under Hub  same result)
- Follow-up verify failed: KeyError: 'db_host_page_id' (map not written because create failed)

**Probable cause:** parent usable (Hub & scratch pass), but databases.create on the Admin DB title hit a Notion edge-case (title/host state). Next action: run the fallback builder that logs the API body and forces hosthub fallback (already prepared).

**Notes:** See full log in chat transcript.
