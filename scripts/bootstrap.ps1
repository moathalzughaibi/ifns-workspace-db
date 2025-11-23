param([switch]$CI=$false)
Write-Host ">>> bootstrap: venv + deps + pre-commit"
if (-not (Test-Path .\.venv)) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1
pip install -q --upgrade pip
pip install -q -r requirements.txt
if (-not $CI) {
  pip install -q pre-commit
  pre-commit install
}
Write-Host ">>> done"
