# Go Backend Preset

## Who is this for?
You write Go. Fast, compiled, concurrent backends. You want VS Code to feel like a proper Go IDE with formatting, linting, and testing all working together.

## What this solves
- gofmt vs gofmt fights? gofmt is the formatter.
- Forgetting to run tests? Test explorer shows them.
- Linting taking forever? golangci-lint configured.
- Debugging Go hard? Delve debugger integrated.

## What your VS Code will feel like
Monokai theme. Go language server running. Tests visible in explorer. Formatting just works. Imports organized automatically.

## Extensions

| Extension | Why It's Here |
|---|---|
| Go | Official Go extension |
| Go Dev Tools | Extended tooling |
| Test Explorer | Visual test runner |
| Prettier | Code formatting |
| EditorConfig | Consistent style |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `go.formatTool` | gofmt | Go standard formatter |
| `go.lintTool` | golangci-lint | Full linting |
| `go.testFlags` | -v -count=1 | Verbose, no cache |
| `go.inlayHints` | enabled | See types inline |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Build | `Ctrl+Shift+B` |
| Run Tests at Cursor | `Ctrl+Shift+T` |
| Debug View | `Ctrl+Shift+D` |
| Continue Debug | `F5` |
| Toggle Terminal | `` Ctrl+` `` |
| Block Comment | `Ctrl+Shift+/` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `gomain` | Main function |
| `gofn` | Function |
| `goerr` | Error handling |
| `gohandler` | HTTP handler |
| `gostruct` | Struct |
| `gointerface` | Interface |
| `gotest` | Test function |
| `goslice` | Slice with make |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset go-backend

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → go-backend.code-profile
```

## Next Step
When you're building full web applications, check out [Web Dev Fullstack](../web-dev-fullstack/) for frontend integration.
