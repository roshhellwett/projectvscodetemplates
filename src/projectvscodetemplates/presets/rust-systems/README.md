# Rust Systems Preset

## Who is this for?
You write Rust. Memory safety matters to you. You want VS Code to understand ownership, lifetimes, and all the Rust-specific tooling that makes the language great.

## What this solves
- Fighting the borrow checker? rust-analyzer shows you exactly why.
- Forgetting to run clippy? It runs on save now.
- Proc macros not working? Enabled.
- Finding the right import path? Crate prefix configured.

## What your VS Code will feel like
One Dark Pro theme. rust-analyzer analyzing your code in real-time. Clippy linting on save. Cargo commands accessible. Everything Rust-aware.

## Extensions

| Extension | Why It's Here |
|---|---|
| rust-analyzer | The best Rust IDE support |
| CodeLLDB | Native Rust debugging |
| Better TOML | TOML file support |
| Crates | Dependency version checker |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `rust-analyzer.checkOnSave.command` | clippy | Lint on save |
| `rust-analyzer.procMacro.enable` | true | Proc macro support |
| `rust-analyzer.imports.prefix` | crate | Consistent imports |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Cargo Build | `Ctrl+Shift+B` |
| Cargo Test | `Ctrl+Shift+T` |
| Cargo Run | `Ctrl+Shift+R` |
| Start Debugger | `F5` |
| Toggle Terminal | `` Ctrl+` `` |
| Block Comment | `Ctrl+Shift+/` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `rsmain` | Main function |
| `rsfn` | Function |
| `rsstruct` | Struct |
| `rsimpl` | Impl block |
| `rsmatch` | Match expression |
| `rsresult` | Result return type |
| `rstest` | Unit test |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset rust-systems

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → rust-systems.code-profile
```

## Next Step
When you need C interoperability or systems work, check out [C/C++ Systems](../c-cpp-systems/) for CMake and debugging.
