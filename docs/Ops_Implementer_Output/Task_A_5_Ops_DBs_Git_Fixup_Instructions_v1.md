# Task A – 5 Ops DBs – Git / Pre-commit Fixup (v1)

This short note is for anyone working on **Task A – 5 Ops DBs** in the
`ifns-workspace-db` repo and hitting the **pre-commit trailing whitespace** hook.

The goal: make sure
`docs/Ops_Implementer_Output/Task_A_5_Ops_DBs_Notion_Execution_v2.md`
is **committed and pushed** to `origin/main` cleanly.

---

## 1. What happened

1. The file was copied into the repo at:

   ```text
   docs/Ops_Implementer_Output/Task_A_5_Ops_DBs_Notion_Execution_v2.md
   ```

2. `git add` and `git commit` were run.

3. The **pre-commit** hook `trim trailing whitespace` fired, found some
   trailing spaces in that file, and **fixed** them automatically.

4. Because a hook modified a file, the commit was **aborted** with a message
   similar to:

   > trim trailing whitespace … Failed
   > files were modified by this hook

5. At that point the file on disk was corrected, but **no commit** was created.

The fix is simply to re-add the corrected file and commit again.

---

## 2. Commands to finish the commit

Run these from **PowerShell** inside VS Code.

```powershell
# 1) Go to the repo root
cd E:\GitHub\ifns-workspace-db

# 2) Check current status (for your own awareness)
git status

# 3) Stage ONLY the Task A execution guide
git add .\docs\Ops_Implementer_Output\Task_A_5_Ops_DBs_Notion_Execution_v2.md

# 4) Commit again – pre-commit should now pass
git commit -m "Add Task A Ops 5 DBs Notion execution v2 (Registry 2025-11-27)"

# 5) Push to origin/main
git push
```

Notes:

- We **only add this one file** to avoid mixing Task A with other local work.
- If pre-commit passes, `git push` will send the new commit to GitHub.
- After this, the file is available to all Notion/Ops agents as part of the repo.
