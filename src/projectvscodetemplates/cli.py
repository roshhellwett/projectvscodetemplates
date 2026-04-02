"""Premium CLI interface for ProjectVSCodeTemplates."""

import sys
import subprocess
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.markdown import Markdown

from projectvscodetemplates import __version__
from projectvscodetemplates.presets import get_preset_manager, Preset
from projectvscodetemplates.installer import VSCodeInstaller
from projectvscodetemplates.backup import BackupManager
from projectvscodetemplates.extensions import ExtensionManager
from projectvscodetemplates.quiz import QuizEngine, QuickQuiz
from projectvscodetemplates.constants import (
    PACKAGE_NAME,
    IS_WINDOWS,
    IS_LINUX,
    IS_MACOS,
    MENU_WIDTH,
    SUCCESS_COLOR,
    ERROR_COLOR,
    WARNING_COLOR,
    INFO_COLOR,
    MAX_ITEMS_PREVIEW,
    PIP_CHECK_TIMEOUT,
    MENU_EXIT,
    MENU_BROWSE,
    MENU_QUIZ,
    MENU_SEARCH,
    MENU_INSTALL,
    MENU_VIEW,
    MENU_UNINSTALL,
    MENU_BACKUP,
    MENU_EXTENSIONS,
    MENU_UPDATE,
    MENU_HELP,
    MENU_ABOUT,
)
from projectvscodetemplates.utils import (
    print_success,
    print_error,
    print_warning,
    print_info,
    print_header,
    print_section,
    print_menu_header,
    clear_screen,
    pause,
    safe_input,
    confirm,
    is_interactive,
    check_vscode_installed,
    check_vscode_running,
    get_terminal_width,
)

if IS_WINDOWS:
    console = Console(legacy_windows=False)
else:
    console = Console()
app = typer.Typer(
    name=PACKAGE_NAME,
    help="Ready-made VS Code configurations for developers and students",
    add_completion=False,
)


class MenuState:
    """Manages menu state and navigation."""

    def __init__(self):
        self.preset_manager = get_preset_manager()
        self.installer = VSCodeInstaller(self.preset_manager)
        self.backup_manager = BackupManager()
        self.extension_manager = ExtensionManager(self.preset_manager)
        self.quiz_engine = QuizEngine(self.preset_manager)
        self.quick_quiz = QuickQuiz(self.preset_manager)
        self.running = True

    def show_welcome(self) -> None:
        """Show welcome banner."""
        width = min(get_terminal_width(), 80)

        welcome_text = f"""
[bold cyan]Welcome to ProjectVSCodeTemplates![/]

Your ultimate VS Code configuration manager.
Choose from [bold]{self.preset_manager.preset_count}[/] curated presets
tailored for different development needs.

[dim]Platform:[/] {"Windows" if IS_WINDOWS else "Linux" if IS_LINUX else "macOS"}
[dim]VS Code:[/] {"[green]Detected[/]" if check_vscode_installed() else "[yellow]Not in PATH[/]"}
"""

        panel = Panel(
            welcome_text.strip(),
            title=f"[bold]v{__version__}[/]",
            border_style="cyan",
            width=width,
        )
        console.print(panel)

    def show_main_menu(self) -> str:
        """Display main menu and get user choice."""
        clear_screen()
        self.show_welcome()

        installed = self.installer.get_installed_preset()
        if installed:
            console.print(
                f"\n[dim]Currently installed:[/] [cyan]{installed.preset_name or installed.preset_id}[/]"
            )

        menu_items = [
            ("1", "Browse & Preview Presets"),
            ("2", "Find Perfect Preset (Quiz)"),
            ("3", "Search Presets"),
            ("4", "Install a Preset"),
            ("5", "View Installed Preset"),
            ("6", "Remove/Uninstall Preset"),
            ("7", "Backup & Restore"),
            ("8", "Install Extensions Only"),
            ("9", "Update projectvscodetemplates"),
            ("10", "Help & Commands"),
            ("11", "About"),
            ("0", "Exit"),
        ]

        menu_text = "\n".join(f"[yellow]{num:>2}.[/]  {text}" for num, text in menu_items)

        menu_panel = Panel(
            menu_text,
            title="[bold]Main Menu Options[/]",
            border_style="cyan",
            padding=(0, 2),
        )
        console.print(menu_panel)

        return safe_input("Enter your choice (0-11): ", allow_empty=False)

    def handle_browse_presets(self) -> None:
        """Handle browse presets option."""
        clear_screen()
        print_menu_header("Browse & Preview Presets")

        categories = self.preset_manager.get_categories()

        console.print("[bold]Filter by category:[/]")
        console.print("  [dim]0.[/] All Presets")
        for i, cat in enumerate(categories, 1):
            console.print(f"  [dim]{i}.[/] {cat.title()}")
        console.print()

        choice = safe_input("Select category (0-{}): ".format(len(categories)), allow_empty=True)

        presets = self.preset_manager.presets

        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(categories):
                presets = self.preset_manager.get_presets_by_category(categories[idx - 1])

        self._display_preset_table(presets)

        console.print(
            "\n[cyan]Enter number (1-{}) or preset ID (or press Enter to go back):[/]".format(
                len(presets)
            )
        )
        user_input = safe_input(">> ", allow_empty=True)

        if user_input:
            preset = None

            if user_input.isdigit():
                idx = int(user_input) - 1
                if 0 <= idx < len(presets):
                    preset = presets[idx]

            if not preset:
                preset = self.preset_manager.get_preset(user_input.strip())

            if preset:
                self._show_preset_detail(preset)
            else:
                print_warning("Preset not found. Enter a number or preset ID.")

        pause()

    def _display_preset_table(self, presets: list[Preset]) -> None:
        """Display presets in a formatted table."""
        table = Table(
            show_header=True,
            header_style="bold cyan",
            show_lines=True,
            expand=False,
        )
        table.add_column("#", style="dim", width=3)
        table.add_column("Preset Name", width=30)
        table.add_column("Category", width=13)
        table.add_column("Level", width=13)
        table.add_column("Ext", justify="center", width=4)

        for i, preset in enumerate(presets, 1):
            diff_color = (
                "[green]"
                if preset.difficulty == "beginner"
                else "[yellow]"
                if preset.difficulty == "intermediate"
                else "[red]"
            )
            table.add_row(
                str(i),
                preset.name,
                preset.category.title(),
                f"{diff_color}{preset.difficulty.title()}[/]",
                str(preset.extension_count),
            )

        console.print(table)
        console.print(f"\n[dim]Showing {len(presets)} preset(s)[/]")

    def _show_preset_detail(self, preset: Preset) -> None:
        """Show detailed information about a preset."""
        clear_screen()

        console.print(f"\n[bold cyan]+------------------------------------------------------+[/]")
        console.print(
            f"[bold cyan]|[/]  [bold]{preset.name}[/]                                   [bold cyan]|[/]"
        )
        console.print(f"[bold cyan]+------------------------------------------------------+[/]\n")

        console.print(f"[bold cyan]Description:[/]")
        console.print(f"  {preset.description}\n")
        console.print(f"[bold cyan]Target User:[/] {preset.target_user}\n")

        details = Table(show_header=False, box=None)
        details.add_column("Field", style="cyan", width=14)
        details.add_column("Value")

        diff_color = (
            "[green]"
            if preset.difficulty == "beginner"
            else "[yellow]"
            if preset.difficulty == "intermediate"
            else "[red]"
        )
        details.add_row("ID", f"[cyan]{preset.id}[/]")
        details.add_row("Category", preset.category.title())
        details.add_row("Track", preset.track.title())
        details.add_row("Difficulty", f"{diff_color}{preset.difficulty.title()}[/]")
        details.add_row("Extensions", str(preset.extension_count))
        details.add_row("Theme", preset.recommended_theme)

        console.print(details)
        console.print()

        console.print("[bold cyan]Tags:[/] ", end="")
        tags_str = "  ".join(f"[dim]{tag}[/]" for tag in preset.tags)
        console.print(tags_str)

        if preset.connects_to:
            console.print("\n[bold cyan]Upgrade Path:[/]")
            for target_id in preset.connects_to:
                target = self.preset_manager.get_preset(target_id)
                if target:
                    console.print(f"  -> {target.name} ({target_id})")

        extensions = self.preset_manager.get_extensions(preset.id)
        if extensions:
            console.print(f"\n[bold]Extensions ({len(extensions)}):[/]")
            for ext in extensions[:10]:
                console.print(f"  * [dim]{ext}[/]")
            if len(extensions) > 10:
                console.print(f"  [dim]... and {len(extensions) - 10} more[/]")

        if check_vscode_running():
            console.print(
                "\n[yellow]! VS Code is running. Restart required for changes to take effect.[/]"
            )

    def handle_quiz(self) -> None:
        """Handle the preset recommendation quiz."""
        clear_screen()
        recommendations = self.quiz_engine.run_quiz()

        if not recommendations:
            console.print("[yellow]No recommendations found. Try different answers.[/]")
            pause()
            return

        self.quiz_engine.display_recommendations(recommendations)

        console.print("\n[bold]Would you like to install one of these presets?[/]")
        console.print("[dim](Enter the number or preset ID, or press Enter to go back)[/]")

        choice = safe_input(">> ", allow_empty=True)

        if choice:
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(recommendations):
                    result = recommendations[idx]
                    self._install_preset_with_confirmation(result.preset)
            else:
                preset = self.preset_manager.get_preset(choice.strip())
                if preset:
                    self._install_preset_with_confirmation(preset)
                else:
                    print_warning("Preset not found")

        pause()

    def handle_search(self) -> None:
        """Handle preset search."""
        clear_screen()
        console.print("\n[bold cyan]+--------------------------------------------------------+[/]")
        console.print(
            "[bold cyan]|[/]              [bold]Search Presets[/]                        [bold cyan]|[/]"
        )
        console.print("[bold cyan]+--------------------------------------------------------+[/]\n")

        query = safe_input("Enter search term: ", allow_empty=False)

        results = self.preset_manager.search_presets(query)

        if not results:
            console.print("\n[yellow]No presets found matching your search.[/]\n")

            quick_results = self.quick_quiz.find_match(query)
            if quick_results:
                console.print("[bold]Did you mean:[/]")
                for i, preset in enumerate(quick_results[:3], 1):
                    console.print(f"  {i}. {preset.name}")
        else:
            console.print(f"\n[green]Found {len(results)} matching preset(s):[/]\n")
            self._display_preset_table(results)

            console.print("\n[cyan]Enter number or preset ID to preview:[/]")
            user_input = safe_input(">> ", allow_empty=True)

            if user_input:
                preset = None

                if user_input.isdigit():
                    idx = int(user_input) - 1
                    if 0 <= idx < len(results):
                        preset = results[idx]

                if not preset:
                    preset = self.preset_manager.get_preset(user_input.strip())

                if preset:
                    self._show_preset_detail(preset)

        pause()

    def handle_install(self) -> None:
        """Handle preset installation."""
        clear_screen()
        print_menu_header("Install a Preset")

        installed = self.installer.get_installed_preset()
        if installed:
            console.print(
                f"[yellow]Warning:[/] You have '{installed.preset_name or installed.preset_id}' installed."
            )
            console.print("[dim]Installing a new preset will replace your current settings.\n[/]")

        self._display_preset_table(self.preset_manager.presets)

        console.print(
            "\n[cyan]Enter the number (1-{}) or preset ID:[/]".format(
                len(self.preset_manager.presets)
            )
        )
        user_input = safe_input(">> ", allow_empty=False).strip()

        preset = None

        if user_input.isdigit():
            idx = int(user_input) - 1
            if 0 <= idx < len(self.preset_manager.presets):
                preset = self.preset_manager.presets[idx]

        if not preset:
            preset = self.preset_manager.get_preset(user_input)

        if preset:
            self._install_preset_with_confirmation(preset)
        else:
            max_num = len(self.preset_manager.presets)
            print_error(f"'{user_input}' not found. Enter a number (1-{max_num}) or preset ID.")

        pause()

    def _install_preset_with_confirmation(self, preset: Preset) -> None:
        """Install a preset with user confirmation."""
        clear_screen()

        print_menu_header("Ready to Install")

        console.print(f"[bold cyan]Preset:[/] [white]{preset.name}[/]")
        console.print(f"[bold cyan]ID:[/] [cyan]{preset.id}[/]\n")
        console.print(f"[bold cyan]Description:[/]")
        console.print(f"  {preset.description}\n")
        console.print(f"[bold cyan]Extensions:[/] {preset.extension_count} will be configured\n")

        if not check_vscode_installed():
            console.print("[yellow]! VS Code CLI not detected in PATH.[/]")
            console.print("[dim]  Extensions will be configured but not auto-installed.[/]\n")

        console.print("[bold]This will:[/]")
        console.print("  1. [dim]Backup current settings (if any)[/]")
        console.print("  2. Install settings.json")
        console.print("  3. Configure extensions.json")
        console.print("  4. Install keybindings (if available)")
        console.print("  5. Install code snippets (if available)")
        console.print()

        if check_vscode_running():
            console.print(
                "[yellow]! VS Code is currently running. Please restart after installation.[/]\n"
            )

        if confirm("Proceed with installation?", default=True):
            self._do_install(preset)

    def _do_install(self, preset: Preset) -> None:
        """Perform the actual installation."""
        console.print(f"\n[cyan]Installing {preset.name}...[/]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("Creating backup...", total=None)
            backup = self.backup_manager.create_backup(preset_id=preset.id)

            progress.update(task, description="Installing preset...")
            result = self.installer.install(
                preset_id=preset.id,
                create_backup=False,
            )

            progress.update(task, description="Done!")

        if result.success:
            console.print()
            print_success(f"Successfully installed {preset.name}!")

            if backup:
                console.print(f"[dim]Backup created: {backup.path}[/]")

            if result.warnings:
                console.print("\n[yellow]Warnings:[/]")
                for warning in result.warnings:
                    console.print(f"  * {warning}")

            console.print("\n[bold]Installed files:[/]")
            for file in result.files_copied[:5]:
                console.print(f"  * [green]{file}[/]")
            if len(result.files_copied) > 5:
                console.print(f"  [dim]... and {len(result.files_copied) - 5} more[/]")
        else:
            console.print()
            print_error(f"Installation failed: {result.errors}")

    def handle_view_installed(self) -> None:
        """Handle view installed preset."""
        clear_screen()
        print_menu_header("View Installed Preset")

        installed = self.installer.get_installed_preset()

        if not installed:
            console.print(
                "[yellow]No preset is currently installed via projectvscodetemplates.[/]\n"
            )

            files_exist = self.installer.get_installed_files()
            if any(files_exist.values()):
                console.print("[dim]However, VS Code configuration files exist at:[/]")
                from projectvscodetemplates.constants import get_vscode_config_dir

                console.print(f"  [dim]{get_vscode_config_dir()}[/]\n")
        else:
            console.print(
                f"[bold cyan]Currently Installed:[/] [white]{installed.preset_name or installed.preset_id}[/]\n"
            )
            console.print(
                f"[dim]Installed at:[/] {installed.installed_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            )

            if installed.files:
                console.print("[bold cyan]Installed files:[/]")
                for file in installed.files[:10]:
                    console.print(f"  * {Path(file).name}")
                if len(installed.files) > 10:
                    console.print(f"  [dim]... and {len(installed.files) - 10} more[/]")

            if installed.preset_id:
                preset = self.preset_manager.get_preset(installed.preset_id)
                if preset:
                    console.print()
                    upgrade_path = self.preset_manager.get_upgrade_path(preset.id)
                    if upgrade_path:
                        console.print("[bold]Upgrade available:[/]")
                        for target in upgrade_path:
                            console.print(f"  -> [cyan]{target.name}[/]")

        pause()

    def handle_uninstall(self) -> None:
        """Handle preset uninstallation."""
        clear_screen()
        print_menu_header("Remove/Uninstall Preset")

        installed = self.installer.get_installed_preset()

        if not installed:
            console.print("[yellow]No preset is currently installed.[/]\n")
        else:
            console.print(
                f"[bold cyan]Current preset:[/] [white]{installed.preset_name or installed.preset_id}[/]\n"
            )

            console.print(
                "[yellow]This will restore your previous VS Code settings from backup.[/]\n"
            )

            if confirm("Proceed with uninstallation?", default=False):
                console.print("\n[cyan]Restoring previous settings...[/]\n")

                success = self.installer.uninstall()

                if success:
                    print_success("Preset uninstalled successfully!")
                    console.print("[dim]Your previous settings have been restored.[/]\n")
                else:
                    print_error("Failed to restore settings")

        pause()

    def handle_backup_restore(self) -> None:
        """Handle backup and restore operations."""
        while True:
            clear_screen()
            print_menu_header("Backup & Restore")

            stats = self.backup_manager.get_backup_stats()
            console.print(f"[bold]Total Backups:[/] {stats['total_backups']}")
            if stats["total_backups"] > 0:
                newest = stats.get("newest_backup")
                if newest:
                    console.print(
                        f"[dim]Newest:[/] {newest.get('created_at', 'N/A')[:19].replace('T', ' ')}"
                    )

            console.print("\n[bold]Options:[/]")
            console.print("  1. Create Backup")
            console.print("  2. List Backups")
            console.print("  3. Restore from Backup")
            console.print("  4. Delete a Backup")
            console.print("  5. Delete Old Backups (keep 5)")
            console.print("  0. Back to Main Menu")

            console.print()
            choice = safe_input("Enter choice: ", allow_empty=False)

            if choice == "0":
                break
            elif choice == "1":
                self._handle_create_backup()
            elif choice == "2":
                self._handle_list_backups()
            elif choice == "3":
                self._handle_restore_backup()
            elif choice == "4":
                self._handle_delete_backup()
            elif choice == "5":
                self._handle_delete_old_backups()

    def _handle_create_backup(self) -> None:
        """Create a new backup."""
        clear_screen()
        console.print("\n[bold cyan]Create New Backup[/]\n")

        desc = safe_input("Description (optional, press Enter to skip): ", allow_empty=True)

        console.print("\n[cyan]Creating backup...[/]")
        backup = self.backup_manager.create_backup(description=desc)

        if backup:
            print_success(f"Backup created successfully!")
            console.print(f"[dim]Backup ID:[/] {backup.id}")
            console.print(f"[dim]Location:[/] {backup.path}")
            console.print(f"[dim]Size:[/] {backup.size_bytes / 1024:.1f} KB")
        else:
            print_error("Failed to create backup")

        pause()

    def _handle_list_backups(self) -> None:
        """List all backups."""
        clear_screen()
        console.print("\n[bold cyan]Available Backups[/]\n")

        backups = self.backup_manager.list_backups()

        if not backups:
            console.print("[yellow]No backups found.[/]\n")
        else:
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("#", width=4)
            table.add_column("ID", width=18)
            table.add_column("Created", width=20)
            table.add_column("Preset", width=25)
            table.add_column("Size", width=10)

            for i, backup in enumerate(backups, 1):
                size_kb = backup.size_bytes / 1024
                table.add_row(
                    str(i),
                    backup.id,
                    backup.created_at_str,
                    backup.preset_id or "[dim]Unknown[/]",
                    f"{size_kb:.1f} KB",
                )

            console.print(table)

        pause()

    def _handle_restore_backup(self) -> None:
        """Restore from a backup."""
        clear_screen()
        console.print("\n[bold cyan]Restore from Backup[/]\n")

        backups = self.backup_manager.list_backups()

        if not backups:
            console.print("[yellow]No backups available to restore.[/]\n")
            pause()
            return

        console.print("Available backups:\n")
        for i, backup in enumerate(backups[:10], 1):
            console.print(f"  {i}. {backup.id} - {backup.created_at_str}")
            if backup.preset_id:
                console.print(f"     Preset: {backup.preset_id}")

        console.print()
        choice = safe_input("Enter backup number to restore: ", allow_empty=False)

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(backups):
                backup = backups[idx]

                console.print(
                    f"\n[yellow]This will restore backup from {backup.created_at_str}.[/]"
                )

                if confirm("Proceed?", default=False):
                    success = self.backup_manager.restore_backup(backup.id)

                    if success:
                        print_success("Backup restored successfully!")
                    else:
                        print_error("Failed to restore backup")

        pause()

    def _handle_delete_backup(self) -> None:
        """Delete a specific backup."""
        clear_screen()
        console.print("\n[bold cyan]Delete Backup[/]\n")

        backups = self.backup_manager.list_backups()

        if not backups:
            console.print("[yellow]No backups to delete.[/]\n")
            pause()
            return

        for i, backup in enumerate(backups[:10], 1):
            console.print(f"  {i}. {backup.id} - {backup.created_at_str}")

        console.print()
        choice = safe_input("Enter backup number to delete (0 to cancel): ", allow_empty=False)

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(backups):
                backup = backups[idx]

                if confirm(f"Delete backup {backup.id}?", default=False):
                    if self.backup_manager.delete_backup(backup.id):
                        print_success("Backup deleted")
                    else:
                        print_error("Failed to delete backup")

        pause()

    def _handle_delete_old_backups(self) -> None:
        """Delete old backups keeping only recent ones."""
        clear_screen()
        console.print("\n[bold cyan]Delete Old Backups[/]\n")

        deleted = self.backup_manager.delete_old_backups(keep_count=5)

        if deleted > 0:
            print_success(f"Deleted {deleted} old backup(s)")
        else:
            console.print("[dim]No old backups to delete (keeping 5 most recent).[/]")

        pause()

    def handle_install_extensions(self) -> None:
        """Handle installing extensions only."""
        clear_screen()
        print_menu_header("Install Extensions Only")

        if not check_vscode_installed():
            console.print(
                "[yellow]! VS Code CLI not detected. Extensions cannot be auto-installed.[/]"
            )
            console.print("[dim]  But we can show you the extension IDs to install manually.\n[/]")

        self._display_preset_table(self.preset_manager.presets)

        console.print()
        preset_id = safe_input("Enter preset number or ID: ", allow_empty=False).strip()

        preset = None

        if preset_id.isdigit():
            idx = int(preset_id) - 1
            if 0 <= idx < len(self.preset_manager.presets):
                preset = self.preset_manager.presets[idx]

        if not preset:
            preset = self.preset_manager.get_preset(preset_id)

        if not preset:
            print_error(f"Preset '{preset_id}' not found")
            pause()
            return

        extensions = self.preset_manager.get_extensions(preset.id)

        clear_screen()
        print_menu_header(f"Extensions for {preset.name}")

        if not extensions:
            console.print("[yellow]No extensions defined for this preset.[/]")
        else:
            for ext in extensions:
                installed = self.extension_manager.is_extension_installed(ext)
                status = "[green]Installed[/]" if installed else "[dim]Not installed[/]"
                console.print(f"  * {ext}")
                console.print(f"    {status}")

            console.print(f"\n[cyan]Total:[/] {len(extensions)} extensions\n")

            if check_vscode_installed():
                if confirm("Install all extensions?", default=True):
                    results = self.extension_manager.install_preset_extensions(preset.id)

                    success_count = sum(1 for r in results.values() if r.success)
                    console.print(
                        f"\n[green]Installed {success_count}/{len(results)} extensions[/]"
                    )

        pause()

    def handle_update(self) -> None:
        """Handle package update."""
        clear_screen()
        print_menu_header("Update projectvscodetemplates")

        console.print(f"[bold cyan]Current version:[/] [white]{__version__}[/]\n")
        console.print("[cyan]Checking for updates...[/]\n")

        try:
            result = subprocess.run(
                ["pip", "index", "versions", PACKAGE_NAME],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                import re

                version_match = re.search(r"Available versions: (.+)", result.stdout)
                if version_match:
                    latest = version_match.group(1).split(",")[0].strip()
                    console.print(f"[bold cyan]Latest version:[/] [white]{latest}[/]")

                    if latest != __version__:
                        console.print("\n[yellow]A new version is available![/]\n")

                        if confirm("Update now?", default=True):
                            console.print("\n[cyan]Updating...[/]\n")

                            update_result = subprocess.run(
                                ["pip", "install", "--upgrade", PACKAGE_NAME],
                                capture_output=True,
                                text=True,
                            )

                            if update_result.returncode == 0:
                                print_success("Updated successfully!")
                                console.print("[dim]Please restart the application.[/]")
                            else:
                                print_error("Update failed")
                    else:
                        console.print("\n[green]You're using the latest version![/]\n")
            else:
                console.print("[yellow]Could not check for updates.[/]\n")

        except Exception as e:
            console.print(f"[yellow]Update check failed: {e}[/]\n")

        pause()

    def handle_help(self) -> None:
        """Show help and CLI commands."""
        clear_screen()

        help_text = """
# ProjectVSCodeTemplates - Help & Commands

## Menu Options

1. **Browse & Preview** - View all available presets with details
2. **Find My Perfect Preset** - Interactive quiz to find the best preset
3. **Search Presets** - Search presets by name, tags, or description
4. **Install a Preset** - Install a selected preset to VS Code
5. **View Installed** - See which preset is currently installed
6. **Remove/Uninstall** - Remove installed preset and restore backup
7. **Backup & Restore** - Manage VS Code configuration backups
8. **Install Extensions** - Install extensions from a preset only
9. **Update** - Check and install updates
10. **Help & Commands** - Show this help
11. **About** - About this project

## CLI Commands

```bash
# Interactive menu
python -m projectvscodetemplates start

# Quick commands (when installed via pip)
projectvscodetemplates list              # List all presets
projectvscodetemplates browse            # Browse presets
projectvscodetemplates install <id>      # Install preset
projectvscodetemplates search <query>    # Search presets
projectvscodetemplates quiz             # Run recommendation quiz
projectvscodetemplates update            # Check for updates
```

## Configuration Locations

- **VS Code Settings:** `%APPDATA%/Code/User/` (Windows)
- **VS Code Settings:** `~/.config/Code/User/` (Linux)
- **Backups:** Same as VS Code settings + `projectvscodetemplates_backups/`

## Tips

- Always restart VS Code after installing a preset
- Use the quiz to get personalized recommendations
- Backups are created automatically before installations
- You can install multiple presets but only one is "active"
"""

        md = Markdown(help_text)
        console.print(md)
        pause()

    def handle_about(self) -> None:
        """Show about information."""
        clear_screen()

        about_text = """
# About ProjectVSCodeTemplates

## Version
**1.0.0**

## Description
Ready-made VS Code configurations for developers and students. 
Choose from 15+ curated presets tailored for different development needs.

## Features
- 15+ Professional VS Code presets
- Interactive preset recommendation quiz
- Easy installation with automatic backups
- Extension management
- Cross-platform support (Windows, Linux, macOS)

## Author
**Roshan Kr Singh**  
Zenith Open Source Projects

## Repository
https://github.com/zenithopensourceprojects/projectvscodetemplates

## License
MIT License

## Preset Categories
- 📚 Student - Learning and education focused
- 💼 Professional - Career and production ready
- 🌿 Lifestyle - Personal and creative workflows
"""

        md = Markdown(about_text)
        console.print(md)
        pause()

    def run(self) -> None:
        """Run the main menu loop."""
        while self.running:
            try:
                choice = self.show_main_menu()

                handlers = {
                    "1": self.handle_browse_presets,
                    "2": self.handle_quiz,
                    "3": self.handle_search,
                    "4": self.handle_install,
                    "5": self.handle_view_installed,
                    "6": self.handle_uninstall,
                    "7": self.handle_backup_restore,
                    "8": self.handle_install_extensions,
                    "9": self.handle_update,
                    "10": self.handle_help,
                    "11": self.handle_about,
                    "0": self._exit,
                }

                handler = handlers.get(choice)
                if handler:
                    handler()
                else:
                    print_warning("Invalid choice. Please try again.")
                    pause()

            except KeyboardInterrupt:
                console.print("\n\n[yellow]Interrupted. Press 0 to exit.[/]")
                pause()
            except Exception as e:
                print_error(f"An error occurred: {e}")
                pause()

    def _exit(self) -> None:
        """Exit the application."""
        self.running = False
        clear_screen()
        console.print("\n[cyan]Thank you for using ProjectVSCodeTemplates![/]\n")
        console.print("[dim]Made with ❤️ for developers[/]\n")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Main entry point."""
    if ctx.invoked_subcommand is None:
        state = MenuState()
        state.run()


@app.command()
def start():
    """Launch the interactive menu."""
    state = MenuState()
    state.run()


def _call_list_presets():
    """Helper to list all presets."""
    manager = get_preset_manager()
    presets = manager.presets

    term_width = min(get_terminal_width(), 90)

    console.print()
    console.print("[bold cyan]" + "=" * term_width + "[/]")
    console.print(
        "[bold cyan]|[/]"
        + " " * 17
        + "[bold white]Preset List[/]"
        + " " * (term_width - 38)
        + "[bold cyan]|[/]"
    )
    console.print("[bold cyan]" + "=" * term_width + "[/]")
    console.print()

    for i, p in enumerate(presets, 1):
        diff_color = (
            "[green]"
            if p.difficulty == "beginner"
            else "[yellow]"
            if p.difficulty == "intermediate"
            else "[red]"
        )
        name = p.name[:30] + "..." if len(p.name) > 30 else p.name
        cat = p.category.title()[:12]
        diff = f"{diff_color}{p.difficulty.title()}[/]"

        console.print(
            f"  [cyan]{i:2}.[/] [white]{name:<32}[/] [dim]{cat:<12}[/] {diff:<14} Ext: {p.extension_count}"
        )

    console.print()
    console.print(f"[dim]Total: {len(presets)} presets[/]")


@app.command("list")
def list_presets(
    category: str = typer.Option(None, "--category", "-c", help="Filter by category"),
    difficulty: str = typer.Option(None, "--difficulty", "-d", help="Filter by difficulty"),
):
    """List all presets."""
    manager = get_preset_manager()
    presets = manager.presets

    if category:
        presets = manager.get_presets_by_category(category)
    if difficulty:
        presets = manager.get_presets_by_difficulty(difficulty)

    term_width = min(get_terminal_width(), 90)

    console.print()
    console.print("[bold cyan]" + "=" * term_width + "[/]")
    console.print(
        "[bold cyan]|[/]"
        + " " * 17
        + "[bold white]Preset List[/]"
        + " " * (term_width - 38)
        + "[bold cyan]|[/]"
    )
    console.print("[bold cyan]" + "=" * term_width + "[/]")
    console.print()

    for i, p in enumerate(presets, 1):
        diff_color = (
            "[green]"
            if p.difficulty == "beginner"
            else "[yellow]"
            if p.difficulty == "intermediate"
            else "[red]"
        )
        name = p.name[:30] + "..." if len(p.name) > 30 else p.name
        cat = p.category.title()[:12]
        diff = f"{diff_color}{p.difficulty.title()}[/]"

        console.print(
            f"  [cyan]{i:2}.[/] [white]{name:<32}[/] [dim]{cat:<12}[/] {diff:<14} Ext: {p.extension_count}"
        )

    console.print()
    console.print(f"[dim]Total: {len(presets)} presets[/]")


@app.command()
def search(query: str):
    """Search presets."""
    manager = get_preset_manager()
    results = manager.search_presets(query)

    if not results:
        console.print(f"[yellow]No presets found matching '{query}'[/]")
        return

    console.print(f"\n[bold cyan]Search Results for '{query}'[/]")
    console.print(f"[dim]Found {len(results)} result(s)[/]\n")

    for i, p in enumerate(results, 1):
        diff_color = (
            "[green]"
            if p.difficulty == "beginner"
            else "[yellow]"
            if p.difficulty == "intermediate"
            else "[red]"
        )
        console.print(f"[yellow]{i}.[/] [white]{p.name}[/] [dim]({p.id})[/]")
        console.print(f"   {p.description[:65]}...")
        console.print(
            f"   [dim]Category:[/] {p.category.title()} | [dim]Difficulty:[/] {diff_color}{p.difficulty.title()}[/] | [dim]Extensions:[/] {p.extension_count}"
        )
        console.print()


@app.command()
def browse(preset_id: str = typer.Option(None, "--id", "-i", help="Preset ID to browse")):
    """Browse presets or view a specific preset."""
    manager = get_preset_manager()

    if preset_id:
        preset = manager.get_preset(preset_id)
        if preset:
            state = MenuState()
            state._show_preset_detail(preset)
        else:
            console.print(f"[red]Preset '{preset_id}' not found[/]")
    else:
        _call_list_presets()


@app.command()
def install(preset_id: str, extensions_only: bool = False):
    """Install a preset."""
    state = MenuState()
    preset = state.preset_manager.get_preset(preset_id)

    if not preset:
        console.print(f"[red]Preset '{preset_id}' not found[/]")
        raise typer.Exit(1)

    state._install_preset_with_confirmation(preset)


@app.command()
def quiz():
    """Run the recommendation quiz."""
    state = MenuState()
    state.handle_quiz()


@app.command()
def update():
    """Check for updates."""
    state = MenuState()
    state.handle_update()


if __name__ == "__main__":
    app()
