param(
    [string]$OutputDir = (Join-Path (Split-Path -Parent $PSScriptRoot) "dist\windows")
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$stagingDir = Join-Path $OutputDir "package"
$sedPath = Join-Path $OutputDir "ProjectVsCodeTemplates-Installer.sed"
$targetExe = Join-Path $OutputDir "ProjectVsCodeTemplates-Installer.exe"

function New-CleanDirectory {
    param([string]$Path)

    if (Test-Path $Path) {
        Remove-Item -LiteralPath $Path -Recurse -Force
    }

    New-Item -ItemType Directory -Path $Path -Force | Out-Null
}

function Copy-Tree {
    param(
        [string]$Source,
        [string]$Destination
    )

    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $Source "*") -Destination $Destination -Recurse -Force
}

New-CleanDirectory -Path $OutputDir
New-CleanDirectory -Path $stagingDir

Copy-Tree -Source (Join-Path $projectRoot "presets") -Destination (Join-Path $stagingDir "presets")
Copy-Tree -Source (Join-Path $projectRoot "windows") -Destination (Join-Path $stagingDir "windows")

$launcherPath = Join-Path $stagingDir "StartInstaller.cmd"
$launcherContent = @"
@echo off
setlocal
set ROOT=%~dp0
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '%ROOT%project-files.zip' -DestinationPath '%ROOT%app' -Force; & '%ROOT%app\windows\install.ps1' -Interactive -NoPause"
endlocal
"@
Set-Content -LiteralPath $launcherPath -Value $launcherContent -Encoding ASCII

$sedContent = @"
[Version]
Class=IEXPRESS
SEDVersion=3
[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=1
HideExtractAnimation=0
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=
DisplayLicense=
FinishMessage=Project VsCode Templates installer closed.
TargetName=$targetExe
FriendlyName=Project VsCode Templates Installer
AppLaunched=StartInstaller.cmd
PostInstallCmd=<None>
AdminQuietInstCmd=
UserQuietInstCmd=
SourceFiles=SourceFiles
[SourceFiles]
SourceFiles0=$stagingDir
[SourceFiles0]
%FILE0%=
%FILE1%=
[Strings]
FILE0=StartInstaller.cmd
FILE1=project-files.zip
"@

# IExpress only packages files that live in the package root. We zip the repo payload, ship that
# archive with the launcher, and the launcher expands it before starting the installer.
$archivePath = Join-Path $stagingDir "project-files.zip"
Compress-Archive -Path (Join-Path $stagingDir "presets"), (Join-Path $stagingDir "windows") -DestinationPath $archivePath -Force

Set-Content -LiteralPath $sedPath -Value $sedContent -Encoding ASCII

Write-Host "Prepared IExpress build files in $OutputDir" -ForegroundColor Green

$iexpress = Get-Command iexpress.exe -ErrorAction SilentlyContinue
if ($iexpress) {
    & $iexpress.Source /N $sedPath | Out-Null
    if (Test-Path $targetExe) {
        Write-Host "Created $targetExe" -ForegroundColor Green
    } else {
        Write-Host "IExpress ran, but the EXE was not created. You can retry manually with the generated SED file." -ForegroundColor Yellow
        Write-Host "  iexpress.exe /N `"$sedPath`"" -ForegroundColor Cyan
    }
} else {
    Write-Host "IExpress is not available on this machine." -ForegroundColor Yellow
    Write-Host "Run this on Windows with IExpress installed:" -ForegroundColor White
    Write-Host "  iexpress.exe /N `"$sedPath`"" -ForegroundColor Cyan
}
