"""Backup and restore functionality for ProjectVSCodeTemplates."""

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from projectvscodetemplates.constants import (
    get_vscode_config_dir,
    get_backup_dir,
    MAX_BACKUPS_TO_KEEP,
)


@dataclass
class BackupInfo:
    """Information about a backup."""

    id: str
    path: Path
    created_at: datetime
    size_bytes: int
    preset_id: str | None = None
    description: str = ""

    @property
    def created_at_str(self) -> str:
        """Get formatted creation date."""
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def size_kb(self) -> float:
        """Get size in KB."""
        return self.size_bytes / 1024

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "path": str(self.path),
            "created_at": self.created_at.isoformat(),
            "size_bytes": self.size_bytes,
            "preset_id": self.preset_id,
            "description": self.description,
        }


class BackupManager:
    """Manages backup and restore operations with robust error handling."""

    def __init__(self):
        """Initialize the backup manager."""
        self._config_dir: Path | None = None
        self._backup_dir: Path | None = None
        self._index_file: Path | None = None

    @property
    def config_dir(self) -> Path:
        """Get VS Code config directory lazily."""
        if self._config_dir is None:
            self._config_dir = get_vscode_config_dir()
        return self._config_dir

    @property
    def backup_dir(self) -> Path:
        """Get backup directory lazily."""
        if self._backup_dir is None:
            self._backup_dir = get_backup_dir()
        return self._backup_dir

    @property
    def index_file(self) -> Path:
        """Get backup index file path."""
        if self._index_file is None:
            self._index_file = self.backup_dir / "backup_index.json"
        return self._index_file

    def _ensure_backup_dir(self) -> bool:
        """Ensure backup directory exists."""
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            return True
        except (OSError, PermissionError):
            return False

    def _load_index(self) -> dict[str, Any]:
        """Load backup index from disk."""
        if self.index_file.exists():
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {"backups": []}
        return {"backups": []}

    def _save_index(self, index: dict[str, Any]) -> bool:
        """Save backup index to disk."""
        try:
            with open(self.index_file, "w", encoding="utf-8") as f:
                json.dump(index, f, indent=2, default=str)
            return True
        except IOError:
            return False

    def _calculate_directory_size(self, path: Path) -> int:
        """Calculate total size of a directory recursively."""
        total = 0
        try:
            if path.is_file():
                return path.stat().st_size
            for item in path.rglob("*"):
                if item.is_file():
                    try:
                        total += item.stat().st_size
                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
            pass
        return total

    def create_backup(
        self,
        preset_id: str | None = None,
        description: str = "",
        include_snippets: bool = True,
    ) -> BackupInfo | None:
        """
        Create a backup of current VS Code configuration.

        Args:
            preset_id: ID of the preset being backed up
            description: Optional description for the backup
            include_snippets: Whether to include snippets in backup

        Returns:
            BackupInfo if successful, None otherwise
        """
        if not self._ensure_backup_dir():
            return None

        timestamp = datetime.now()
        backup_id = timestamp.strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / backup_id

        try:
            backup_path.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError):
            return None

        files_copied = 0

        for file_name in ["settings.json", "extensions.json", "keybindings.json"]:
            src = self.config_dir / file_name
            if src.exists():
                try:
                    shutil.copy2(src, backup_path / file_name)
                    files_copied += 1
                except (OSError, IOError):
                    continue

        if include_snippets:
            snippets_src = self.config_dir / "snippets"
            if snippets_src.exists() and snippets_src.is_dir():
                snippets_dest = backup_path / "snippets"
                try:
                    shutil.copytree(snippets_src, snippets_dest, dirs_exist_ok=True)
                except (OSError, IOError):
                    pass

        if files_copied == 0:
            try:
                shutil.rmtree(backup_path)
            except (OSError, IOError):
                pass
            return None

        backup_size = self._calculate_directory_size(backup_path)

        installed_file = self.config_dir / ".projectvscodetemplates_installed.json"
        preset_name = preset_id

        if installed_file.exists():
            try:
                with open(installed_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    preset_name = data.get("preset_name") or preset_id
            except (json.JSONDecodeError, IOError):
                pass

        backup_info = BackupInfo(
            id=backup_id,
            path=backup_path,
            created_at=timestamp,
            size_bytes=backup_size,
            preset_id=preset_name,
            description=description,
        )

        index = self._load_index()
        index["backups"].append(backup_info.to_dict())
        self._save_index(index)

        return backup_info

    def list_backups(self) -> list[BackupInfo]:
        """
        List all available backups sorted by creation date (newest first).

        Returns:
            List of BackupInfo objects
        """
        index = self._load_index()
        backups: list[BackupInfo] = []
        valid_ids: set[str] = set()

        for backup_data in index.get("backups", []):
            backup_path = Path(backup_data.get("path", ""))

            if not backup_path.exists():
                continue

            try:
                created_at = datetime.fromisoformat(backup_data.get("created_at", ""))
                if created_at.year == 1:
                    created_at = datetime.now()
            except (ValueError, TypeError):
                created_at = datetime.now()

            backup_info = BackupInfo(
                id=backup_data.get("id", ""),
                path=backup_path,
                created_at=created_at,
                size_bytes=backup_data.get("size_bytes", 0),
                preset_id=backup_data.get("preset_id"),
                description=backup_data.get("description", ""),
            )
            backups.append(backup_info)
            valid_ids.add(backup_data.get("id", ""))

        backups.sort(key=lambda b: b.created_at, reverse=True)

        if len(valid_ids) < len(index.get("backups", [])):
            self._cleanup_invalid_backups(index, valid_ids)

        return backups

    def _cleanup_invalid_backups(self, index: dict[str, Any], valid_ids: set[str]) -> None:
        """Remove invalid entries from index."""
        index["backups"] = [b for b in index.get("backups", []) if b.get("id", "") in valid_ids]
        self._save_index(index)

    def restore_backup(self, backup_id: str) -> bool:
        """
        Restore a backup by ID.

        Args:
            backup_id: ID of the backup to restore

        Returns:
            True if successful, False otherwise
        """
        index = self._load_index()

        backup_data = None
        for b in index.get("backups", []):
            if b.get("id") == backup_id:
                backup_data = b
                break

        if not backup_data:
            return False

        backup_path = Path(backup_data.get("path", ""))

        if not backup_path.exists():
            return False

        files_restored = 0

        for file_name in ["settings.json", "extensions.json", "keybindings.json"]:
            src = backup_path / file_name
            if src.exists():
                try:
                    shutil.copy2(src, self.config_dir / file_name)
                    files_restored += 1
                except (OSError, IOError):
                    continue

        snippets_src = backup_path / "snippets"
        if snippets_src.exists() and snippets_src.is_dir():
            snippets_dest = self.config_dir / "snippets"
            try:
                if snippets_dest.exists():
                    shutil.rmtree(snippets_dest)
                shutil.copytree(snippets_src, snippets_dest)
            except (OSError, IOError):
                pass

        return files_restored > 0

    def delete_backup(self, backup_id: str) -> bool:
        """
        Delete a specific backup.

        Args:
            backup_id: ID of the backup to delete

        Returns:
            True if successful, False otherwise
        """
        index = self._load_index()

        backup_path = None
        new_backups = []

        for backup_data in index.get("backups", []):
            if backup_data.get("id") == backup_id:
                backup_path = Path(backup_data.get("path", ""))
            else:
                new_backups.append(backup_data)

        if backup_path is None:
            return False

        index["backups"] = new_backups
        self._save_index(index)

        if backup_path.exists():
            try:
                shutil.rmtree(backup_path)
            except (OSError, IOError):
                pass

        return True

    def delete_old_backups(self, keep_count: int = MAX_BACKUPS_TO_KEEP) -> int:
        """
        Delete old backups, keeping the most recent ones.

        Args:
            keep_count: Number of recent backups to keep

        Returns:
            Number of backups deleted
        """
        backups = self.list_backups()

        if len(backups) <= keep_count:
            return 0

        deleted_count = 0
        for backup in backups[keep_count:]:
            if self.delete_backup(backup.id):
                deleted_count += 1

        return deleted_count

    def cleanup_all(self) -> int:
        """
        Delete all backups.

        Returns:
            Number of backups deleted
        """
        backups = self.list_backups()
        deleted_count = 0

        for backup in backups:
            if self.delete_backup(backup.id):
                deleted_count += 1

        return deleted_count

    def get_backup_stats(self) -> dict[str, Any]:
        """
        Get backup statistics.

        Returns:
            Dictionary with backup statistics
        """
        backups = self.list_backups()

        if not backups:
            return {
                "total_backups": 0,
                "total_size_bytes": 0,
                "total_size_kb": 0.0,
                "oldest_backup": None,
                "newest_backup": None,
            }

        total_size = sum(b.size_bytes for b in backups)

        return {
            "total_backups": len(backups),
            "total_size_bytes": total_size,
            "total_size_kb": round(total_size / 1024, 2),
            "oldest_backup": backups[-1].to_dict() if backups else None,
            "newest_backup": backups[0].to_dict() if backups else None,
        }
