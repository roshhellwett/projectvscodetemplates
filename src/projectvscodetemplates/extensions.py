"""VS Code extension management for ProjectVSCodeTemplates."""

import json
import logging
import re
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

__all__ = [
    "ExtensionInfo",
    "ExtensionInstallResult",
    "ExtensionSearchResult",
    "ExtensionManager",
]

from projectvscodetemplates.presets import PresetManager, get_preset_manager
from projectvscodetemplates.constants import (
    IS_WINDOWS,
    IS_LINUX,
    IS_MACOS,
    EXTENSION_INSTALL_TIMEOUT,
    MAX_SEARCH_RESULTS,
)
from projectvscodetemplates.utils import (
    print_info,
    print_success,
    print_error,
    print_warning,
    run_command,
    ensure_directory,
)


@dataclass
class ExtensionInfo:
    """Information about a VS Code extension."""

    id: str
    name: str = ""
    version: str = ""
    publisher: str = ""
    description: str = ""
    installed: bool = False
    install_version: str | None = None
    pre_release: bool = False
    download_count: int = 0
    last_updated: str = ""

    def __str__(self) -> str:
        parts = [self.name or self.id]
        if self.version:
            parts.append(f"v{self.version}")
        if self.publisher:
            parts.append(f"by {self.publisher}")
        return " ".join(parts)

    def __repr__(self) -> str:
        return f"ExtensionInfo(id={self.id!r}, installed={self.installed})"

    @property
    def short_id(self) -> str:
        """Get short extension ID (publisher.name)."""
        return self.id

    @property
    def display_name(self) -> str:
        """Get display name."""
        return self.name or self.id.split(".")[-1] if self.id else "Unknown"


@dataclass
class ExtensionInstallResult:
    """Result of extension installation operation."""

    extension_id: str
    success: bool
    installed: bool = False
    message: str = ""
    version: str | None = None
    duration_ms: int = 0

    def __str__(self) -> str:
        status = "Installed" if self.success else "Failed"
        return f"{status}: {self.extension_id} - {self.message}"


@dataclass
class ExtensionSearchResult:
    """Result from extension search."""

    extension: ExtensionInfo
    score: float = 0.0
    match_reason: str = ""


class ExtensionManager:
    """Manages VS Code extensions installation and queries."""

    def __init__(self, preset_manager: PresetManager | None = None):
        """Initialize the extension manager."""
        self._preset_manager = preset_manager
        self._code_available: bool | None = None
        self._installed_cache: list[str] | None = None
        self._cache_timestamp: float = 0
        self._cache_ttl: float = 30.0

    @property
    def preset_manager(self) -> PresetManager:
        """Get preset manager with lazy loading."""
        if self._preset_manager is None:
            self._preset_manager = get_preset_manager()
        return self._preset_manager

    def _is_code_available(self, force_check: bool = False) -> bool:
        """Check if VS Code CLI is available with caching."""
        if force_check or self._code_available is None:
            self._code_available = self._check_code_in_path()
        return self._code_available

    def _check_code_in_path(self) -> bool:
        """Actually check if code CLI is in PATH."""
        try:
            if IS_WINDOWS:
                returncode, _, _ = run_command(["where", "code"], timeout=5, capture=True)
            else:
                returncode, _, _ = run_command(["which", "code"], timeout=5, capture=True)
            return returncode == 0
        except OSError:
            return False

    def _run_code_command(
        self, args: list[str], timeout: int | None = None
    ) -> tuple[int, str, str]:
        """Run a VS Code CLI command with proper timeout."""
        if timeout is None:
            timeout = EXTENSION_INSTALL_TIMEOUT
        return run_command(["code"] + args, timeout=timeout)

    def _invalidate_cache(self) -> None:
        """Invalidate the installed extensions cache."""
        self._installed_cache = None
        self._cache_timestamp = 0

    def _get_cached_installed(self, force_refresh: bool = False) -> list[str] | None:
        """Get cached installed extensions list."""
        if force_refresh:
            self._invalidate_cache()

        if self._installed_cache is None or (time.time() - self._cache_timestamp) > self._cache_ttl:
            self._installed_cache = self._fetch_installed_extensions()
            self._cache_timestamp = time.time()

        return self._installed_cache

    def _fetch_installed_extensions(self) -> list[str]:
        """Actually fetch installed extensions from VS Code."""
        if not self._is_code_available():
            return []

        returncode, stdout, _ = self._run_code_command(["--list-extensions"])

        if returncode != 0:
            return []

        extensions: list[str] = []
        for line in stdout.strip().split("\n"):
            line = line.strip()
            if line and "." in line:
                extensions.append(line)

        return sorted(set(extensions))

    def get_installed_extensions(self, force_refresh: bool = False) -> list[str]:
        """Get list of installed extension IDs with caching."""
        cached = self._get_cached_installed(force_refresh)
        return cached if cached is not None else []

    def get_installed_count(self) -> int:
        """Get count of installed extensions."""
        return len(self.get_installed_extensions())

    def is_extension_installed(self, extension_id: str, force_refresh: bool = False) -> bool:
        """Check if a specific extension is installed."""
        installed = self._get_cached_installed(force_refresh)
        return extension_id in (installed or [])

    def search_extension(
        self, extension_id: str, force_refresh: bool = False
    ) -> ExtensionInfo | None:
        """Search for extension information from marketplace."""
        if not self._is_code_available():
            return None

        returncode, stdout, stderr = self._run_code_command(
            ["--install-extension", extension_id, "--dry-run"]
        )

        info = ExtensionInfo(id=extension_id, name=self._parse_extension_name(extension_id))

        if "not found" in stdout.lower() or "not found" in stderr.lower() or returncode != 0:
            return info

        version_match = re.search(r"v?(\d+\.\d+\.\d+)", stdout + stderr)
        if version_match:
            info.version = version_match.group(1)

        if force_refresh:
            self._parse_extension_details(extension_id, info)

        return info

    def _parse_extension_name(self, extension_id: str) -> str:
        """Parse extension name from extension ID."""
        parts = extension_id.split(".")
        return parts[-1] if len(parts) > 1 else extension_id

    def _parse_extension_details(self, extension_id: str, info: ExtensionInfo) -> None:
        """Parse additional extension details from ID."""
        if "." in extension_id:
            parts = extension_id.split(".")
            if len(parts) >= 2:
                info.publisher = parts[0]
                info.name = ".".join(parts[1:])

    def validate_extension_id(self, extension_id: str) -> bool:
        """Validate extension ID format (publisher.name)."""
        if not extension_id or not isinstance(extension_id, str):
            return False
        parts = extension_id.strip().split(".")
        if len(parts) < 2:
            return False
        import re

        valid_pattern = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]*$")
        return all(bool(valid_pattern.match(p)) for p in parts)

    def install_extension(
        self,
        extension_id: str,
        force: bool = False,
        enable_proposals: bool = False,
    ) -> ExtensionInstallResult:
        """Install a VS Code extension."""
        start_time = time.time()

        if not self._is_code_available():
            return ExtensionInstallResult(
                extension_id=extension_id,
                success=False,
                message="VS Code CLI (code) not found in PATH. Please install VS Code.",
            )

        if not force and self.is_extension_installed(extension_id):
            return ExtensionInstallResult(
                extension_id=extension_id,
                success=True,
                installed=True,
                message="Extension already installed",
                duration_ms=int((time.time() - start_time) * 1000),
            )

        print_info(f"Installing extension: {extension_id}")

        args = ["--install-extension", extension_id]
        if enable_proposals:
            args.append("--enable-proposed-api")

        returncode, stdout, stderr = self._run_code_command(args)

        duration_ms = int((time.time() - start_time) * 1000)

        if returncode == 0:
            self._invalidate_cache()
            return ExtensionInstallResult(
                extension_id=extension_id,
                success=True,
                installed=True,
                message="Extension installed successfully",
                duration_ms=duration_ms,
            )
        else:
            error_msg = self._parse_error_message(stderr or stdout)
            return ExtensionInstallResult(
                extension_id=extension_id,
                success=False,
                message=f"Failed to install: {error_msg}",
                duration_ms=duration_ms,
            )

    def _parse_error_message(self, error_output: str) -> str:
        """Parse user-friendly error message from output."""
        error_lower = error_output.lower()

        if "not found" in error_lower:
            return "Extension not found in marketplace"
        if "already installed" in error_lower:
            return "Extension already installed"
        if "signature" in error_lower or "verification" in error_lower:
            return "Signature verification failed"
        if "network" in error_lower or "connection" in error_lower:
            return "Network error - check connection"
        if "timeout" in error_lower:
            return "Installation timed out"

        lines = error_output.strip().split("\n")
        return lines[-1] if lines else "Unknown error"

    def uninstall_extension(self, extension_id: str) -> ExtensionInstallResult:
        """Uninstall a VS Code extension."""
        start_time = time.time()

        if not self._is_code_available():
            return ExtensionInstallResult(
                extension_id=extension_id,
                success=False,
                message="VS Code CLI (code) not found in PATH",
            )

        if not self.is_extension_installed(extension_id):
            return ExtensionInstallResult(
                extension_id=extension_id,
                success=True,
                message="Extension not installed",
                duration_ms=int((time.time() - start_time) * 1000),
            )

        returncode, stdout, stderr = self._run_code_command(["--uninstall-extension", extension_id])

        duration_ms = int((time.time() - start_time) * 1000)

        if returncode == 0:
            self._invalidate_cache()
            return ExtensionInstallResult(
                extension_id=extension_id,
                success=True,
                installed=False,
                message="Extension uninstalled successfully",
                duration_ms=duration_ms,
            )
        else:
            return ExtensionInstallResult(
                extension_id=extension_id,
                success=False,
                message=f"Failed to uninstall: {stderr or stdout}",
                duration_ms=duration_ms,
            )

    def install_preset_extensions(
        self,
        preset_id: str,
        show_progress: bool = True,
        stop_on_error: bool = False,
    ) -> dict[str, ExtensionInstallResult]:
        """Install all extensions for a preset."""
        extension_ids = self.preset_manager.get_extensions(preset_id)

        if not extension_ids:
            return {}

        results: dict[str, ExtensionInstallResult] = {}
        successful = 0
        failed = 0

        for ext_id in extension_ids:
            result = self.install_extension(ext_id)
            results[ext_id] = result

            if result.success:
                successful += 1
            else:
                failed += 1

            if show_progress:
                status = "[green]OK[/]" if result.success else "[red]FAIL[/]"
                print(f"  {status} {ext_id}: {result.message}")

            if stop_on_error and not result.success:
                print_warning(f"Stopping due to error with {ext_id}")
                break

        if show_progress:
            print()
            print_info(f"Installed {successful}/{len(extension_ids)} extensions")
            if failed > 0:
                print_warning(f"{failed} extension(s) failed to install")

        return results

    def install_from_file(self, file_path: Path) -> dict[str, ExtensionInstallResult]:
        """Install extensions from extensions.json file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError, OSError) as e:
            return {
                "_error": ExtensionInstallResult(
                    extension_id="",
                    success=False,
                    message=f"Failed to read file: {e}",
                )
            }

        extension_ids = data.get("recommendations", [])

        if not isinstance(extension_ids, list):
            extension_ids = data.get("extensions", [])

        results: dict[str, ExtensionInstallResult] = {}
        for ext_id in extension_ids:
            if isinstance(ext_id, str):
                results[ext_id] = self.install_extension(ext_id)

        return results

    def get_extension_status(
        self,
        extension_ids: list[str],
        force_refresh: bool = False,
    ) -> dict[str, bool]:
        """Get installation status for multiple extensions."""
        installed = set(self.get_installed_extensions(force_refresh))
        return {ext_id: ext_id in installed for ext_id in extension_ids}

    def get_missing_extensions(
        self,
        extension_ids: list[str],
    ) -> list[str]:
        """Get list of extensions that are not installed."""
        installed = set(self.get_installed_extensions())
        return [ext_id for ext_id in extension_ids if ext_id not in installed]

    def get_installed_preset_extensions(
        self,
        preset_id: str,
    ) -> dict[str, bool]:
        """Get installation status for all preset extensions."""
        extension_ids = self.preset_manager.get_extensions(preset_id)
        return self.get_extension_status(extension_ids, force_refresh=True)

    def recommend_extensions(self, tags: list[str]) -> list[str]:
        """Recommend popular extensions based on tags using preset data."""
        recommended: set[str] = set()

        for tag in tags:
            tag_lower = tag.lower().strip()

            for preset in self.preset_manager.presets:
                preset_tags = [t.lower() for t in preset.tags]
                if tag_lower in preset_tags or any(tag_lower in pt for pt in preset_tags):
                    ext_ids = self.preset_manager.get_extensions(preset.id)
                    for ext_id in ext_ids:
                        if ext_id:
                            recommended.add(ext_id)

        return list(recommended)[:MAX_SEARCH_RESULTS]

    def search_by_keyword(self, keyword: str) -> list[ExtensionSearchResult]:
        """Search extensions by keyword across presets."""
        keyword_lower = keyword.lower()
        results: list[ExtensionSearchResult] = []
        seen_ids: set[str] = set()

        for preset in self.preset_manager.presets:
            preset_name_lower = preset.name.lower()
            preset_desc_lower = preset.description.lower()
            preset_tags = " ".join(preset.tags).lower()

            score = 0.0
            match_reason = ""

            if keyword_lower in preset_name_lower:
                score += 10.0
                match_reason = "Name match"
            elif keyword_lower in preset_desc_lower:
                score += 5.0
                match_reason = "Description match"
            if keyword_lower in preset_tags:
                score += 7.0
                if match_reason:
                    match_reason += " + Tag match"
                else:
                    match_reason = "Tag match"

            if score > 0:
                ext_ids = self.preset_manager.get_extensions(preset.id)
                for ext_id in ext_ids:
                    if ext_id and ext_id not in seen_ids:
                        seen_ids.add(ext_id)
                        results.append(
                            ExtensionSearchResult(
                                extension=ExtensionInfo(
                                    id=ext_id,
                                    name=self._parse_extension_name(ext_id),
                                    publisher=ext_id.split(".")[0] if "." in ext_id else "",
                                ),
                                score=score,
                                match_reason=match_reason,
                            )
                        )

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:MAX_SEARCH_RESULTS]

    def export_installed(self, output_path: Path) -> bool:
        """Export installed extensions to a file."""
        installed = self.get_installed_extensions()

        try:
            data = {
                "recommendations": sorted(installed),
                "exported_at": datetime.now().isoformat(),
                "count": len(installed),
            }

            ensure_directory(output_path.parent)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return True
        except (IOError, OSError) as e:
            print_error(f"Failed to export: {e}")
            return False

    def get_statistics(self) -> dict[str, Any]:
        """Get extension statistics."""
        installed = self.get_installed_extensions()
        installed_set = set(installed)

        publishers: dict[str, int] = {}
        for ext_id in installed:
            publisher = ext_id.split(".")[0] if "." in ext_id else "unknown"
            publishers[publisher] = publishers.get(publisher, 0) + 1

        return {
            "total_installed": len(installed),
            "publishers": publishers,
            "top_publisher": max(publishers.items(), key=lambda x: x[1])[0] if publishers else None,
            "vscode_available": self._is_code_available(),
            "cache_valid": self._installed_cache is not None,
        }
