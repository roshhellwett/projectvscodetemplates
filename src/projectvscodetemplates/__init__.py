"""ProjectVSCodeTemplates - Ready-made VS Code configurations for developers and students."""

__version__ = "1.0.0"
__author__ = "Roshan Kr Singh"
__email__ = "roshankumar77630@gmail.com"

from projectvscodetemplates.presets import PresetManager, Preset
from projectvscodetemplates.installer import VSCodeInstaller
from projectvscodetemplates.backup import BackupManager
from projectvscodetemplates.extensions import ExtensionManager
from projectvscodetemplates.quiz import QuizEngine, QuickQuiz

__all__ = [
    "__version__",
    "__author__",
    "PresetManager",
    "Preset",
    "VSCodeInstaller",
    "BackupManager",
    "ExtensionManager",
    "QuizEngine",
    "QuickQuiz",
]
