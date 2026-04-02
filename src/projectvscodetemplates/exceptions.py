"""Custom exceptions for ProjectVSCodeTemplates."""


class ProjectVSCodeTemplatesError(Exception):
    """Base exception for all projectvscodetemplates errors."""

    pass


class PresetNotFoundError(ProjectVSCodeTemplatesError):
    """Raised when a requested preset cannot be found."""

    pass


class ValidationError(ProjectVSCodeTemplatesError):
    """Raised when input validation fails."""

    pass


class ConfigurationError(ProjectVSCodeTemplatesError):
    """Raised when there is a configuration error."""

    pass


class InstallationError(ProjectVSCodeTemplatesError):
    """Raised when preset installation fails."""

    pass


class BackupError(ProjectVSCodeTemplatesError):
    """Raised when backup operations fail."""

    pass


class ExtensionError(ProjectVSCodeTemplatesError):
    """Raised when extension operations fail."""

    pass
