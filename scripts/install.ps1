$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$target = Join-Path $scriptDir "..\windows\install.ps1"

if (-not (Test-Path $target)) {
    Write-Error "Windows installer not found at $target"
    exit 1
}

& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $target @args
exit $LASTEXITCODE
