"""Comprehensive stress tests for ProjectVSCodeTemplates.

This test suite is designed to break the project and verify robustness.
Tests cover: boundary conditions, type attacks, value attacks, filesystem,
presets, quiz, exceptions, imports, logging, and performance.
"""

import importlib
import json
import sys
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from projectvscodetemplates import __version__
from projectvscodetemplates import constants
from projectvscodetemplates.exceptions import (
    BackupError,
    ConfigurationError,
    ExtensionError,
    InstallationError,
    ProjectVSCodeTemplatesError,
    PresetNotFoundError,
    ValidationError,
)
from projectvscodetemplates.presets import Preset, PresetFile, PresetManager
from projectvscodetemplates.installer import InstallResult, VSCodeInstaller
from projectvscodetemplates.backup import BackupInfo, BackupManager
from projectvscodetemplates.quiz import QuizEngine, QuickQuiz


# ==============================================================================
# PHASE 1: UNIT STRESS TESTS - PresetManager
# ==============================================================================


def test_presets_get_preset_valid_id():
    """Test getting a preset with valid ID returns correct preset."""
    pm = PresetManager()
    preset = pm.get_preset("python-beginner")
    assert preset is not None
    assert preset.id == "python-beginner"
    assert preset.name == "Python Beginner"


def test_presets_get_preset_invalid_id():
    """Test getting a preset with invalid ID returns None."""
    pm = PresetManager()
    preset = pm.get_preset("nonexistent-preset-id-xyz")
    assert preset is None


def test_presets_get_preset_empty_string():
    """Test getting a preset with empty string returns None."""
    pm = PresetManager()
    preset = pm.get_preset("")
    assert preset is None


def test_presets_get_preset_by_index_valid():
    """Test getting preset by valid index."""
    pm = PresetManager()
    preset = pm.get_preset_by_index(0)
    assert preset is not None
    assert isinstance(preset, Preset)


def test_presets_get_preset_by_index_negative():
    """Test getting preset by negative index returns None."""
    pm = PresetManager()
    preset = pm.get_preset_by_index(-1)
    assert preset is None


def test_presets_get_preset_by_index_out_of_bounds():
    """Test getting preset by out-of-bounds index returns None."""
    pm = PresetManager()
    preset = pm.get_preset_by_index(9999)
    assert preset is None


def test_presets_get_preset_files_valid():
    """Test getting preset files returns non-empty dict."""
    pm = PresetManager()
    files = pm.get_preset_files("python-beginner")
    assert isinstance(files, dict)
    assert len(files) > 0


def test_presets_get_preset_files_invalid():
    """Test getting files for invalid preset returns empty dict."""
    pm = PresetManager()
    files = pm.get_preset_files("nonexistent")
    assert files == {}


def test_presets_get_extensions_valid():
    """Test getting extensions for valid preset."""
    pm = PresetManager()
    exts = pm.get_extensions("python-beginner")
    assert isinstance(exts, list)


def test_presets_get_extensions_empty_for_invalid():
    """Test getting extensions for invalid preset returns empty list."""
    pm = PresetManager()
    exts = pm.get_extensions("nonexistent-preset")
    assert exts == []


def test_presets_get_settings_valid():
    """Test getting settings for valid preset."""
    pm = PresetManager()
    settings = pm.get_settings("python-beginner")
    assert settings is not None
    assert isinstance(settings, dict)


def test_presets_get_settings_none_for_invalid():
    """Test getting settings for invalid preset returns None."""
    pm = PresetManager()
    settings = pm.get_settings("nonexistent")
    assert settings is None


def test_presets_get_keybindings_valid():
    """Test getting keybindings for valid preset."""
    pm = PresetManager()
    keybindings = pm.get_keybindings("python-beginner")
    assert keybindings is not None


def test_presets_get_categories():
    """Test getting categories returns expected values."""
    pm = PresetManager()
    categories = pm.get_categories()
    assert "student" in categories
    assert "professional" in categories
    assert "lifestyle" in categories


def test_presets_get_difficulties():
    """Test getting difficulties returns sorted list."""
    pm = PresetManager()
    difficulties = pm.get_difficulties()
    assert len(difficulties) > 0
    assert difficulties[0] == "beginner"


def test_presets_get_tracks():
    """Test getting tracks returns non-empty list."""
    pm = PresetManager()
    tracks = pm.get_tracks()
    assert len(tracks) > 0


def test_presets_get_presets_by_category_valid():
    """Test filtering presets by valid category."""
    pm = PresetManager()
    presets = pm.get_presets_by_category("student")
    assert len(presets) > 0
    assert all(p.category == "student" for p in presets)


def test_presets_get_presets_by_category_invalid():
    """Test filtering presets by invalid category returns empty list."""
    pm = PresetManager()
    presets = pm.get_presets_by_category("nonexistent-category")
    assert presets == []


def test_presets_get_presets_by_difficulty_valid():
    """Test filtering presets by valid difficulty."""
    pm = PresetManager()
    presets = pm.get_presets_by_difficulty("beginner")
    assert len(presets) > 0
    assert all(p.difficulty == "beginner" for p in presets)


def test_presets_search_presets_exact_match():
    """Test search with exact preset ID match."""
    pm = PresetManager()
    results = pm.search_presets("python-beginner")
    assert len(results) > 0
    assert results[0].id == "python-beginner"


def test_presets_search_presets_partial_match():
    """Test search with partial name match."""
    pm = PresetManager()
    results = pm.search_presets("python")
    assert len(results) > 0


def test_presets_search_presets_empty_query():
    """Test search with empty query returns all presets."""
    pm = PresetManager()
    results = pm.search_presets("")
    assert len(results) == pm.preset_count


def test_presets_search_presets_special_chars():
    """Test search with special characters doesn't crash."""
    pm = PresetManager()
    results = pm.search_presets("../../../etc/passwd")
    assert isinstance(results, list)


def test_presets_search_presets_emoji():
    """Test search with emoji doesn't crash."""
    pm = PresetManager()
    results = pm.search_presets("🔥💀🚀")
    assert isinstance(results, list)


def test_presets_get_recommendations_valid_tags():
    """Test getting recommendations with valid tags."""
    pm = PresetManager()
    recs = pm.get_recommendations(["python", "student"])
    assert len(recs) > 0


def test_presets_get_recommendations_empty_tags():
    """Test getting recommendations with empty tags."""
    pm = PresetManager()
    recs = pm.get_recommendations([])
    assert recs == []


def test_presets_get_recommendations_with_exclude():
    """Test getting recommendations with exclude_id."""
    pm = PresetManager()
    recs = pm.get_recommendations(["python"], exclude_id="python-beginner")
    assert all(p.id != "python-beginner" for p in recs)


def test_presets_get_recommendations_limit():
    """Test getting recommendations respects limit."""
    pm = PresetManager()
    recs = pm.get_recommendations(["python"], limit=3)
    assert len(recs) <= 3


def test_presets_get_upgrade_path_valid():
    """Test getting upgrade path for preset with connections."""
    pm = PresetManager()
    path = pm.get_upgrade_path("python-beginner")
    assert isinstance(path, list)


def test_presets_get_upgrade_path_no_connections():
    """Test getting upgrade path for preset without connections."""
    pm = PresetManager()
    # web-dev-frontend actually connects to web-dev-fullstack per manifest
    # Let's test python-professional which has empty connects_to
    path = pm.get_upgrade_path("python-professional")
    assert path == [], f"Expected empty path for python-professional, got {path}"


def test_presets_get_statistics():
    """Test getting statistics returns correct structure."""
    pm = PresetManager()
    stats = pm.get_statistics()
    assert stats["total_presets"] == 15
    assert "total_extensions" in stats
    assert "categories" in stats


def test_presets_preset_count():
    """Test preset_count property."""
    pm = PresetManager()
    assert pm.preset_count == 15


# ==============================================================================
# PHASE 1: UNIT STRESS TESTS - Preset dataclass
# ==============================================================================


def test_preset_from_dict_valid():
    """Test creating Preset from valid dict."""
    data = {
        "id": "test-preset",
        "name": "Test Preset",
        "category": "student",
        "track": "learning",
        "difficulty": "beginner",
        "description": "A test preset",
        "target_user": "Testers",
        "recommended_theme": "Test Theme",
        "extension_count": 5,
        "tags": ["test", "mock"],
        "connects_to": [],
    }
    preset = Preset.from_dict(data)
    assert preset.id == "test-preset"
    assert preset.name == "Test Preset"
    assert preset.extension_count == 5


def test_preset_from_dict_missing_keys():
    """Test Preset.from_dict with missing keys raises KeyError."""
    data = {"id": "test"}
    with pytest.raises(KeyError):
        Preset.from_dict(data)


def test_preset_from_dict_empty():
    """Test Preset.from_dict with empty dict raises KeyError."""
    with pytest.raises(KeyError):
        Preset.from_dict({})


def test_preset_matches_tag_exact():
    """Test matching exact tag."""
    pm = PresetManager()
    preset = pm.get_preset("python-beginner")
    assert preset.matches_tag("python")
    assert preset.matches_tag("Python")


def test_preset_matches_tag_no_match():
    """Test tag not matching."""
    pm = PresetManager()
    preset = pm.get_preset("python-beginner")
    assert not preset.matches_tag("rust")


def test_preset_matches_any_tag_some_match():
    """Test matching any of multiple tags."""
    pm = PresetManager()
    preset = pm.get_preset("python-beginner")
    assert preset.matches_any_tag(["rust", "python"])


def test_preset_matches_any_tag_no_match():
    """Test none of tags match."""
    pm = PresetManager()
    preset = pm.get_preset("python-beginner")
    assert not preset.matches_any_tag(["rust", "go"])


def test_preset_to_dict():
    """Test converting preset to dict."""
    pm = PresetManager()
    preset = pm.get_preset("python-beginner")
    d = preset.to_dict()
    assert isinstance(d, dict)
    assert d["id"] == "python-beginner"


def test_preset_difficulty_level():
    """Test difficulty_level property."""
    pm = PresetManager()
    preset = pm.get_preset("python-beginner")
    assert preset.difficulty_level == 1


def test_preset_difficulty_color():
    """Test difficulty_color property."""
    pm = PresetManager()
    preset = pm.get_preset("python-beginner")
    assert preset.difficulty_color == "green"


# ==============================================================================
# PHASE 2: FILESYSTEM STRESS TESTS
# ==============================================================================


def test_preset_file_from_file_nonexistent(tmp_path):
    """Test loading preset file from nonexistent path raises exception."""
    with pytest.raises(FileNotFoundError):
        PresetFile.from_file(tmp_path / "nonexistent.json")


def test_preset_file_from_file_empty_file(tmp_path):
    """Test loading empty JSON file raises JSONDecodeError."""
    empty_file = tmp_path / "empty.json"
    empty_file.write_text("")
    with pytest.raises(json.JSONDecodeError):
        PresetFile.from_file(empty_file)


def test_preset_file_from_file_invalid_json(tmp_path):
    """Test loading invalid JSON file raises JSONDecodeError."""
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("{not valid json")
    with pytest.raises(json.JSONDecodeError):
        PresetFile.from_file(invalid_file)


def test_preset_file_from_file_valid_json(tmp_path):
    """Test loading valid JSON file succeeds."""
    valid_file = tmp_path / "valid.json"
    valid_file.write_text('{"key": "value"}')
    pf = PresetFile.from_file(valid_file)
    assert pf.content == {"key": "value"}


def test_preset_file_to_json():
    """Test converting preset file to JSON string."""
    pf = PresetFile(name="test", content={"key": "value"})
    json_str = pf.to_json()
    assert "key" in json_str
    assert "value" in json_str


# ==============================================================================
# PHASE 3: PRESET & DATA STRESS TESTS
# ==============================================================================


def test_all_15_presets_loadable():
    """Test all 15 presets are loadable."""
    pm = PresetManager()
    assert pm.preset_count == 15


def test_all_presets_have_required_fields():
    """Test every preset has all required fields."""
    pm = PresetManager()
    required_fields = [
        "id",
        "name",
        "category",
        "track",
        "difficulty",
        "description",
        "target_user",
        "recommended_theme",
        "extension_count",
        "tags",
        "connects_to",
    ]
    for preset in pm.presets:
        for field in required_fields:
            assert hasattr(preset, field), f"Preset {preset.id} missing field {field}"


def test_all_presets_have_valid_categories():
    """Test all presets have valid categories."""
    pm = PresetManager()
    valid_categories = ["student", "professional", "lifestyle"]
    for preset in pm.presets:
        assert preset.category in valid_categories, f"Invalid category: {preset.category}"


def test_all_presets_have_valid_difficulty():
    """Test all presets have valid difficulty levels."""
    pm = PresetManager()
    valid_difficulties = ["beginner", "intermediate", "advanced"]
    for preset in pm.presets:
        assert preset.difficulty in valid_difficulties, f"Invalid difficulty: {preset.difficulty}"


def test_all_presets_extension_count_positive():
    """Test all presets have non-negative extension count."""
    pm = PresetManager()
    for preset in pm.presets:
        assert preset.extension_count >= 0


# ==============================================================================
# PHASE 5: QUIZ MODULE STRESS TESTS
# ==============================================================================


def test_quiz_engine_get_recommendation_by_quick_tags_empty():
    """Test quick tags with empty list."""
    qe = QuizEngine()
    results = qe.get_recommendation_by_quick_tags([])
    assert isinstance(results, list)


def test_quiz_engine_get_recommendation_by_quick_tags_single():
    """Test quick tags with single tag."""
    qe = QuizEngine()
    results = qe.get_recommendation_by_quick_tags(["python"])
    assert len(results) > 0


def test_quiz_engine_get_recommendation_by_quick_tags_limit():
    """Test quick tags respects limit."""
    qe = QuizEngine()
    results = qe.get_recommendation_by_quick_tags(["python"], limit=3)
    assert len(results) <= 3


def test_quiz_engine_reset_clears_state():
    """Test reset clears all internal state."""
    qe = QuizEngine()
    qe.collected_tags = ["python", "student"]
    qe.tag_weights = {"python": 1.0}
    qe.reset()
    assert qe.collected_tags == []
    assert qe.tag_weights == {}


def test_quiz_quickquiz_find_match_valid():
    """Test QuickQuiz find_match with valid query."""
    qq = QuickQuiz()
    matches = qq.find_match("python")
    assert isinstance(matches, list)


def test_quiz_quickquiz_find_match_empty():
    """Test QuickQuiz find_match with empty query returns search results."""
    qq = QuickQuiz()
    matches = qq.find_match("")
    assert isinstance(matches, list)


def test_quiz_quickquiz_find_match_special_chars():
    """Test QuickQuiz with special characters doesn't crash."""
    qq = QuickQuiz()
    matches = qq.find_match("../../../etc/passwd")
    assert isinstance(matches, list)


def test_quiz_quickquiz_suggestions():
    """Test getting suggestions returns list of tuples."""
    qq = QuickQuiz()
    suggestions = qq.get_suggestions()
    assert len(suggestions) > 0
    assert all(isinstance(s, tuple) and len(s) == 2 for s in suggestions)


# ==============================================================================
# PHASE 6: EXCEPTION HIERARCHY STRESS TESTS
# ==============================================================================


def test_exception_hierarchy_base():
    """Test ProjectVSCodeTemplatesError is subclass of Exception."""
    assert issubclass(ProjectVSCodeTemplatesError, Exception)


def test_exception_hierarchy_preset_not_found():
    """Test PresetNotFoundError is subclass of base."""
    assert issubclass(PresetNotFoundError, ProjectVSCodeTemplatesError)


def test_exception_hierarchy_validation():
    """Test ValidationError is subclass of base."""
    assert issubclass(ValidationError, ProjectVSCodeTemplatesError)


def test_exception_hierarchy_configuration():
    """Test ConfigurationError is subclass of base."""
    assert issubclass(ConfigurationError, ProjectVSCodeTemplatesError)


def test_exception_hierarchy_installation():
    """Test InstallationError is subclass of base."""
    assert issubclass(InstallationError, ProjectVSCodeTemplatesError)


def test_exception_hierarchy_backup():
    """Test BackupError is subclass of base."""
    assert issubclass(BackupError, ProjectVSCodeTemplatesError)


def test_exception_hierarchy_extension():
    """Test ExtensionError is subclass of base."""
    assert issubclass(ExtensionError, ProjectVSCodeTemplatesError)


def test_exception_catching_base_catches_all():
    """Test catching base exception catches all subclasses."""
    exceptions = [
        PresetNotFoundError("test"),
        ValidationError("test"),
        ConfigurationError("test"),
        InstallationError("test"),
        BackupError("test"),
        ExtensionError("test"),
    ]
    for exc in exceptions:
        assert isinstance(exc, ProjectVSCodeTemplatesError)


def test_exception_has_message():
    """Test all exceptions have non-empty message when constructed."""
    exceptions = [
        PresetNotFoundError("Test error message"),
        ValidationError("Test error message"),
        ConfigurationError("Test error message"),
        InstallationError("Test error message"),
        BackupError("Test error message"),
        ExtensionError("Test error message"),
    ]
    for exc in exceptions:
        assert len(str(exc)) > 0


def test_exception_preserves_cause():
    """Test exceptions preserve original cause."""
    original = ValueError("original error")
    try:
        raise ValidationError("wrapped error") from original
    except ValidationError as e:
        assert e.__cause__ is original


# ==============================================================================
# PHASE 7: IMPORT & VERSION STRESS TESTS
# ==============================================================================


def test_version_exact_match():
    """Test __version__ equals '1.1.2'."""
    assert __version__ == "1.1.2"


def test_version_constants_match():
    """Test constants VERSION matches __version__."""
    assert constants.PACKAGE_VERSION == "1.1.2"


def test_version_drift_guard():
    """Test version assertion in __init__.py works."""
    assert __version__ == constants.PACKAGE_VERSION


def test_all_exported_names_importable():
    """Test all names in __all__ are importable from package."""
    import projectvscodetemplates as pvt

    for name in pvt.__all__:
        assert hasattr(pvt, name), f"Missing export: {name}"


def test_all_exported_names_not_none():
    """Test no exported name is None."""
    import projectvscodetemplates as pvt

    for name in pvt.__all__:
        attr = getattr(pvt, name)
        assert attr is not None, f"Export {name} is None"


def test_all_exported_names_not_private():
    """Test no exported name starts with underscore except dunder names."""
    import projectvscodetemplates as pvt

    for name in pvt.__all__:
        if name.startswith("__"):
            assert name in ["__version__", "__author__", "__email__"], (
                f"Unexpected dunder in exports: {name}"
            )
        else:
            assert not name.startswith("_"), f"Private name in exports: {name}"


def test_package_import_multiple_times():
    """Test importing package multiple times doesn't crash."""
    for _ in range(10):
        importlib.reload(sys.modules["projectvscodetemplates"])
        importlib.reload(sys.modules["projectvscodetemplates.presets"])


def test_import_produces_no_output():
    """Test importing package produces no stdout/stderr output."""
    import subprocess

    result = subprocess.run(
        [sys.executable, "-c", "import projectvscodetemplates"],
        capture_output=True,
        text=True,
    )
    assert result.stdout == ""
    assert result.stderr == ""


# ==============================================================================
# PHASE 8: LOGGING STRESS TESTS
# ==============================================================================


def test_no_basic_config_in_library():
    """Test no module calls logging.basicConfig()."""
    src_dir = Path("src/projectvscodetemplates")
    for py_file in src_dir.glob("*.py"):
        if py_file.name == "__init__.py":
            continue
        content = py_file.read_text(encoding="utf-8")
        assert "logging.basicConfig" not in content, f"Found basicConfig in {py_file}"


# ==============================================================================
# PHASE 9: PERFORMANCE BASELINE TESTS
# ==============================================================================


def test_package_import_performance():
    """Test package import completes in under 500ms."""
    start = time.perf_counter()
    import projectvscodetemplates

    elapsed = time.perf_counter() - start
    assert elapsed < 0.5, f"Import took {elapsed:.3f}s — too slow"


def test_loading_all_presets_performance():
    """Test loading all 15 presets completes in under 1 second."""
    PresetManager._instance = None
    PresetManager._presets = None

    start = time.perf_counter()
    pm = PresetManager()
    _ = pm.presets
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"Loading presets took {elapsed:.3f}s — too slow"


def test_search_presets_performance():
    """Test search completes in under 200ms."""
    pm = PresetManager()
    start = time.perf_counter()
    _ = pm.search_presets("python")
    elapsed = time.perf_counter() - start
    assert elapsed < 0.2, f"Search took {elapsed:.3f}s — too slow"


def test_quick_tags_performance():
    """Test get_recommendation_by_quick_tags with many tags completes in under 2s."""
    qe = QuizEngine()
    many_tags = [f"tag{i}" for i in range(100)]
    start = time.perf_counter()
    _ = qe.get_recommendation_by_quick_tags(many_tags, limit=5)
    elapsed = time.perf_counter() - start
    assert elapsed < 2.0, f"Quick tags took {elapsed:.3f}s — too slow"


# ==============================================================================
# BOUNDARY CONDITIONS - Additional stress tests
# ==============================================================================


def test_search_very_long_string():
    """Test search with very long string doesn't crash."""
    pm = PresetManager()
    long_query = "a" * 10000
    results = pm.search_presets(long_query)
    assert isinstance(results, list)


def test_search_unicode_string():
    """Test search with unicode string doesn't crash."""
    pm = PresetManager()
    results = pm.search_presets("你好世界")
    assert isinstance(results, list)


def test_get_recommendations_many_tags():
    """Test recommendations with many tags."""
    pm = PresetManager()
    many_tags = ["python", "java", "rust", "go", "cpp"] * 20
    recs = pm.get_recommendations(many_tags)
    assert isinstance(recs, list)


def test_preset_file_to_json_indent():
    """Test to_json with different indent values."""
    pf = PresetFile(name="test", content={"key": "value"})
    json_0 = pf.to_json(indent=0)
    json_2 = pf.to_json(indent=2)
    json_10 = pf.to_json(indent=10)
    assert "key" in json_0
    assert "key" in json_2
    assert "key" in json_10
