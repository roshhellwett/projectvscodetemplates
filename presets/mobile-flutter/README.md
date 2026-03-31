# Mobile (Flutter) Preset

## Who is this for?
You build mobile apps with Flutter and Dart. You want hot reload to be instant, debugging to work seamlessly, and your code to be formatted consistently.

## What this solves
- Hot reload feeling slow? Optimized settings.
- Can't find device info? Device selector ready.
- Code formatting inconsistent? Dartfmt configured.
- Widget IDs confusing? They're visible now.

## What your VS Code will feel like
Flutter theme. Dart analysis working. Hot reload and hot restart mapped. Debug panel accessible. Everything tuned for mobile development.

## Extensions

| Extension | Why It's Here |
|---|---|
| Flutter | Core Flutter support |
| Flutter Provider | State management snippets |
| Flutter Snippets | Common Flutter patterns |
| Dart | Dart language support |
| ESLint | Code quality |
| Prettier | Code formatting |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `dart.lineLength` | 120 | Flutter convention |
| `dart.insertArgumentPlaceholders` | true | Saves typing |
| `flutter.showWidgetIds` | true | See widget tree |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Launch Debugger | `F5` |
| Attach to App | `Ctrl+Shift+F5` |
| Hot Reload | `R` (when debugging) |
| Hot Restart | `Shift+R` (when debugging) |
| Toggle Terminal | `` Ctrl+` `` |
| Block Comment | `Ctrl+Shift+/` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `flstl` | Stateless widget |
| `flstf` | Stateful widget |
| `flmain` | Main entry point |
| `flfuture` | FutureBuilder |
| `dcon` | Constructor with fields |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset mobile-flutter

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → mobile-flutter.code-profile
```

## You're All Set
This preset is complete for Flutter development.
