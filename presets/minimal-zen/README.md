# Minimal Zen Preset

## Who is this for?
You want to write. Code, prose, notes - it doesn't matter. You want VS Code to disappear and let you focus. No sidebars, no status bar, just you and your words.

## What this solves
- Distracted by file explorer? Hidden.
- Status bar stealing attention? Gone.
- Activity bar wasting space? Invisible.
- Scrolling feels jarring? Smooth, minimal scrollbars.

## What your VS Code will feel like
Quiet Light theme - soft, paper-like, restful. Almost nothing on screen except your text. Zen mode available with `Ctrl+K Z`. The most peaceful coding experience possible.

## Extensions

| Extension | Why It's Here |
|---|---|
| Error Lens | Inline errors without visual noise |
| Material Icon Theme | Subtle, clean icons |
| Markdown Preview Enhanced | Beautiful Markdown rendering |
| Markdown Extended | Better Markdown support |
| Code Spell Checker | Quiet spell checking |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `workbench.activityBar.location` | `hidden` | No activity bar |
| `workbench.statusBar.visible` | false | No status bar |
| `workbench.sideBar.visible` | false | No file explorer |
| `workbench.editor.showTabs` | none | Tab-free |
| `editor.lineNumbers` | off | Pure writing focus |
| `editor.renderLineHighlight` | none | No line highlighting |
| `zenMode.centerLayout` | true | Content stays centered |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Toggle Zen Mode | `Ctrl+K Z` |
| Markdown Preview | `Ctrl+Shift+V` |
| Toggle Terminal | `` Ctrl+` `` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `mdlink` | Markdown link |
| `mdimg` | Markdown image |
| `mdrow` | Markdown table row |
| `mdcode` | Markdown code block |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset minimal-zen

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → minimal-zen.code-profile
```

## Next Step
If you also stream or record content, check out [Streamer & Content Creator](../streamer-content-creator/) for larger fonts and theme switching.
