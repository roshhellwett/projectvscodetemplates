# Data Science Preset

## Who is this for?
You work with pandas, numpy, matplotlib, and Jupyter notebooks. You explore data, train models, and visualize results. You need VS Code to feel like a proper data IDE.

## What this solves
- Switching between notebook and script? Seamless.
- Can't see your notebook cells clearly? Line numbers and toolbar.
- Matplotlib plots looking cramped? Fixed dimensions set up.
- Need to restart kernel often? Now it asks first.

## What your VS Code will feel like
GitHub Dark Dimmed theme - easy on the eyes during long analysis sessions. Jupyter integration built in. Cells execute with Shift+Enter. Plots display inline.

## Extensions

| Extension | Why It's Here |
|---|---|
| Python | Core Python support |
| Pylance | Deep code understanding |
| Jupyter | Notebook support |
| Jupyter Cell Tags | Organize notebook cells |
| Black Formatter | Auto-format on save |
| Copilot | AI code suggestions |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `notebook.lineNumbers` | on | See cell positions |
| `jupyter.askForKernelRestart` | false | Don't ask, just restart |
| `editor.rulers` | 88 | PEP 8 line length |
| `editor.wordWrap` | on | Long lines wrap |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Run Cell | `Shift+Enter` |
| Run Cell & Select Below | `Ctrl+Enter` |
| Toggle Terminal | `` Ctrl+` `` |
| Format Document | `Ctrl+Shift+F` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `mplsetup` | Matplotlib with seaborn styling |
| `pdread` | Read CSV with initial exploration |
| `npimp` | NumPy import |
| `ttsplit` | Train test split |
| `grpb` | Pandas group by with aggregation |
| `mplsub` | Matplotlib subplots grid |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset data-science

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → data-science.code-profile
```

## Next Step
When you're building production ML pipelines, upgrade to [Python Professional](../python-professional/) for testing and advanced type checking.
