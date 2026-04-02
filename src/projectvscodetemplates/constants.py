"""Constants and configuration values for ProjectVSCodeTemplates."""

import os
import platform
from pathlib import Path
from typing import Final

PACKAGE_NAME: Final[str] = "projectvscodetemplates"
PACKAGE_VERSION: Final[str] = "1.0.0"
PACKAGE_AUTHOR: Final[str] = "Roshan Kr Singh"
PACKAGE_EMAIL: Final[str] = "roshankumar77630@gmail.com"

IS_WINDOWS: Final[bool] = platform.system() == "Windows"
IS_LINUX: Final[bool] = platform.system() == "Linux"
IS_MACOS: Final[bool] = platform.system() == "Darwin"

VSCODE_CONFIG_SUBDIR: Final[str] = "User"


def get_vscode_config_dir() -> Path:
    """Get VS Code user configuration directory based on OS."""
    if IS_WINDOWS:
        appdata = os.getenv("APPDATA", "")
        if not appdata:
            raise RuntimeError("APPDATA environment variable not set")
        return Path(appdata) / "Code" / VSCODE_CONFIG_SUBDIR
    elif IS_LINUX:
        xdg_config = os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        return Path(xdg_config) / "Code" / VSCODE_CONFIG_SUBDIR
    elif IS_MACOS:
        return Path.home() / "Library" / "Application Support" / "Code" / VSCODE_CONFIG_SUBDIR
    else:
        raise OSError(f"Unsupported platform: {platform.system()}")


def get_vscode_snippets_dir() -> Path:
    """Get VS Code snippets directory based on OS."""
    return get_vscode_config_dir() / "snippets"


BACKUP_DIR_NAME: Final[str] = "projectvscodetemplates_backups"
CACHE_DIR_NAME: Final[str] = "projectvscodetemplates_cache"
INSTALLED_INFO_FILE: Final[str] = ".projectvscodetemplates_installed.json"


def get_backup_dir() -> Path:
    """Get backup directory path."""
    try:
        base = get_vscode_config_dir()
        return base / BACKUP_DIR_NAME
    except RuntimeError:
        fallback = Path.home() / ".config" / "Code" / VSCODE_CONFIG_SUBDIR
        return fallback / BACKUP_DIR_NAME


def get_cache_dir() -> Path:
    """Get cache directory path."""
    if IS_WINDOWS:
        base = Path(os.getenv("LOCALAPPDATA", os.getenv("TEMP", "")))
    else:
        base = Path(os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache")))
    return base / CACHE_DIR_NAME


def get_installed_info_path() -> Path:
    """Get path to installed preset info file."""
    return get_vscode_config_dir() / INSTALLED_INFO_FILE


VSCODE_SETTINGS_FILE: Final[str] = "settings.json"
VSCODE_KEYBINDINGS_FILE: Final[str] = "keybindings.json"
VSCODE_EXTENSIONS_FILE: Final[str] = "extensions.json"

PRESET_MANIFEST_FILE: Final[str] = "manifest.json"

DIFFICULTY_LEVELS: Final[dict[str, int]] = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3,
}

DIFFICULTY_COLORS: Final[dict[str, str]] = {
    "beginner": "green",
    "intermediate": "yellow",
    "advanced": "red",
}

DIFFICULTY_DESCRIPTIONS: Final[dict[str, str]] = {
    "beginner": "New to programming or VS Code",
    "intermediate": "Comfortable with coding basics",
    "advanced": "Experienced developer or power user",
}

CATEGORIES: Final[list[str]] = ["student", "professional", "lifestyle"]

TRACKS: Final[list[str]] = [
    "learning",
    "career",
    "dsa",
    "frontend",
    "fullstack",
    "systems",
    "data",
    "devops",
    "mobile",
    "backend",
    "writing",
    "streaming",
    "remote",
]

MENU_WIDTH: Final[int] = 45
PANEL_WIDTH: Final[int] = 60
PANEL_BORDER_COLOR: Final[str] = "cyan"

INFO_COLOR: Final[str] = "cyan"
SUCCESS_COLOR: Final[str] = "green"
WARNING_COLOR: Final[str] = "yellow"
ERROR_COLOR: Final[str] = "red"
DEBUG_COLOR: Final[str] = "dim"

SPINNER_STYLE: Final[str] = "dots12"
TABLE_STYLE: Final[str] = "rounded"

TERMINAL_WIDTH_THRESHOLD: Final[int] = 80
MIN_TERMINAL_WIDTH: Final[int] = 60

MAX_DISPLAY_LENGTH: Final[int] = 50
MAX_BACKUPS_TO_KEEP: Final[int] = 10
MAX_SEARCH_RESULTS: Final[int] = 20

INSTALL_TIMEOUT_SECONDS: Final[int] = 120
EXTENSION_INSTALL_TIMEOUT: Final[int] = 60
