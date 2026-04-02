![Repo Size](https://img.shields.io/github/repo-size/roshhellwett/projectvscodetemplates?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/roshhellwett/projectvscodetemplates?style=for-the-badge)
![Forks](https://img.shields.io/github/forks/roshhellwett/projectvscodetemplates?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/roshhellwett/projectvscodetemplates?style=for-the-badge)
![VS Code](https://img.shields.io/badge/VSCode-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)
![PyPI](https://img.shields.io/pypi/v/projectvscodetemplates?style=for-the-badge)

# PROJECT VSCODE TEMPLATES

Ready-made VS Code setups for students, developers, creators, and remote teams.

![SAMPLE](https://github.com/roshhellwett/projectvscodetemplates/blob/45a255158543af850adc24d55df143181502b7d4/Sample/sample.png)

## What is this?

**VSCode Templates** is a tool that automatically sets up VS Code for you with the perfect extensions, settings, and shortcuts for your workflow. Instead of manually installing 20+ extensions and changing settings, just pick a preset and it all happens in seconds!

### Why use this?
- **No more searching** for "best VS Code extensions for Python"
- **One-click setup** - everything configured automatically
- **15 ready-made presets** for different types of work

---

## Quick Start (For Beginners)

### Step 1: Install Python
If you don't have Python, download it here: https://www.python.org/downloads/
(Check "Add Python to PATH" during installation)

### Step 2: Open Your Terminal/Command Prompt
- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **macOS**: Press `Cmd + Space`, type `terminal`, press Enter
- **Linux**: Press `Ctrl + Alt + T`

### Step 3: Install the Tool
Copy and paste this command:

```bash
pip install projectvscodetemplates
```

### Step 4: Run It!
After installing, just type:

```bash
projectvscodetemplates
```

That's it! The tool will ask you questions and set up VS Code for you.

---

## Installation Options

### Option 1: Install via pip (Recommended - works on Windows, macOS, Linux)

```bash
pip install projectvscodetemplates
projectvscodetemplates
```

Or run with Python directly:

```bash
python -m projectvscodetemplates
```

### Option 2: Windows PowerShell Installer

If you prefer Windows-specific installation:

```powershell
powershell -ExecutionPolicy Bypass -File .\windows\install.ps1 -Interactive
```

### Option 3: Linux/macOS Shell Script

```bash
chmod +x ./linux/quiz.sh
./linux/quiz.sh
```

Or install a specific preset:

```bash
./linux/install.sh --preset python-beginner
```

---

## How to Choose a Preset

| If you are... | Use this preset... | What it does |
|---|---|---|
| Just started learning Python | `python-beginner` | Basic extensions, simple settings |
| Doing data analysis or AI/ML | `data-science` | Jupyter, pandas, numpy support |
| Building websites (HTML/CSS/JS) | `web-dev-frontend` | Live Server, Prettier, Emmet |
| Building full web apps (frontend + backend) | `web-dev-fullstack` | Node.js, React, API tools |
| Doing coding competitions (DSA) | `competitive-programming` | Fast coding, competitive programming tools |
| Writing Java in school/college | `java-student` | Java extensions, project support |
| Working with DevOps/Cloud (AWS, Docker, etc.) | `devops-cloud` | Docker, Kubernetes, cloud tools |
| Connecting to remote servers via SSH | `remote-ssh-server` | Remote development setup |
| Want a clean, distraction-free setup | `minimal-zen` | Minimal UI, focus mode |
| Creating content/streams | `streamer-content-creator` | Screen recording, streaming tools |
| Learning C/C++ programming | `c-cpp-systems` | C/C++ compiler support |
| Learning Rust | `rust-systems` | Rust language support |
| Building mobile Flutter apps | `mobile-flutter` | Flutter and Dart support |
| Building Go backend apps | `go-backend` | Go language support |

**Don't know which one?** Just run the tool and answer the questions - it will recommend the best preset for you!

---

## Step-by-Step Example: Installing a Python Preset

Let's say you want to set up VS Code for Python:

1. Open your terminal
2. Type: `pip install projectvscodetemplates`
3. Wait for it to install (shows "Successfully installed")
4. Type: `projectvscodetemplates`
5. The tool will show you a list of presets
6. Type the number for `python-beginner` or `python-professional`
7. Press Enter and let it install everything

Done! Your VS Code is now ready for Python programming!

---

## What Happens During Installation?

When you install a preset, the tool:

1. **Installs extensions** - VS Code extensions for your chosen workflow
2. **Configures settings** - Editor settings, formatting, themes
3. **Sets up keybindings** - Keyboard shortcuts for faster work
4. **Creates snippets** - Ready-made code templates

You can watch the installation progress in your terminal.

---

## Troubleshooting

### "pip is not recognized" error
- Make sure Python is installed
- Make sure Python is in your PATH (during installation, check "Add Python to PATH")

### "command not found" error
- Try restarting your terminal
- On macOS/Linux, you may need to add `~/.local/bin` to your PATH

### VS Code not opening
- Make sure VS Code is installed: https://code.visualstudio.com/
- Install it first, then run this tool again

---

## For Developers

### Project Layout

```
projectvscodetemplates/
├── src/projectvscodetemplates/   # Main source code
│   ├── presets/                  # Preset configurations
│   ├── cli.py                    # Command-line interface
│   └── ...
├── windows/                      # Windows installer scripts
├── linux/                        # Linux installer scripts
└── tests/                        # Test files
```

### Running Tests

```bash
pytest
```

### Building for PyPI

```bash
python -m build
```

---

## Need Help?

- **GitHub Issues**: https://github.com/zenithopensourceprojects/projectvscodetemplates/issues
- **Documentation**: https://github.com/zenithopensourceprojects/projectvscodetemplates#readme

---

© 2026 [Zenith Open Source Projects](https://zenithopensourceprojects.vercel.app/). All Rights Reserved. Zenith is an Open Source Project Idea by @roshhellwett