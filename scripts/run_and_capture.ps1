param(
  [Parameter(Mandatory=$true)][string]$Command,
  [string]$Tag = "run"
)

$ErrorActionPreference = "Continue"
$logs = Join-Path $PSScriptRoot "..\logs"
New-Item -ItemType Directory -Force $logs | Out-Null

$ts   = Get-Date -Format "yyyyMMdd_HHmmss"
$base = "$Tag`_$ts"
$full = Join-Path $logs "$base`_full.log"
$sum  = Join-Path $logs "$base`_summary.md"
$last = Join-Path $logs "last_summary.md"

$start = Get-Date
# run the command via cmd to capture a proper exit code for external tools
$null = & cmd /c "$Command" 2>&1 | Tee-Object -FilePath $full
$code  = $LASTEXITCODE
$stop  = Get-Date
$dur   = ("{0:n1}s" -f ($stop-$start).TotalSeconds)

# extract signal (errors/warnings/tracebacks)
$regex = '(?i)(ERROR|Exception|Traceback|HTTPStatusError|APIResponseError|permission|Forbidden|NotFound|Could not find database|Missing NOTION_TOKEN|Missing WORKSPACE_DB_ID|4\d{2}|KeyError|AttributeError|ValueError|TypeError)'
$hits  = Select-String -Path $full -Pattern $regex | Select-Object -ExpandProperty Line -Unique
$tail  = Get-Content $full -Tail 40

# write summary
@"
# IFNS run summary

**Command:** $Command
**Exit code:** $code
**Duration:** $dur
**Full log:** logs/$($base)_full.log

## Signals
$([string]::Join("`n", ($hits | ForEach-Object { "- $_" })))

## Last 40 lines
"@ | Set-Content -Encoding UTF8 $sum

Copy-Item $sum $last -Force

# auto-append to the Error Ledger on failure (uses existing helper if present)
if ($code -ne 0 -and (Test-Path ".\scripts\append_ledger.py")) {
  @"
Command: $Command
Exit: $code
See: logs/$($base)_full.log
Key lines:
$([string]::Join("`n", ($hits | Select-Object -First 10)))
"@ | python .\scripts\append_ledger.py | Out-Null
}

Write-Host "Summary   $sum"
Write-Host "Full log  $full"
exit $code
