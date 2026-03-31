# Python Professional Preset

## Who is this for?
You're a working Python developer. You write production code, run tests, and care about code quality. You want VS Code to catch bugs early and help you write clean, maintainable code.

## What this solves
- Runtime errors that should have been caught? Type checking now.
- Forgetting to format code? Auto-formats on save.
- Not sure what a function returns? Inlay hints show types.
- Tests scattered everywhere? Test Explorer shows them all.

## What your VS Code will feel like
One Dark Pro theme, professional and focused. Deep Python analysis with Pylance. Inlay hints showing types. Testing panel always accessible. Debugging just works.

## Extensions

| Extension | Why It's Here |
|---|---|
| Python + Pylance | Industry-standard Python tooling |
| Black Formatter | PEP 8 compliant formatting |
| Pylint | Advanced linting |
| autoDocstring | Professional documentation |
| Python Test Explorer | Visual test runner |
| Debugpy | Python debugging |
| GitHub Copilot | AI code suggestions |
| Error Lens | Inline error display |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `python.analysis.typeCheckingMode` | full | Catch bugs early |
| `python.testing.pytestEnabled` | true | Modern Python testing |
| `editor.rulers` | [79, 88] | PEP 8 and Black limits |
| `python.analysis.inlayHints` | enabled | See types inline |
| `editor.stickyScroll` | enabled | Context while scrolling |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Format Document | `Ctrl+Shift+F` |
| Run All Tests | `Ctrl+Shift+T` |
| Start Debugger | `Ctrl+Alt+D` |
| Toggle Terminal | `` Ctrl+` `` |
| Block Comment | `Ctrl+Shift+/` |
| Copy Line Down | `Ctrl+Shift+D` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `pymain` | Main block |
| `pyclass` | Class with init and toString |
| `pytry` | Try/except/finally |
| `pytest` | Pytest function |
| `pydc` | Python dataclass |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset python-professional

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → python-professional.code-profile
```

## You're All Set
This preset is complete for professional Python development.
