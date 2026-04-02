# C/C++ Systems Preset

## Who is this for?
You write low-level code. Operating systems, embedded systems, game engines, or high-performance applications. You need deep C/C++ support, CMake integration, and serious debugging.

## What this solves
- CMake projects not configuring? Auto-configure on open.
- Can't find memory leaks? LLDB integration helps.
- Compilation warnings everywhere? Error squiggles enabled.
- Makefiles need special handling? CMake Tools ready.

## What your VS Code will feel like
Monokai theme - classic and focused. C++20 by default. Build tasks configured. Debugger ready. Minimize visible for large codebases.

## Extensions

| Extension | Why It's Here |
|---|---|
| C/C++ Extension Pack | Complete C++ tooling |
| CMake Tools | CMake project support |
| CMake Language Support | Syntax highlighting |
| C/C++ Runner | Quick compilation |
| Code Spell Checker | Catches typos |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `C_Cpp.default.cppStandard` | c++20 | Latest features |
| `cmake.configureOnOpen` | true | Auto-configure CMake |
| `editor.rulers` | [80, 120] | Line length limits |
| `editor.tabSize` | 4 | C++ convention |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Build Task | `Ctrl+Shift+B` |
| Start Debugging | `F5` |
| Step Over | `F6` |
| Toggle Terminal | `` Ctrl+` `` |
| Debug View | `Ctrl+Shift+D` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `cmain` | C++ main template |
| `cclass` | Class with encapsulation |
| `cmake` | CMakeLists.txt |
| `mkrule` | Makefile rule |
| `raii` | RAII guard pattern |
| `gdbbp` | GDB commands |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset c-cpp-systems

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → c-cpp-systems.code-profile
```

## You're All Set
This preset is complete for systems programming.
