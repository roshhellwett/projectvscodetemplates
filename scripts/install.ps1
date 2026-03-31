# ProjectVSCode Presets Installer for Windows
# PowerShell script

param(
    [string]$Preset = "",
    [switch]$List = $false,
    [switch]$Help = $false,
    [switch]$Version = $false
)

$InstallerVersion = "1.0.0"
$GITHUB_REPO = "zenithopensourceprojects/projectvscodetemplates"
$INSTALL_URL = "https://raw.githubusercontent.com/$GITHUB_REPO/main/scripts/install.ps1"
$ScriptDir = $PSScriptRoot

function Show-Help {
    Write-Host ""
    Write-Host "ProjectVSCode Presets Installer" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: install.ps1 [-Preset <name>] [-List] [-Help] [-Version]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Preset <name>    Install a specific preset"
    Write-Host "  -List            Show all available presets"
    Write-Host "  -Help            Show this help message"
    Write-Host "  -Version         Show version"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\install.ps1 -Preset python-beginner"
    Write-Host "  .\install.ps1 -List"
    Write-Host ""
}

function Show-Version {
    Write-Host "ProjectVSCode Presets Installer v$InstallerVersion"
}

function Show-Presets {
    $manifestFile = Join-Path $ScriptDir "..\presets\manifest.json"

    if (Test-Path $manifestFile) {
        Write-Host ""
        Write-Host "Available Presets:" -ForegroundColor Cyan
        Write-Host ""

        $data = Get-Content $manifestFile | ConvertFrom-Json
        foreach ($preset in $data.presets) {
            $desc = $preset.description
            if ($desc.Length -gt 50) { $desc = $desc.Substring(0, 50) + "..." }
            Write-Host "  $($preset.id.PadRight(30)) - $desc"
            Write-Host "    Category: $($preset.category.PadRight(15)) Difficulty: $($preset.difficulty)"
            Write-Host ""
        }
    } else {
        Write-Host "Fetching preset list from GitHub..." -ForegroundColor Yellow
        try {
            $response = Invoke-WebRequest -Uri "https://raw.githubusercontent.com/$GITHUB_REPO/main/presets/manifest.json" -UseBasicParsing
            $data = $response.Content | ConvertFrom-Json
            Write-Host ""
            Write-Host "Available Presets:" -ForegroundColor Cyan
            Write-Host ""
            foreach ($preset in $data.presets) {
                $desc = $preset.description
                if ($desc.Length -gt 50) { $desc = $desc.Substring(0, 50) + "..." }
                Write-Host "  $($preset.id.PadRight(30)) - $desc"
                Write-Host "    Category: $($preset.category.PadRight(15)) Difficulty: $($preset.difficulty)"
                Write-Host ""
            }
        } catch {
            Write-Host "Could not fetch presets. Check your internet connection." -ForegroundColor Red
        }
    }
}

function Get-VSCodeConfigDir {
    return Join-Path $env:APPDATA "Code\User"
}

function Backup-Existing {
    param([string]$File)

    if (Test-Path $File) {
        $timestamp = Get-Date -Format "yyyy-MM-dd-HHmmss"
        $backup = "$File.backup.$timestamp"
        Copy-Item $File $backup -Force
        Write-Host "Backed up existing file to: $backup" -ForegroundColor Yellow
    }
}

function Install-Preset {
    param([string]$PresetId)

    Write-Host ""
    Write-Host "Installing preset: $PresetId" -ForegroundColor Cyan

    $localPreset = Join-Path $ScriptDir "..\presets\$PresetId"
    $remoteUrl = "https://raw.githubusercontent.com/$GITHUB_REPO/main/presets/$PresetId"

    $presetPath = $null
    $isRemote = $false

    if (Test-Path $localPreset) {
        $presetPath = $localPreset
        Write-Host "Using local preset..." -ForegroundColor Yellow
    } else {
        try {
            $response = Invoke-WebRequest -Uri "$remoteUrl/settings.json" -UseBasicParsing -Method Head
            if ($response.StatusCode -eq 200) {
                $presetPath = $remoteUrl
                $isRemote = $true
                Write-Host "Using remote preset from GitHub..." -ForegroundColor Yellow
            }
        } catch {
            Write-Host "Preset not found locally or remotely." -ForegroundColor Red
            Write-Host "Run 'install.ps1 -List' to see available presets." -ForegroundColor Yellow
            exit 1
        }
    }

    $configDir = Get-VSCodeConfigDir
    Write-Host ""
    Write-Host "VS Code config directory: $configDir" -ForegroundColor Cyan
    Write-Host ""

    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        Write-Host "Created config directory." -ForegroundColor Yellow
    }

    Write-Host "Installing settings..." -ForegroundColor Cyan
    Backup-Existing (Join-Path $configDir "settings.json")

    if ($isRemote) {
        Invoke-WebRequest -Uri "$presetPath/settings.json" -OutFile (Join-Path $configDir "settings.json") -UseBasicParsing
    } else {
        Copy-Item (Join-Path $presetPath "settings.json") $configDir -Force
    }
    Write-Host "settings.json installed" -ForegroundColor Green

    Write-Host ""
    Write-Host "Installing extensions..." -ForegroundColor Cyan
    Backup-Existing (Join-Path $configDir "extensions.json")

    if ($isRemote) {
        Invoke-WebRequest -Uri "$presetPath/extensions.json" -OutFile (Join-Path $configDir "extensions.json") -UseBasicParsing
    } else {
        Copy-Item (Join-Path $presetPath "extensions.json") $configDir -Force
    }
    Write-Host "extensions.json installed" -ForegroundColor Green

    Write-Host ""
    Write-Host "Installing keybindings..." -ForegroundColor Cyan
    Backup-Existing (Join-Path $configDir "keybindings.json")

    if ($isRemote) {
        Invoke-WebRequest -Uri "$presetPath/keybindings.json" -OutFile (Join-Path $configDir "keybindings.json") -UseBasicParsing
    } else {
        Copy-Item (Join-Path $presetPath "keybindings.json") $configDir -Force
    }
    Write-Host "keybindings.json installed" -ForegroundColor Green

    $snippetsDir = Join-Path $configDir "snippets"
    if (-not (Test-Path $snippetsDir)) {
        New-Item -ItemType Directory -Path $snippetsDir -Force | Out-Null
    }

    if ($isRemote) {
        $snippetsFile = Join-Path $snippetsDir "$PresetId.code-snippets"
        try {
            Invoke-WebRequest -Uri "$presetPath/$PresetId.code-snippets" -OutFile $snippetsFile -UseBasicParsing
            Write-Host "Snippets installed" -ForegroundColor Green
        } catch { }
    } elseif (Test-Path (Join-Path $presetPath "$PresetId.code-snippets")) {
        Copy-Item (Join-Path $presetPath "$PresetId.code-snippets") $snippetsDir -Force
        Write-Host "Snippets installed" -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "Installing extensions in VS Code..." -ForegroundColor Cyan

    $extensionsFile = Join-Path $configDir "extensions.json"
    $codeCli = Get-Command code -ErrorAction SilentlyContinue
    if ($codeCli -and (Test-Path $extensionsFile)) {
        $extData = Get-Content $extensionsFile | ConvertFrom-Json
        foreach ($ext in $extData.recommendations) {
            Write-Host "Installing: $ext" -ForegroundColor Yellow
            & $codeCli.Source --install-extension $ext --force 2>$null | Out-Null
            if ($LASTEXITCODE -ne 0) {
                Write-Host "  (requires VS Code restart)" -ForegroundColor Yellow
            }
        }
        Write-Host "Extensions installation initiated" -ForegroundColor Green
    } else {
        Write-Host "VS Code CLI not found. Extensions will be suggested when you open VS Code." -ForegroundColor Yellow
    }

    $global:LASTEXITCODE = 0

    Write-Host ""
    Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   Preset installed: $PresetId                                ║
║                                                              ║
║   Settings: $configDir               ║
║                                                              ║
║   Extensions: See extensions.json                            ║
║                                                              ║
║   Keybindings: Applied                                       ║
║                                                              ║
║   Restart VS Code for all changes to take effect             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Green
    Write-Host ""
}

if ($Help) {
    Show-Help
    exit 0
}

if ($Version) {
    Show-Version
    exit 0
}

if ($List) {
    Show-Presets
    exit 0
}

if ($Preset -ne "") {
    Install-Preset -PresetId $Preset
} else {
    Show-Help
    exit 1
}
