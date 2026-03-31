# Streamer & Content Creator Preset

## Who is this for?
You code on camera. YouTube tutorials, Twitch streams, conference talks. You need VS Code to look beautiful on screen, with high contrast, large fonts, and quick theme switching.

## What this solves
- Font too small for viewers to read? Now it's 17px.
- Same theme boring on camera? Switch instantly with Peacock.
- Need to highlight specific code during recording? Line highlighting on.
- Viewers can't see file structure? Material icons everywhere.

## What your VS Code will feel like
One Dark Pro with Material icons. Large, readable fonts with ligatures. Quick theme switching with `Ctrl+Shift+1/2/3` for different languages. Todo tree for keeping track of topics.

## Extensions

| Extension | Why It's Here |
|---|---|
| Prettier | Beautiful code formatting |
| ESLint | Error checking |
| Peacock | One-click theme switching for streams |
| Material Icon Theme | Beautiful file icons |
| Error Lens | Inline errors |
| Auto Rename Tag | Save time while streaming |
| Live Server | See changes instantly |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `editor.fontSize` | 17 | Visible on camera |
| `editor.lineHeight` | 1.8 | Comfortable spacing |
| `editor.renderLineHighlight` | all | Current line stands out |
| `peacock.favoriteColors` | 5 presets | Quick theme switching |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Peacock: Angular Theme | `Ctrl+Shift+1` |
| Peacock: React Theme | `Ctrl+Shift+2` |
| Peacock: Vue Theme | `Ctrl+Shift+3` |
| Toggle Zen Mode | `Ctrl+K Z` |
| Toggle Terminal | `` Ctrl+` `` |
| Command Palette | `Ctrl+Shift+P` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `rafce` | React functional component |
| `clog` | Labeled console.log |
| `fetchapi` | Fetch with error handling |
| `usest` | useState hook |
| `todo` | TODO comment |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset streamer-content-creator

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → streamer-content-creator.code-profile
```

## You're All Set
This preset is designed for content creation. No further upgrades needed - you've got everything for streaming!
