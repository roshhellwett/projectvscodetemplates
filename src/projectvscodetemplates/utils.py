"""Utility functions for ProjectVSCodeTemplates."""

import logging
import os
import sys
import subprocess
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

__all__ = [
    "get_terminal_width",
    "is_interactive",
    "print_success",
    "print_error",
    "print_warning",
    "print_info",
    "print_header",
    "print_section",
    "print_menu_header",
    "clear_screen",
    "pause",
    "confirm",
    "safe_input",
    "select_from_list",
    "check_vscode_installed",
    "check_vscode_running",
    "run_command",
    "ensure_directory",
    "is_writable",
    "truncate_string",
    "format_list",
    "with_progress",
]

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

from projectvscodetemplates.constants import (
    IS_WINDOWS,
    IS_LINUX,
    SUCCESS_COLOR,
    ERROR_COLOR,
    WARNING_COLOR,
    INFO_COLOR,
    SPINNER_STYLE,
    MIN_TERMINAL_WIDTH,
    PANEL_BORDER_COLOR,
)

console = Console()


def get_terminal_width() -> int:
    """Get current terminal width with fallbacks."""
    try:
        width = os.get_terminal_size().columns
        return max(width, MIN_TERMINAL_WIDTH)
    except (OSError, ValueError):
        return 80


def is_interactive() -> bool:
    """Check if running in an interactive terminal."""
    try:
        return sys.stdin.isatty() and sys.stdout.isatty()
    except (AttributeError, ValueError):
        return False


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[{SUCCESS_COLOR}]OK[/] {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[{ERROR_COLOR}]X[/] {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[{WARNING_COLOR}]![/] {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[{INFO_COLOR}]i[/] {message}")


def print_header(title: str, subtitle: str | None = None) -> None:
    """Print a formatted header with optional subtitle."""
    from rich.box import SIMPLE

    text = Text(title, style="bold cyan")
    if subtitle:
        text.append(f"\n{subtitle}", style="dim")
    console.print(Panel(text, box=SIMPLE, padding=(0, 0)))


def print_section(title: str, width: int | None = None) -> None:
    """Print a section divider with title."""
    if width is None:
        width = min(get_terminal_width(), 90)
    console.print()
    console.print("[bold cyan]" + "=" * width + "[/]")
    console.print(
        "[bold cyan]|[/]"
        + " " * ((width - len(title) - 4) // 2)
        + "[bold white]"
        + title
        + "[/]"
        + " " * ((width - len(title) - 4) // 2)
        + "[bold cyan]|[/]"
    )
    console.print("[bold cyan]" + "=" * width + "[/]")
    console.print()


def print_menu_header(title: str, width: int | None = None) -> None:
    """Print a consistent section header using Rich Panel.

    Args:
        title: The header title to display
        width: Optional width (auto-calculated if not provided)
    """
    if width is None:
        width = min(get_terminal_width(), 46)

    panel = Panel(
        f"[bold]{title}[/]",
        border_style="cyan",
        width=width,
        padding=(0, 0),
    )
    console.print(f"\n{panel}\n")


def clear_screen() -> None:
    """Clear the terminal screen based on OS."""
    if IS_WINDOWS:
        os.system("cls")
    else:
        os.system("clear")


def pause(message: str = "Press Enter to continue...") -> None:
    """Pause execution and wait for user input."""
    if is_interactive():
        try:
            console.print()
            console.print(f"[dim]{message}[/dim]")
            input()
        except (KeyboardInterrupt, EOFError, AttributeError):
            pass


def confirm(message: str, default: bool = False) -> bool:
    """
    Ask user for confirmation with Y/N prompt.

    Args:
        message: The confirmation question
        default: Default value if user just presses Enter

    Returns:
        True if user confirmed, False otherwise
    """
    choices = "(y/n)"
    if default:
        choices = "(Y/n)" if default else "(y/N)"

    console.print()
    while True:
        try:
            console.print(f"{message} {choices}: ", end="")
            response = input().strip().lower()

            if not response:
                return default

            if response in ("y", "yes"):
                return True
            if response in ("n", "no"):
                return False

            print_warning("Please enter 'y' or 'n'")
        except (KeyboardInterrupt, EOFError):
            console.print()
            console.print("[yellow]Operation cancelled[/yellow]")
            return False


def safe_input(prompt: str, allow_empty: bool = False) -> str:
    """
    Safe input that handles interrupts gracefully.

    Args:
        prompt: The input prompt
        allow_empty: Whether to allow empty input

    Returns:
        User's input string
    """
    try:
        console.print(prompt, end="")
        result = input().strip()

        while not result and not allow_empty:
            print_warning("Input cannot be empty. Please try again.")
            console.print(prompt, end="")
            result = input().strip()

        return result
    except (KeyboardInterrupt, EOFError):
        console.print()
        console.print("[yellow]Operation cancelled by user[/yellow]")
        sys.exit(0)


def select_from_list(items: list[str], prompt: str = "Select an option") -> int | None:
    """
    Present a numbered list and let user select by number.

    Args:
        items: List of items to display
        prompt: Prompt message

    Returns:
        Selected index (0-based) or None if cancelled
    """
    if not items:
        return None

    for i, item in enumerate(items, 1):
        console.print(f"  [cyan]{i}.[/] {item}")

    console.print()
    choice = safe_input(f"{prompt} (1-{len(items)}, 0 to cancel): ", allow_empty=False)

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(items):
            return idx

    return None


def check_vscode_installed() -> bool:
    """Check if VS Code CLI is installed and in PATH."""
    try:
        if IS_WINDOWS:
            result = subprocess.run(
                ["where", "code"],
                capture_output=True,
                text=True,
                shell=True,
                timeout=5,
            )
        else:
            result = subprocess.run(
                ["which", "code"],
                capture_output=True,
                text=True,
                timeout=5,
            )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def check_vscode_running() -> bool:
    """Check if VS Code is currently running."""
    try:
        if IS_WINDOWS:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq Code.exe"],
                capture_output=True,
                text=True,
                shell=True,
                timeout=5,
            )
            return "Code.exe" in result.stdout
        elif IS_LINUX:
            result = subprocess.run(
                ["pgrep", "-x", "code"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        elif sys.platform == "darwin":
            result = subprocess.run(
                ["pgrep", "-x", "Code"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        return False
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def run_command(cmd: list[str], timeout: int = 30, capture: bool = True) -> tuple[int, str, str]:
    """
    Run a command and return the result.

    Args:
        cmd: Command and arguments as list
        timeout: Timeout in seconds
        capture: Whether to capture output

    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=timeout,
            shell=IS_WINDOWS,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except FileNotFoundError:
        return -1, "", "Command not found"
    except OSError as e:
        return -1, "", str(e)


def ensure_directory(path: Path) -> bool:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path

    Returns:
        True if directory exists or was created
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except (OSError, PermissionError):
        return False


def is_writable(path: Path) -> bool:
    """Check if a path is writable."""
    try:
        if path.exists():
            return os.access(path, os.W_OK)
        return os.access(path.parent, os.W_OK)
    except (OSError, PermissionError):
        return False


def truncate_string(s: str, max_length: int, suffix: str = "...") -> str:
    """Truncate a string to max length with suffix."""
    if len(s) <= max_length:
        return s
    return s[: max_length - len(suffix)] + suffix


def format_list(items: list[str], separator: str = ", ", max_items: int = 0) -> str:
    """Format a list of items as a string."""
    if max_items > 0 and len(items) > max_items:
        shown = items[:max_items]
        return separator.join(shown) + f" ... and {len(items) - max_items} more"
    return separator.join(items)


def with_progress(description: str, task: Any = None) -> Progress:
    """Create a progress context."""
    return Progress(
        SpinnerColumn(SPINNER_STYLE),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    )
