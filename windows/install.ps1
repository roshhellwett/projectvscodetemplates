param(
    [string]$Preset = "",
    [switch]$List = $false,
    [switch]$Help = $false,
    [switch]$Version = $false,
    [switch]$Interactive = $false,
    [switch]$NoPause = $false
)

$ErrorActionPreference = "Stop"

$InstallerVersion = "1.0.0"
$RepoSlug = "zenithopensourceprojects/projectvscodetemplates"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$LocalManifestPath = Join-Path $ProjectRoot "presets\manifest.json"

function Write-Section {
    param([string]$Message)
    Write-Host ""
    Write-Host "== $Message ==" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    Write-Host "[!] $Message" -ForegroundColor Yellow
}

function Write-ErrorLine {
    param([string]$Message)
    Write-Host "[X] $Message" -ForegroundColor Red
}

function Pause-ForUser {
    if (-not $NoPause) {
        Write-Host ""
        Read-Host "Press Enter to continue"
    }
}

function Get-ManifestData {
    if (Test-Path $LocalManifestPath) {
        return Get-Content $LocalManifestPath -Raw | ConvertFrom-Json
    }

    $remoteManifest = "https://raw.githubusercontent.com/$RepoSlug/main/presets/manifest.json"
    return Invoke-RestMethod -Uri $remoteManifest
}

function Get-PresetMap {
    $manifest = Get-ManifestData
    $map = @{}
    foreach ($item in $manifest.presets) {
        $map[$item.id] = $item
    }
    return $map
}

function Show-Help {
    Write-Host ""
    Write-Host "Project VsCode Templates - Windows Installer" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  .\install.ps1 -Interactive"
    Write-Host "  .\install.ps1 -Preset python-beginner"
    Write-Host "  .\install.ps1 -List"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Interactive    Launch the guided installer menu"
    Write-Host "  -Preset <id>    Install a preset directly"
    Write-Host "  -List           Show all preset ids"
    Write-Host "  -Version        Show installer version"
    Write-Host "  -Help           Show this message"
    Write-Host ""
}

function Show-Version {
    Write-Host "Project VsCode Templates Windows Installer v$InstallerVersion"
}

function Show-Presets {
    $manifest = Get-ManifestData
    Write-Section "Available Presets"

    foreach ($preset in $manifest.presets) {
        Write-Host ("{0,-28}  {1}" -f $preset.id, $preset.name) -ForegroundColor White
        Write-Host ("  {0} | {1} | {2}" -f $preset.category, $preset.difficulty, $preset.description) -ForegroundColor DarkGray
        Write-Host ""
    }
}

function Get-VSCodeConfigDir {
    return Join-Path $env:APPDATA "Code\User"
}

function Backup-File {
    param([string]$Path)

    if (Test-Path $Path) {
        $stamp = Get-Date -Format "yyyy-MM-dd-HHmmss"
        $backup = "$Path.backup.$stamp"
        Copy-Item -LiteralPath $Path -Destination $backup -Force
        Write-Warn "Backed up existing file to $backup"
    }
}

function Resolve-PresetSource {
    param([string]$PresetId)

    $localPath = Join-Path $ProjectRoot "presets\$PresetId"
    if (Test-Path $localPath) {
        return @{
            IsRemote = $false
            BasePath = $localPath
        }
    }

    $remoteBase = "https://raw.githubusercontent.com/$RepoSlug/main/presets/$PresetId"
    try {
        Invoke-WebRequest -Uri "$remoteBase/settings.json" -UseBasicParsing -Method Head | Out-Null
        return @{
            IsRemote = $true
            BasePath = $remoteBase
        }
    } catch {
        throw "Preset '$PresetId' was not found locally or on GitHub."
    }
}

function Copy-PresetFile {
    param(
        [hashtable]$Source,
        [string]$SourceName,
        [string]$DestinationPath
    )

    if ($Source.IsRemote) {
        Invoke-WebRequest -Uri "$($Source.BasePath)/$SourceName" -OutFile $DestinationPath -UseBasicParsing
    } else {
        Copy-Item -LiteralPath (Join-Path $Source.BasePath $SourceName) -Destination $DestinationPath -Force
    }
}

function Install-ExtensionsFromFile {
    param([string]$ExtensionsPath)

    $codeCmd = Get-Command code -ErrorAction SilentlyContinue
    if (-not $codeCmd) {
        Write-Warn "VS Code CLI ('code') was not found. Open VS Code later and install the recommended extensions from extensions.json."
        return
    }

    try {
        $extensions = (Get-Content $ExtensionsPath -Raw | ConvertFrom-Json).recommendations
    } catch {
        Write-Warn "Could not parse extensions.json. Skipping automatic extension install."
        return
    }

    if (-not $extensions) {
        Write-Warn "No recommended extensions were found for this preset."
        return
    }

    Write-Section "Installing Recommended Extensions"
    foreach ($extension in $extensions) {
        Write-Host "Installing $extension..." -ForegroundColor Yellow
        & $codeCmd.Source --install-extension $extension --force 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "$extension installed"
        } else {
            Write-Warn "$extension could not be installed automatically. VS Code may need to be restarted."
        }
    }
}

function Install-Preset {
    param([string]$PresetId)

    $presetMap = Get-PresetMap
    if (-not $presetMap.ContainsKey($PresetId)) {
        throw "Preset '$PresetId' is not listed in presets/manifest.json."
    }

    $preset = $presetMap[$PresetId]
    $source = Resolve-PresetSource -PresetId $PresetId
    $configDir = Get-VSCodeConfigDir
    $snippetsDir = Join-Path $configDir "snippets"

    Write-Section "Installing $($preset.name)"
    Write-Host $preset.description -ForegroundColor White
    Write-Host "Target folder: $configDir" -ForegroundColor DarkGray

    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        Write-Success "Created VS Code User folder"
    }

    if (-not (Test-Path $snippetsDir)) {
        New-Item -ItemType Directory -Path $snippetsDir -Force | Out-Null
    }

    $files = @(
        @{ Name = "settings.json"; Destination = Join-Path $configDir "settings.json" },
        @{ Name = "extensions.json"; Destination = Join-Path $configDir "extensions.json" },
        @{ Name = "keybindings.json"; Destination = Join-Path $configDir "keybindings.json" }
    )

    foreach ($file in $files) {
        Backup-File -Path $file.Destination
        Copy-PresetFile -Source $source -SourceName $file.Name -DestinationPath $file.Destination
        Write-Success "$($file.Name) installed"
    }

    $snippetFile = "$PresetId.code-snippets"
    $snippetDestination = Join-Path $snippetsDir $snippetFile
    try {
        Copy-PresetFile -Source $source -SourceName $snippetFile -DestinationPath $snippetDestination
        Write-Success "$snippetFile installed"
    } catch {
        Write-Warn "No snippets file was installed for this preset."
    }

    Install-ExtensionsFromFile -ExtensionsPath (Join-Path $configDir "extensions.json")

    Write-Section "Finished"
    Write-Success "Preset '$PresetId' is ready."
    Write-Host "Restart VS Code if it was already open." -ForegroundColor White
}

function Read-Choice {
    param(
        [string]$Prompt,
        [int]$Min,
        [int]$Max
    )

    while ($true) {
        $value = Read-Host $Prompt
        if ($value -match '^\d+$') {
            $number = [int]$value
            if ($number -ge $Min -and $number -le $Max) {
                return $number
            }
        }
        Write-ErrorLine "Please enter a number between $Min and $Max."
    }
}

function Ask-Menu {
    param(
        [string]$Title,
        [string[]]$Options
    )

    Write-Host ""
    Write-Host $Title -ForegroundColor Cyan
    for ($i = 0; $i -lt $Options.Count; $i++) {
        Write-Host ("  {0}. {1}" -f ($i + 1), $Options[$i]) -ForegroundColor White
    }
    return Read-Choice -Prompt "Choose an option" -Min 1 -Max $Options.Count
}

function Get-GuidedPreset {
    $track = Ask-Menu -Title "What do you mainly do in VS Code?" -Options @(
        "Python or data science",
        "Frontend web development",
        "Full-stack web development",
        "C or C++",
        "Competitive programming",
        "Java",
        "Rust or Go",
        "Mobile with Flutter",
        "DevOps or cloud work",
        "Writing, notes, and minimal setup"
    )

    $experience = Ask-Menu -Title "Which experience level fits you best?" -Options @(
        "Complete beginner",
        "Learning and building projects",
        "Working professional"
    )

    $style = Ask-Menu -Title "What matters most in your setup?" -Options @(
        "Balanced everyday coding",
        "Minimal and distraction-free",
        "Streaming or recording",
        "Remote SSH work"
    )

    switch ($track) {
        1 {
            if ($style -eq 2) { return "minimal-zen" }
            if ($style -eq 3) { return "streamer-content-creator" }
            if ($experience -eq 1) { return "python-beginner" }
            if ($experience -eq 2) { return "data-science" }
            return "python-professional"
        }
        2 {
            if ($experience -eq 3) { return "web-dev-fullstack" }
            return "web-dev-frontend"
        }
        3 { return "web-dev-fullstack" }
        4 { return "c-cpp-systems" }
        5 { return "competitive-programming" }
        6 { return "java-student" }
        7 {
            $language = Ask-Menu -Title "Pick the language you want the preset for." -Options @("Rust", "Go")
            if ($language -eq 1) { return "rust-systems" }
            return "go-backend"
        }
        8 { return "mobile-flutter" }
        9 {
            if ($style -eq 4) { return "remote-ssh-server" }
            return "devops-cloud"
        }
        10 {
            if ($style -eq 3) { return "streamer-content-creator" }
            if ($style -eq 4) { return "remote-ssh-server" }
            return "minimal-zen"
        }
        default { return "python-beginner" }
    }
}

function Start-InteractiveInstaller {
    while ($true) {
        Clear-Host
        Write-Host "Project VsCode Templates" -ForegroundColor Cyan
        Write-Host "Friendly Windows installer for VS Code presets" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "1. Guided setup"
        Write-Host "2. Install by preset id"
        Write-Host "3. Show all presets"
        Write-Host "4. Exit"

        $menuChoice = Read-Choice -Prompt "Select an option" -Min 1 -Max 4

        switch ($menuChoice) {
            1 {
                $presetId = Get-GuidedPreset
                $preset = (Get-PresetMap)[$presetId]
                Write-Section "Recommended Preset"
                Write-Host "$($preset.name) [$presetId]" -ForegroundColor Green
                Write-Host $preset.description -ForegroundColor White
                $confirm = Read-Host "Install this preset now? (Y/n)"
                if ($confirm -notmatch '^[Nn]') {
                    Install-Preset -PresetId $presetId
                }
                Pause-ForUser
            }
            2 {
                $chosenPreset = Read-Host "Enter the preset id"
                if ([string]::IsNullOrWhiteSpace($chosenPreset)) {
                    Write-Warn "No preset id entered."
                } else {
                    Install-Preset -PresetId $chosenPreset.Trim()
                }
                Pause-ForUser
            }
            3 {
                Show-Presets
                Pause-ForUser
            }
            4 {
                return
            }
        }
    }
}

$shouldLaunchInteractive = $Interactive -or (
    [string]::IsNullOrWhiteSpace($Preset) -and -not $List -and -not $Help -and -not $Version
)

try {
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

    if (-not [string]::IsNullOrWhiteSpace($Preset)) {
        Install-Preset -PresetId $Preset.Trim()
        exit 0
    }

    if ($shouldLaunchInteractive) {
        Start-InteractiveInstaller
        exit 0
    }

    Show-Help
    exit 1
} catch {
    Write-ErrorLine $_.Exception.Message
    if ($shouldLaunchInteractive) {
        Pause-ForUser
    }
    exit 1
}
