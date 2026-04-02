"""Preset management for ProjectVSCodeTemplates."""

import json
import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

from projectvscodetemplates.constants import (
    DIFFICULTY_COLORS,
    DIFFICULTY_LEVELS,
)


@dataclass(frozen=True)
class Preset:
    """Represents a VS Code preset configuration."""

    id: str
    name: str
    category: str
    track: str
    difficulty: str
    description: str
    target_user: str
    recommended_theme: str
    extension_count: int
    tags: tuple[str, ...]
    connects_to: tuple[str, ...]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Preset":
        """Create Preset from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            track=data["track"],
            difficulty=data["difficulty"],
            description=data["description"],
            target_user=data["target_user"],
            recommended_theme=data["recommended_theme"],
            extension_count=data["extension_count"],
            tags=tuple(data.get("tags", [])),
            connects_to=tuple(data.get("connects_to", [])),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert Preset to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "track": self.track,
            "difficulty": self.difficulty,
            "description": self.description,
            "target_user": self.target_user,
            "recommended_theme": self.recommended_theme,
            "extension_count": self.extension_count,
            "tags": list(self.tags),
            "connects_to": list(self.connects_to),
        }

    @property
    def difficulty_level(self) -> int:
        """Get numeric difficulty level."""
        return DIFFICULTY_LEVELS.get(self.difficulty, 0)

    @property
    def difficulty_color(self) -> str:
        """Get Rich color for difficulty."""
        return DIFFICULTY_COLORS.get(self.difficulty, "white")

    @property
    def difficulty_label(self) -> str:
        """Get formatted difficulty label with color."""
        color = self.difficulty_color
        return f"[{color}]{self.difficulty.title()}[/]"

    @property
    def short_description(self) -> str:
        """Get truncated description."""
        if len(self.description) <= 60:
            return self.description
        return self.description[:57] + "..."

    def matches_tag(self, tag: str) -> bool:
        """Check if preset has a specific tag."""
        return tag.lower() in [t.lower() for t in self.tags]

    def matches_any_tag(self, tags: list[str]) -> bool:
        """Check if preset matches any of the given tags."""
        preset_tags = {t.lower() for t in self.tags}
        return any(tag.lower() in preset_tags for tag in tags)

    def get_upgrade_preset(self) -> "Preset | None":
        """Get the next preset in the upgrade path."""
        if self.connects_to:
            return PresetManager().get_preset(self.connects_to[0])
        return None


@dataclass
class PresetFile:
    """Represents a preset's configuration file."""

    name: str
    content: dict[str, Any]

    @classmethod
    def from_file(cls, path: Path) -> "PresetFile":
        """Load preset file from path."""
        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)
        return cls(name=path.stem, content=content)

    def to_json(self, indent: int = 4) -> str:
        """Convert content to formatted JSON string."""
        return json.dumps(self.content, indent=indent, ensure_ascii=False)


class PresetManager:
    """Manages preset loading, caching, and querying."""

    _instance: "PresetManager | None" = None
    _presets: list[Preset] | None = None
    _preset_dict: dict[str, Preset] | None = None
    _presets_dir: Path | None = None

    def __new__(cls) -> "PresetManager":
        """Singleton pattern for single instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the preset manager."""
        if self._presets is None:
            self._load_presets()

    def _get_presets_dir(self) -> Path:
        """Find the presets directory."""
        if self._presets_dir is not None:
            return self._presets_dir

        pkg_names = [
            "projectvscodetemplates",
            "src.projectvscodetemplates",
        ]

        for pkg_name in pkg_names:
            try:
                import importlib

                spec = importlib.util.find_spec(pkg_name)
                if spec and spec.submodule_search_locations:
                    presets_path = Path(spec.submodule_search_locations[0]) / "presets"
                    if presets_path.exists():
                        self._presets_dir = presets_path
                        return presets_path
            except (ImportError, AttributeError):
                continue

        this_file = Path(__file__).parent
        presets_path = this_file / "presets"
        if presets_path.exists():
            self._presets_dir = presets_path
            return presets_path

        project_root = this_file.parent.parent
        presets_path = project_root / "presets"
        self._presets_dir = presets_path
        return presets_path

    def _load_presets(self) -> None:
        """Load all presets from manifest file."""
        presets_dir = self._get_presets_dir()
        manifest_path = presets_dir / "manifest.json"

        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")

        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        presets_data = data.get("presets", [])
        self._presets = [Preset.from_dict(p) for p in presets_data]
        self._preset_dict = {p.id: p for p in self._presets}

    def reload(self) -> None:
        """Reload presets from disk."""
        self._presets = None
        self._preset_dict = None
        self._load_presets()

    @property
    def presets(self) -> list[Preset]:
        """Get all presets."""
        if self._presets is None:
            self._load_presets()
        return list(self._presets or [])

    @property
    def preset_count(self) -> int:
        """Get total number of presets."""
        return len(self.presets)

    def get_preset(self, preset_id: str) -> Preset | None:
        """Get a preset by ID."""
        if self._preset_dict is None:
            self._load_presets()
        return self._preset_dict.get(preset_id) if self._preset_dict else None

    def get_preset_by_index(self, index: int) -> Preset | None:
        """Get a preset by its index (0-based)."""
        presets = self.presets
        if 0 <= index < len(presets):
            return presets[index]
        return None

    def get_preset_files(self, preset_id: str) -> dict[str, PresetFile]:
        """Load all configuration files for a preset."""
        preset_dir = self._get_presets_dir() / preset_id
        files: dict[str, PresetFile] = {}

        if preset_dir.exists():
            for file_path in preset_dir.glob("*.json"):
                try:
                    files[file_path.stem] = PresetFile.from_file(file_path)
                except (json.JSONDecodeError, IOError):
                    continue

        return files

    def get_extensions(self, preset_id: str) -> list[str]:
        """Get extension IDs for a preset."""
        files = self.get_preset_files(preset_id)
        extensions_file = files.get("extensions")

        if extensions_file:
            return extensions_file.content.get("recommendations", [])
        return []

    def get_settings(self, preset_id: str) -> dict[str, Any] | None:
        """Get settings for a preset."""
        files = self.get_preset_files(preset_id)
        settings_file = files.get("settings")
        return settings_file.content if settings_file else None

    def get_keybindings(self, preset_id: str) -> list[dict[str, Any]] | None:
        """Get keybindings for a preset."""
        files = self.get_preset_files(preset_id)
        keybindings_file = files.get("keybindings")

        if keybindings_file:
            content = keybindings_file.content
            if isinstance(content, list):
                return content
            return [content]
        return None

    def get_snippets(self, preset_id: str) -> dict[str, PresetFile]:
        """Get code snippets for a preset."""
        preset_dir = self._get_presets_dir() / preset_id
        snippets: dict[str, PresetFile] = {}

        if preset_dir.exists():
            for file_path in preset_dir.glob("*.snippets"):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = json.load(f)
                    snippets[file_path.stem] = PresetFile(name=file_path.stem, content=content)
                except (json.JSONDecodeError, IOError):
                    continue

        return snippets

    def get_categories(self) -> list[str]:
        """Get all unique categories."""
        return sorted(set(p.category for p in self.presets))

    def get_tracks(self) -> list[str]:
        """Get all unique tracks."""
        return sorted(set(p.track for p in self.presets))

    def get_difficulties(self) -> list[str]:
        """Get all unique difficulty levels sorted by level."""
        difficulties = [
            (d, DIFFICULTY_LEVELS.get(d, 0)) for d in set(p.difficulty for p in self.presets)
        ]
        difficulties.sort(key=lambda x: x[1])
        return [d[0] for d in difficulties]

    def get_presets_by_category(self, category: str) -> list[Preset]:
        """Get presets filtered by category."""
        return [p for p in self.presets if p.category == category]

    def get_presets_by_difficulty(self, difficulty: str) -> list[Preset]:
        """Get presets filtered by difficulty."""
        return [p for p in self.presets if p.difficulty == difficulty]

    def get_presets_by_track(self, track: str) -> list[Preset]:
        """Get presets filtered by track."""
        return [p for p in self.presets if p.track == track]

    def search_presets(self, query: str) -> list[Preset]:
        """
        Search presets by name, description, tags, or ID.

        Uses weighted scoring:
        - Exact ID match: 10 points
        - Name contains: 8 points
        - Tag match: 5 points
        - Description contains: 3 points
        - Target user contains: 2 points
        """
        query_lower = query.lower().strip()
        if not query_lower:
            return self.presets

        scored: list[tuple[Preset, int]] = []

        for preset in self.presets:
            score = 0

            if query_lower == preset.id.lower():
                score += 10
            elif query_lower in preset.id.lower():
                score += 2

            if query_lower in preset.name.lower():
                score += 8

            if any(query_lower in tag.lower() for tag in preset.tags):
                score += 5

            if query_lower in preset.description.lower():
                score += 3

            if query_lower in preset.target_user.lower():
                score += 2

            if score > 0:
                scored.append((preset, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [p for p, _ in scored]

    def get_recommendations(
        self,
        tags: list[str],
        exclude_id: str | None = None,
        limit: int = 5,
    ) -> list[Preset]:
        """
        Get preset recommendations based on tags.

        Args:
            tags: List of tags to match
            exclude_id: Preset ID to exclude
            limit: Maximum number of recommendations

        Returns:
            List of recommended presets sorted by relevance
        """
        scored: dict[str, tuple[Preset, int]] = {}

        for preset in self.presets:
            if preset.id == exclude_id:
                continue

            score = 0
            preset_tags = {t.lower() for t in preset.tags}

            for tag in tags:
                tag_lower = tag.lower()

                if tag_lower in preset_tags:
                    score += 3

                for ptag in preset_tags:
                    if tag_lower in ptag or ptag in tag_lower:
                        score += 1

            if score > 0:
                scored[preset.id] = (preset, score)

        sorted_presets = sorted(scored.values(), key=lambda x: x[1], reverse=True)
        return [p for p, _ in sorted_presets[:limit]]

    def get_upgrade_path(self, preset_id: str) -> list[Preset]:
        """Get the upgrade path for a preset."""
        path: list[Preset] = []
        visited: set[str] = set()
        current_id: str | None = preset_id

        while current_id and current_id not in visited:
            visited.add(current_id)
            preset = self.get_preset(current_id)

            if not preset or not preset.connects_to:
                break

            next_id = preset.connects_to[0]
            next_preset = self.get_preset(next_id)

            if next_preset:
                path.append(next_preset)
                current_id = next_id
            else:
                break

        return path

    def get_statistics(self) -> dict[str, Any]:
        """Get preset statistics."""
        total_extensions = sum(p.extension_count for p in self.presets)
        category_counts: dict[str, int] = {}
        difficulty_counts: dict[str, int] = {}
        track_counts: dict[str, int] = {}

        for preset in self.presets:
            category_counts[preset.category] = category_counts.get(preset.category, 0) + 1
            difficulty_counts[preset.difficulty] = difficulty_counts.get(preset.difficulty, 0) + 1
            track_counts[preset.track] = track_counts.get(preset.track, 0) + 1

        return {
            "total_presets": self.preset_count,
            "total_extensions": total_extensions,
            "categories": category_counts,
            "difficulties": difficulty_counts,
            "tracks": track_counts,
        }


@lru_cache(maxsize=1)
def get_preset_manager() -> PresetManager:
    """Get singleton PresetManager instance."""
    return PresetManager()
