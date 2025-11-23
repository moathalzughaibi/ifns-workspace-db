$ErrorActionPreference = "Stop"
if (-not (Test-Path .\.venv\Scripts\python.exe)) { throw "venv not active" }
$req = (Get-Content .\.venv\Lib\site-packages\pip\_vendor\__init__.py -ErrorAction SilentlyContinue) | Out-Null
pip freeze | Set-Content -Encoding utf8 .\requirements.lock
pip freeze | Set-Content -Encoding utf8 .\requirements.txt
Write-Host "Pinned current environment to requirements.lock and requirements.txt"
