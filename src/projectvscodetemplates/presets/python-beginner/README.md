# Python Beginner Preset

## Who is this for?
You just installed VS Code. You're writing your first Python scripts. Every time you make a mistake, VS Code gives you no hints. You're fixing indentation by eye. This preset is built for you.

## What this solves
- No more invisible indentation errors
- Auto-formats your code on every save
- Tells you exactly where and why your code is wrong
- Font size that doesn't strain your eyes

## What your VS Code will feel like
Dark background, warm orange/purple syntax colors, large readable font, errors highlighted inline in red, code auto-formats the moment you hit save. Clean. Calm.

## Extensions

| Extension | Why It's Here |
|---|---|
| Python (Pylance) | Deep understanding of your Python code |
| Black Formatter | Auto-formats on save |
| Error Lens | Shows errors inline, not just underlined |
| autoDocstring | Generates docstrings automatically |
| Code Runner | Run Python with Ctrl+Alt+N |
| Material Icon Theme | Pretty file icons |
| Code Spell Checker | Catches typos in your code |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `editor.fontSize` | 15 | Large enough to read comfortably |
| `editor.tabSize` | 4 | Python convention |
| `editor.wordWrap` | on | No horizontal scrolling |
| `python.analysis.typeCheckingMode` | basic | Catches bugs without being annoying |
| `editor.formatOnSave` | true | Always formatted code |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Run Python | `Ctrl+Alt+N` |
| Toggle Terminal | `` Ctrl+` `` |
| Format Document | `Ctrl+Shift+F` |
| Block Comment | `Ctrl+Shift+/` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `pymain` | Creates `if __name__ == "__main__":` block |
| `pyclass` | Full class with `__init__` and `__str__` |
| `pyread` | Common input patterns |
| `pydebug` | Debug print with variable name |
| `pylist` | List comprehension template |
| `pytry` | Try/except/finally block |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset python-beginner

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → python-beginner.code-profile
```

## Next Step
When you're ready, upgrade to [Python Professional](../python-professional/) for production-ready Python workflows with testing and type checking.
