"""Stress tests for ProjectVSCodeTemplates."""

import sys
from pathlib import Path

from projectvscodetemplates.presets import get_preset_manager, PresetManager
from projectvscodetemplates.installer import VSCodeInstaller
from projectvscodetemplates.backup import BackupManager
from projectvscodetemplates.extensions import ExtensionManager
from projectvscodetemplates.quiz import QuizEngine, QuickQuiz, RecommendationResult


def test_preset_manager():
    """Test PresetManager thoroughly."""
    print("=" * 50)
    print("PRESET MANAGER STRESS TEST")
    print("=" * 50)

    pm = get_preset_manager()

    assert pm.preset_count == 15, f"Expected 15 presets, got {pm.preset_count}"
    print(f"[OK] Loaded {pm.preset_count} presets")

    p = pm.get_preset("python-beginner")
    assert p is not None, "Preset python-beginner not found"
    assert p.name == "Python Beginner"
    print(f"[OK] Get preset by ID: {p.name}")

    p_invalid = pm.get_preset("nonexistent")
    assert p_invalid is None, "Invalid preset should return None"
    print("[OK] Invalid preset returns None")

    cats = pm.get_categories()
    assert "student" in cats, "student category not found"
    assert "professional" in cats, "professional category not found"
    print(f"[OK] Categories: {cats}")

    diffs = pm.get_difficulties()
    assert "beginner" in diffs, "beginner difficulty not found"
    print(f"[OK] Difficulties: {diffs}")

    results = pm.search_presets("python")
    assert len(results) >= 3, f"Expected >= 3 python results, got {len(results)}"
    print(f"[OK] Search 'python': {len(results)} results")

    student_presets = pm.get_presets_by_category("student")
    assert len(student_presets) > 0, "No student presets found"
    print(f"[OK] Student presets: {len(student_presets)}")

    beginner_presets = pm.get_presets_by_difficulty("beginner")
    assert len(beginner_presets) > 0, "No beginner presets found"
    print(f"[OK] Beginner presets: {len(beginner_presets)}")

    exts = pm.get_extensions("python-beginner")
    assert len(exts) == 9, f"Expected 9 extensions, got {len(exts)}"
    print(f"[OK] Extensions for python-beginner: {len(exts)}")

    settings = pm.get_settings("python-beginner")
    assert settings is not None, "Settings not found"
    assert "editor.fontSize" in settings, "editor.fontSize not in settings"
    print(f"[OK] Settings keys: {len(settings)}")

    keybindings = pm.get_keybindings("python-beginner")
    assert keybindings is not None, "Keybindings not found"
    print(f"[OK] Keybindings loaded")

    stats = pm.get_statistics()
    assert stats["total_presets"] == 15
    assert stats["total_extensions"] > 0
    print(
        f"[OK] Statistics: {stats['total_presets']} presets, {stats['total_extensions']} extensions"
    )

    upgrade = pm.get_upgrade_path("python-beginner")
    assert len(upgrade) > 0, "No upgrade path found"
    print(f"[OK] Upgrade path: {[pr.name for pr in upgrade]}")

    recs = pm.get_recommendations(["python", "data"], exclude_id="python-beginner")
    assert len(recs) > 0, "No recommendations found"
    print(f"[OK] Recommendations: {[pr.name for pr in recs]}")

    matches = [pr for pr in pm.presets if pr.matches_any_tag(["student"])]
    assert len(matches) > 0, "No tag matches found"
    print(f"[OK] Tag matches: {len(matches)}")

    p_idx = pm.get_preset_by_index(0)
    assert p_idx is not None
    print(f"[OK] Get preset by index: {p_idx.name}")

    print("\n" + "=" * 50)
    print("ALL PRESET MANAGER TESTS PASSED!")
    print("=" * 50 + "\n")


def test_backup_manager():
    """Test BackupManager."""
    print("=" * 50)
    print("BACKUP MANAGER STRESS TEST")
    print("=" * 50)

    bm = BackupManager()

    backup = bm.create_backup(preset_id="test", description="Test backup")
    assert backup is not None, "Backup creation failed"
    print(f"[OK] Created backup: {backup.id}")

    backups = bm.list_backups()
    assert len(backups) > 0, "No backups listed"
    print(f"[OK] Listed {len(backups)} backups")

    stats = bm.get_backup_stats()
    assert stats["total_backups"] > 0
    print(f"[OK] Backup stats: {stats['total_backups']} backups")

    success = bm.restore_backup(backups[0].id)
    assert success, "Restore failed"
    print(f"[OK] Restored backup: {backups[0].id}")

    print("\n" + "=" * 50)
    print("ALL BACKUP MANAGER TESTS PASSED!")
    print("=" * 50 + "\n")


def test_quiz_engine():
    """Test QuizEngine."""
    print("=" * 50)
    print("QUIZ ENGINE STRESS TEST")
    print("=" * 50)

    qe = QuizEngine()

    assert len(qe.QUESTIONS) > 0, "No quiz questions"
    print(f"[OK] Quiz has {len(qe.QUESTIONS)} questions")

    qe.collected_tags = ["python", "beginner", "student"]
    qe.tag_weights = {tag: 1.0 for tag in qe.collected_tags}
    recs = qe._calculate_recommendations()
    assert len(recs) > 0, "No recommendations"
    assert all(isinstance(r, RecommendationResult) for r in recs), "Wrong return type"
    print(f"[OK] Got {len(recs)} recommendations for python+beginner+student")
    print(f"     Top match: {recs[0].preset.name} ({recs[0].confidence:.0%} confidence)")

    qe.reset()
    assert len(qe.collected_tags) == 0
    print("[OK] Quiz reset works")

    qq = QuickQuiz()
    matches = qq.find_match("python")
    assert len(matches) > 0, "Quick quiz found nothing"
    print(f"[OK] Quick quiz 'python': {len(matches)} matches")

    matches_empty = qq.find_match("xyz123nonexistent")
    print(f"[OK] Quick quiz edge case: {len(matches_empty)} matches")

    suggestions = qq.get_suggestions()
    assert len(suggestions) > 0
    print(f"[OK] Quick quiz suggestions: {len(suggestions)}")

    print("\n" + "=" * 50)
    print("ALL QUIZ ENGINE TESTS PASSED!")
    print("=" * 50 + "\n")


def test_installer():
    """Test VSCodeInstaller."""
    print("=" * 50)
    print("INSTALLER STRESS TEST")
    print("=" * 50)

    installer = VSCodeInstaller()

    installed = installer.get_installed_preset()
    print(f"[OK] Current installed preset: {installed}")

    files = installer.get_installed_files()
    assert "settings" in files
    assert "extensions" in files
    print(f"[OK] Installed files status: {files}")

    is_installed = installer.is_preset_installed("python-beginner")
    assert isinstance(is_installed, bool)
    print(f"[OK] python-beginner installed: {is_installed}")

    stats = installer.get_installation_statistics()
    assert "files_copied" in stats
    print(f"[OK] Installation statistics: {stats['files_copied']} files")

    print("\n" + "=" * 50)
    print("ALL INSTALLER TESTS PASSED!")
    print("=" * 50 + "\n")


def test_extension_manager():
    """Test ExtensionManager."""
    print("=" * 50)
    print("EXTENSION MANAGER STRESS TEST")
    print("=" * 50)

    em = ExtensionManager()

    is_available = em._is_code_available()
    print(f"[OK] VS Code CLI available: {is_available}")

    installed = em.get_installed_extensions()
    print(f"[OK] Installed extensions count: {len(installed)}")

    is_installed = em.is_extension_installed("ms-python.python")
    assert isinstance(is_installed, bool)
    print(f"[OK] ms-python.python installed: {is_installed}")

    statuses = em.get_extension_status(["ms-python.python", "nonexistent.ext"])
    assert "ms-python.python" in statuses
    print(f"[OK] Extension status check works")

    recs = em.recommend_extensions(["python", "data"])
    assert len(recs) > 0
    print(f"[OK] Recommended {len(recs)} extensions")

    search_results = em.search_by_keyword("python")
    print(f"[OK] Search by keyword: {len(search_results)} results")

    stats = em.get_statistics()
    assert "total_installed" in stats
    print(f"[OK] Extension statistics: {stats['total_installed']} installed")

    valid_id = em.validate_extension_id("ms-python.python")
    assert valid_id is True
    invalid_id = em.validate_extension_id("invalid")
    assert invalid_id is False
    print("[OK] Extension ID validation works")

    missing = em.get_missing_extensions(["ms-python.python", "nonexistent.ext"])
    assert "nonexistent.ext" in missing
    print(f"[OK] Missing extensions: {missing}")

    print("\n" + "=" * 50)
    print("ALL EXTENSION MANAGER TESTS PASSED!")
    print("=" * 50 + "\n")


def run_all_tests():
    """Run all stress tests."""
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + " PROJECTVSCODE TEMPLATES STRESS TESTS ".center(58) + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    print()

    try:
        test_preset_manager()
        test_backup_manager()
        test_quiz_engine()
        test_installer()
        test_extension_manager()

        print("\n" + "#" * 60)
        print("#" + " ALL STRESS TESTS PASSED! ".center(59) + "#")
        print("#" * 60 + "\n")

        return 0
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
