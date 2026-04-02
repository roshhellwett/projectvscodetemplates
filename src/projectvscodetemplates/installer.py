"""VS Code preset installer for ProjectVSCodeTemplates."""

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from projectvscodetemplates.presets import PresetManager, get_preset_manager
from projectvscodetemplates.constants import (
    get_vscode_config_dir,
    get_vscode_snippets_dir,
)


@dataclass
class InstallResult:
    """Result of an installation operation."""

    success: bool
    preset_id: str
    files_copied: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def status_message(self) -> str:
        """Get human-readable status message."""
        if self.success:
            return f"Successfully installed {len(self.files_copied)} file(s)"
        return f"Installation failed with {len(self.errors)} error(s)"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "preset_id": self.preset_id,
            "files_copied": self.files_copied,
            "errors": self.errors,
            "warnings": self.warnings,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class InstalledPresetInfo:
    """Information about an installed preset."""

    preset_id: str
    installed_at: datetime
    preset_name: str | None = None
    version: str | None = None
    files: list[str] = field(default_factory=list)

    @property
    def file_count(self) -> int:
        """Get number of installed files."""
        return len(self.files)


class VSCodeInstaller:
    """Handles installation of VS Code presets with robust error handling."""

    def __init__(self, preset_manager: PresetManager | None = None):
        """Initialize the installer."""
        self.preset_manager = preset_manager or get_preset_manager()
        self._config_dir: Path | None = None
        self._snippets_dir: Path | None = None

    @property
    def config_dir(self) -> Path:
        """Get VS Code config directory lazily."""
        if self._config_dir is None:
            self._config_dir = get_vscode_config_dir()
        return self._config_dir

    @property
    def snippets_dir(self) -> Path:
        """Get VS Code snippets directory lazily."""
        if self._snippets_dir is None:
            self._snippets_dir = get_vscode_snippets_dir()
        return self._snippets_dir

    def _ensure_directories(self) -> tuple[bool, str]:
        """Ensure required directories exist."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)

            if not self.snippets_dir.exists():
                self.snippets_dir.mkdir(parents=True, exist_ok=True)

            return True, ""
        except (OSError, PermissionError) as e:
            return False, f"Cannot create directories: {e}"

    def _get_installed_info_path(self) -> Path:
        """Get path to installed preset info file."""
        return self.config_dir / ".projectvscodetemplates_installed.json"

    def _load_installed_info(self) -> dict[str, Any]:
        """Load installed preset information."""
        info_file = self._get_installed_info_path()

        if info_file.exists():
            try:
                with open(info_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_installed_info(self, info: dict[str, Any]) -> tuple[bool, str]:
        """Save installed preset information."""
        info_file = self._get_installed_info_path()

        try:
            with open(info_file, "w", encoding="utf-8") as f:
                json.dump(info, f, indent=2, default=str)
            return True, ""
        except IOError as e:
            return False, f"Cannot save installation info: {e}"

    def _backup_existing_file(self, file_path: Path) -> tuple[bool, str, Path | None]:
        """Backup an existing file before overwriting."""
        if not file_path.exists():
            return True, "", None

        backup_dir = self.config_dir / "backups"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.bak"
        backup_path = backup_dir / backup_name

        try:
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, backup_path)
            return True, "", backup_path
        except (OSError, IOError) as e:
            return False, f"Backup failed: {e}", None

    def _read_json_file(self, file_name: str) -> dict[str, Any] | None:
        """Read a JSON file safely."""
        file_path = self.config_dir / file_name

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def _write_json_file(
        self,
        file_name: str,
        content: Any,
    ) -> tuple[bool, str]:
        """Write content to a JSON file safely."""
        file_path = self.config_dir / file_name

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(content, f, indent=4, ensure_ascii=False)
            return True, ""
        except IOError as e:
            return False, f"Failed to write {file_name}: {e}"

    def _merge_settings(
        self,
        existing: dict[str, Any] | None,
        new: dict[str, Any],
    ) -> dict[str, Any]:
        """Merge existing settings with new settings."""
        if existing is None:
            return new.copy()

        merged = existing.copy()

        for key, value in new.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key] = {**merged[key], **value}
            elif isinstance(value, list) and key in merged and isinstance(merged[key], list):
                merged[key] = list(set(merged[key] + value))
            else:
                merged[key] = value

        return merged

    def install(
        self,
        preset_id: str,
        create_backup: bool = True,
        install_extensions: bool = True,
        install_snippets: bool = True,
        install_keybindings: bool = True,
    ) -> InstallResult:
        """
        Install a preset to VS Code.

        Args:
            preset_id: ID of the preset to install
            create_backup: Whether to create backup before installing
            install_extensions: Whether to install extensions
            install_snippets: Whether to install snippets
            install_keybindings: Whether to install keybindings

        Returns:
            InstallResult with status and details
        """
        preset = self.preset_manager.get_preset(preset_id)

        if preset is None:
            return InstallResult(
                success=False,
                preset_id=preset_id,
                errors=[f"Preset '{preset_id}' not found"],
            )

        result = InstallResult(success=True, preset_id=preset_id)

        dirs_ok, dir_error = self._ensure_directories()
        if not dirs_ok:
            result.success = False
            result.errors.append(dir_error)
            return result

        if create_backup:
            self._backup_all_settings()

        ok, msg = self._install_settings(preset_id)
        if ok:
            result.files_copied.append(str(self.config_dir / "settings.json"))
        else:
            result.warnings.append(msg)

        if install_keybindings:
            ok, msg = self._install_keybindings(preset_id)
            if ok:
                result.files_copied.append(str(self.config_dir / "keybindings.json"))
            else:
                result.warnings.append(msg)

        if install_extensions:
            ok, msg = self._install_extensions(preset_id)
            if ok:
                result.files_copied.append(str(self.config_dir / "extensions.json"))
            else:
                result.warnings.append(msg)

        if install_snippets:
            ok, msg, files = self._install_snippets(preset_id)
            if ok:
                result.files_copied.extend(files)
            else:
                result.warnings.append(msg)

        info = {
            "preset_id": preset_id,
            "preset_name": preset.name,
            "installed_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "files": result.files_copied,
        }
        self._save_installed_info(info)

        return result

    def _install_settings(self, preset_id: str) -> tuple[bool, str]:
        """Install settings.json for a preset."""
        settings = self.preset_manager.get_settings(preset_id)

        if settings is None:
            return False, "No settings defined for this preset"

        existing = self._read_json_file("settings.json")
        merged = self._merge_settings(existing, settings)

        return self._write_json_file("settings.json", merged)

    def _install_extensions(self, preset_id: str) -> tuple[bool, str]:
        """Install extensions.json for a preset."""
        extension_ids = self.preset_manager.get_extensions(preset_id)

        if not extension_ids:
            return False, "No extensions defined for this preset"

        existing = self._read_json_file("extensions.json")

        merged: dict[str, Any] = {"recommendations": [], "unwantedRecommendations": []}

        if existing:
            existing_rec = set(existing.get("recommendations", []))
            existing_unwanted = set(existing.get("unwantedRecommendations", []))
            merged["recommendations"] = sorted(existing_rec | set(extension_ids))
            merged["unwantedRecommendations"] = sorted(existing_unwanted)
        else:
            merged["recommendations"] = extension_ids
            merged["unwantedRecommendations"] = []

        return self._write_json_file("extensions.json", merged)

    def _install_keybindings(self, preset_id: str) -> tuple[bool, str]:
        """Install keybindings.json for a preset."""
        keybindings = self.preset_manager.get_keybindings(preset_id)

        if keybindings is None:
            return False, "No keybindings defined for this preset"

        existing_content: list[dict[str, Any]] = []
        existing_file = self.config_dir / "keybindings.json"

        if existing_file.exists():
            try:
                with open(existing_file, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    if isinstance(content, list):
                        existing_content = content
            except (json.JSONDecodeError, IOError):
                pass

        if isinstance(keybindings, list):
            merged = existing_content + keybindings
        else:
            merged = existing_content

        return self._write_json_file("keybindings.json", merged)

    def _install_snippets(self, preset_id: str) -> tuple[bool, str, list[str]]:
        """Install code snippets for a preset."""
        snippets = self.preset_manager.get_snippets(preset_id)

        if not snippets:
            return False, "No snippets defined for this preset", []

        installed_files: list[str] = []

        for snippet_name, snippet_file in snippets.items():
            snippet_path = self.snippets_dir / f"{snippet_name}.json"

            try:
                with open(snippet_path, "w", encoding="utf-8") as f:
                    json.dump(snippet_file.content, f, indent=4, ensure_ascii=False)
                installed_files.append(str(snippet_path))
            except IOError:
                continue

        if installed_files:
            return True, f"Installed {len(installed_files)} snippet file(s)", installed_files
        return False, "Failed to install snippets", []

    def _backup_all_settings(self) -> Path | None:
        """Backup all VS Code settings before installation."""
        backup_dir = self.config_dir / "backups"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        try:
            backup_dir.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError):
            return None

        for file_name in ["settings.json", "extensions.json", "keybindings.json"]:
            file_path = self.config_dir / file_name
            if file_path.exists():
                backup_path = backup_dir / f"{file_name}.{timestamp}.bak"
                try:
                    shutil.copy2(file_path, backup_path)
                except (OSError, IOError):
                    pass

        if self.snippets_dir.exists():
            snippets_backup_dir = backup_dir / f"snippets.{timestamp}"
            try:
                shutil.copytree(self.snippets_dir, snippets_backup_dir, dirs_exist_ok=True)
            except (OSError, IOError):
                pass

        return backup_dir

    def get_installed_preset(self) -> InstalledPresetInfo | None:
        """Get information about the currently installed preset."""
        info = self._load_installed_info()

        if not info or "preset_id" not in info:
            return None

        try:
            installed_at = datetime.fromisoformat(info.get("installed_at", ""))
            if installed_at.year == 1:
                installed_at = datetime.now()
        except (ValueError, TypeError):
            installed_at = datetime.now()

        return InstalledPresetInfo(
            preset_id=info.get("preset_id", ""),
            installed_at=installed_at,
            preset_name=info.get("preset_name"),
            version=info.get("version"),
            files=info.get("files", []),
        )

    def is_preset_installed(self, preset_id: str) -> bool:
        """Check if a specific preset is installed."""
        installed = self.get_installed_preset()
        return installed is not None and installed.preset_id == preset_id

    def uninstall(self, preset_id: str | None = None) -> bool:
        """Uninstall a preset or reset to defaults."""
        target_id = preset_id

        if target_id is None:
            installed = self.get_installed_preset()
            target_id = installed.preset_id if installed else None

        if target_id is None:
            return False

        backup_dir = self.config_dir / "backups"

        if backup_dir.exists():
            for file_name in ["settings.json", "extensions.json", "keybindings.json"]:
                backup_files = sorted(
                    backup_dir.glob(f"{file_name}.*.bak"),
                    key=lambda p: p.stat().st_mtime,
                    reverse=True,
                )

                if backup_files:
                    try:
                        shutil.copy2(backup_files[0], self.config_dir / file_name)
                    except (OSError, IOError):
                        continue

        self._save_installed_info({})
        return True

    def get_installed_files(self) -> dict[str, bool]:
        """Check which VS Code configuration files exist."""
        return {
            "settings": (self.config_dir / "settings.json").exists(),
            "extensions": (self.config_dir / "extensions.json").exists(),
            "keybindings": (self.config_dir / "keybindings.json").exists(),
            "snippets": self.snippets_dir.exists(),
        }

    def validate_installation(self, preset_id: str) -> tuple[bool, list[str]]:
        """Validate that a preset was installed correctly."""
        errors: list[str] = []

        preset = self.preset_manager.get_preset(preset_id)
        if not preset:
            errors.append("Preset not found")
            return False, errors

        settings = self._read_json_file("settings.json")
        if settings is None:
            errors.append("settings.json not found")

        extensions = self._read_json_file("extensions.json")
        if extensions is None:
            errors.append("extensions.json not found")

        return len(errors) == 0, errors

    def get_installation_statistics(self) -> dict[str, Any]:
        """Get statistics about the current installation."""
        installed = self.get_installed_preset()
        files = self.get_installed_files()

        file_count = sum(1 for exists in files.values() if exists)

        return {
            "is_installed": installed is not None,
            "preset_id": installed.preset_id if installed else None,
            "preset_name": installed.preset_name if installed else None,
            "files_copied": file_count,
            "total_files": len(files),
            "installed_at": installed.installed_at if installed else None,
        }
