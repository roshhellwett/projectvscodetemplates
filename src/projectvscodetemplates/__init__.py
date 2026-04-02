"""ProjectVSCodeTemplates - Ready-made VS Code configurations for developers and students."""

import logging

__version__ = "1.1.2"
__author__ = "Roshan Kr Singh"
__email__ = "roshankumar77630@gmail.com"

from projectvscodetemplates.presets import PresetManager, Preset
from projectvscodetemplates.installer import VSCodeInstaller
from projectvscodetemplates.backup import BackupManager
from projectvscodetemplates.extensions import ExtensionManager
from projectvscodetemplates.quiz import QuizEngine, QuickQuiz
from projectvscodetemplates.exceptions import (
    ProjectVSCodeTemplatesError,
    PresetNotFoundError,
    ValidationError,
    ConfigurationError,
    InstallationError,
    BackupError,
    ExtensionError,
)

from .constants import PACKAGE_VERSION

assert __version__ == PACKAGE_VERSION, (
    f"Version mismatch: __init__.py={__version__!r}, constants.py={PACKAGE_VERSION!r}"
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "PresetManager",
    "Preset",
    "VSCodeInstaller",
    "BackupManager",
    "ExtensionManager",
    "QuizEngine",
    "QuickQuiz",
    "ProjectVSCodeTemplatesError",
    "PresetNotFoundError",
    "ValidationError",
    "ConfigurationError",
    "InstallationError",
    "BackupError",
    "ExtensionError",
]
