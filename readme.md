![Repo Size](https://img.shields.io/github/repo-size/roshhellwett/projectvscodetemplates?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/roshhellwett/projectvscodetemplates?style=for-the-badge)
![Forks](https://img.shields.io/github/forks/roshhellwett/projectvscodetemplates?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/roshhellwett/projectvscodetemplates?style=for-the-badge)
![VS Code](https://img.shields.io/badge/VSCode-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)
![PyPI](https://img.shields.io/pypi/v/projectvscodetemplates?style=for-the-badge)

# PROJECT VSCODE TEMPLATES

Ready-made VS Code setups for students, developers, creators, and remote teams.

![SAMPLE](https://github.com/roshhellwett/projectvscodetemplates/blob/45a255158543af850adc24d55df143181502b7d4/Sample/sample.png)

## What You Get

- 15 curated presets for different workflows
- one-click Windows installer flow
- guided Linux CLI flow
- settings, extensions, keybindings, and snippets bundled per preset

## Install

### Via pip (cross-platform)

```bash
pip install projectvscodetemplates
projectvscodetemplates
```

### Windows

Choose the option that feels easiest:

- `EXE`: build or distribute the Windows installer package from [`windows/build-exe.ps1`](windows/build-exe.ps1)
- `PowerShell (.ps1)`: run [`windows/install.ps1`](windows/install.ps1)

```powershell
powershell -ExecutionPolicy Bypass -File .\windows\install.ps1 -Interactive
```

### Linux

Use the guided quiz or install a preset directly:

```bash
chmod +x ./linux/quiz.sh ./linux/install.sh
./linux/quiz.sh
```

```bash
./linux/install.sh --preset python-beginner
```

## Pick a Preset Fast

| If you are... | Start with... |
|---|---|
| learning Python | `python-beginner` |
| doing data work | `data-science` |
| building frontend apps | `web-dev-frontend` |
| shipping full-stack apps | `web-dev-fullstack` |
| practicing DSA and contests | `competitive-programming` |
| writing Java in college | `java-student` |
| doing DevOps or cloud work | `devops-cloud` |
| working over SSH | `remote-ssh-server` |
| want a clean calm setup | `minimal-zen` |

See the full list in [`PRESETS.md`](PRESETS.md).

## Project Layout

```text
presets/   preset files and manifest
windows/   Windows installer, EXE build helper, RC file
linux/     Linux installer and guided quiz
scripts/   compatibility wrappers for older links
```

## For Maintainers

- Windows resource metadata lives in [`windows/ProjectVsCodeTemplates.rc`](windows/ProjectVsCodeTemplates.rc)
- The installer reads preset data from [`presets/manifest.json`](presets/manifest.json)
- Legacy script paths still work through wrappers in [`scripts/`](scripts)

---

© 2026 [Zenith Open Source Projects](https://zenithopensourceprojects.vercel.app/). All Rights Reserved. Zenith is a Open Source Project Idea's by @roshhellwett
