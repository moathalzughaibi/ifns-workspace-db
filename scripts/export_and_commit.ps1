param(
  [switch]$Push = $true
)
$ErrorActionPreference = "Stop"

# run exporter
python .\scripts\export_workspace_companions.py

# stage CSV mirrors (and ledger if changed)
git add sync/workspace/*.csv 2>$null
if (Test-Path .\docs\IFNS_Error_Ledger.md) { git add .\docs\IFNS_Error_Ledger.md }

# commit with timestamp if there are changes
$diff = git status --porcelain
if (-not [string]::IsNullOrWhiteSpace($diff)) {
  $ts = Get-Date -Format "yyyy-MM-dd HH:mm"
  git commit -m "Export mirrors ($ts)"
  if ($Push) { git push }
  Write-Host "Committed & pushed: Export mirrors ($ts)"
} else {
  Write-Host "No mirror changes to commit."
}
