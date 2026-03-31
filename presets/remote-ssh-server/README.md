# Remote SSH Server Preset

## Who is this for?
You connect to remote servers via SSH and do your work there. Maybe it's a production server, a GPU machine for ML, or a dev environment in the cloud. You want VS Code to feel native even when remote.

## What this solves
- SSH connections dropping? Reconnection configured.
- Extensions not loading remotely? Extension sync ready.
- Terminal feeling clunky? JetBrains Mono, optimized.
- Can't find files easily? Recent files accessible.

## What your VS Code will feel like
Solarized Dark theme. Terminal is home. SSH connections quick. Remote extensions load automatically. Everything feels local even when it's not.

## Extensions

| Extension | Why It's Here |
|---|---|
| Remote SSH | Core SSH support |
| Remote SSH Edit | Edit SSH config |
| Remote Extensions | Remote extension pack |
| YAML | Config file editing |
| EditorConfig | Consistent formatting |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `remote.SSH.showLoginTerminal` | true | See login process |
| `remote.restoreExtensions` | true | Restore extensions |
| `terminal.integrated.cursorStyle` | block | Terminal native cursor |
| `files.autoSave` | onFocusChange | Auto-save remote files |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Command Palette | `Ctrl+Shift+P` or `F1` |
| Open Recent | `Ctrl+K Ctrl+R` |
| New Window | `Ctrl+Shift+N` |
| Toggle Terminal | `` Ctrl+` `` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `sshhost` | SSH config entry |
| `fn` | Bash function |
| `tmux` | TMUX session |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset remote-ssh-server

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → remote-ssh-server.code-profile
```

## Next Step
When you're also managing containers and cloud infrastructure, check out [DevOps & Cloud](../devops-cloud/) for Docker and Kubernetes support.
