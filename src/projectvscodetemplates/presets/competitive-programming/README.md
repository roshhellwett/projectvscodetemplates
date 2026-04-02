# Competitive Programming Preset

## Who is this for?
You're a competitive programmer. Codeforces, LeetCode, AtCoder - you compete. Every second counts. You need your editor to get out of the way and let you code fast.

## What this solves
- Copy-paste boilerplate every contest? Not anymore.
- Can't see compilation errors? Now they're inline.
- Switching between files in a contest? Streamlined.
- Running code with test input? One key.

## What your VS Code will feel like
Tokyo Night Storm theme - dark, easy on the eyes during long contests. Clean editor, no distractions. Terminal always visible. Code runs with your test input instantly.

## Extensions

| Extension | Why It's Here |
|---|---|
| C/C++ Extension Pack | Full C++ IntelliSense and debugging |
| Code Runner | One-click run with input.txt |
| Error Lens | Inline compilation errors |
| Better Comments | Color-coded comments (TODO, BUG, etc.) |
| Tokyo Night Theme | Beautiful dark theme |
| Code Spell Checker | Catches typos in variable names |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `editor.fontSize` | 14 | Compact but readable |
| `code-runner.runInTerminal` | true | See output immediately |
| `code-runner.executorMap.cpp` | Custom with input.txt | Contest workflow |
| `files.autoSave` | onFocusChange | Never lose work |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Run Code | `Ctrl+Alt+R` |
| Toggle Terminal | `` Ctrl+` `` |
| Move Line Up/Down | `Alt+Up/Down` |
| Copy Line Down | `Ctrl+Shift+D` |
| Block Comment | `Ctrl+Shift+/` |
| Build Task | `Ctrl+Shift+B` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `cptemplate` | Complete contest template with includes, defines, main loop |
| `bsearch` | Binary search with customizable condition |
| `bfs` | BFS traversal with queue |
| `dfs` | DFS traversal with recursion |
| `dijkstra` | Shortest path algorithm |
| `seg` | Segment tree with query/update |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset competitive-programming

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → competitive-programming.code-profile
```

## Next Step
When you're doing systems programming or low-level work, check out [C/C++ Systems](../c-cpp-systems/) for CMake and debugging support.
