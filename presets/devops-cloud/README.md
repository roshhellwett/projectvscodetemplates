# DevOps & Cloud Preset

## Who is this for?
You work with Docker, Kubernetes, Terraform, and cloud providers. You need to manage containers, edit YAML flawlessly, and connect to remote environments.

## What this solves
- YAML validation a nightmare? Schemas enforce correctness.
- Docker commands taking forever? Integrated Docker extension.
- Kubernetes manifests hard to read? Syntax highlighting and validation.
- Remote server access complicated? SSH extension ready.

## What your VS Code will feel like
Solarized Dark theme. Docker, Kubernetes, and cloud tools visible. YAML editing is a pleasure. Terminal always available for CLI work.

## Extensions

| Extension | Why It's Here |
|---|---|
| Docker | Container management |
| Remote SSH | Work on remote servers |
| Azure Functions | Serverless deployment |
| Kubernetes | K8s manifest editing |
| Terraform | IaC support |
| YAML | Schema validation |
| EditorConfig | Consistent formatting |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `yaml.schemas` | k8s, terraform | Schema validation |
| `terminal.fontSize` | 13 | Comfortable terminal |
| `docker.dockerPath` | docker | Native Docker |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Command Palette | `Ctrl+Shift+P` |
| Toggle Terminal | `` Ctrl+` `` |
| Resize Terminal Up | `Ctrl+K Ctrl+=` |
| Resize Terminal Down | `Ctrl+K Ctrl+-` |
| Extensions | `Ctrl+Shift+X` |
| Explorer | `Ctrl+Shift+E` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `dockerfile` | Dockerfile template |
| `dcfile` | Docker Compose file |
| `k8sdeploy` | Kubernetes deployment |
| `k8ssvc` | Kubernetes service |
| `tfprov` | Terraform provider |
| `tfres` | Terraform resource |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset devops-cloud

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → devops-cloud.code-profile
```

## Next Step
If you primarily work on remote servers, check out [Remote SSH Server](../remote-ssh-server/) for optimized remote workflows.
