@echo off
setlocal
set SCRIPT_DIR=%~dp0

if not exist "%SCRIPT_DIR%install.ps1" (
    echo Windows installer not found at "%SCRIPT_DIR%install.ps1"
    exit /b 1
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%install.ps1" -Interactive
set EXIT_CODE=%ERRORLEVEL%
endlocal & exit /b %EXIT_CODE%
