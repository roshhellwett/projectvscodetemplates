# ProjectVSCode Presets

```
╔══════════════════════════════════════════════════════════════╗
║                                                               ║
║              🖥️  ProjectVSCode Presets                       ║
║                                                               ║
║         Your perfect VS Code setup in 60 seconds              ║
║                                                               ║
╚══════════════════════════════════════════════════════════════╝
```

A curated collection of VS Code configuration presets for every type of developer. Whether you're a student learning Python, a competitive programmer, or a professional fullstack developer - we have a preset for you.

## Quick Install

```bash
# Linux / Mac
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset <preset-name>

# Windows (PowerShell)
.\install.ps1 -Preset <preset-name>
```

Or use the interactive quiz:

```bash
# Answer 4 questions, get your perfect setup
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/quiz.sh)
```

## Don't Know Which Preset?

Run the quiz:

```bash
bash scripts/quiz.sh
```

Answer 4 quick questions about:
1. What you code
2. Your experience level
3. How you use VS Code
4. Your operating system

Get your perfect preset recommendation instantly.

## All Presets

| Preset | For | Difficulty |
|--------|-----|------------|
| [python-beginner](presets/python-beginner/) | Students learning Python | ⭐ |
| [python-professional](presets/python-professional/) | Production Python developers | ⭐⭐ |
| [competitive-programming](presets/competitive-programming/) | Contest coders, DSA learners | ⭐⭐ |
| [java-student](presets/java-student/) | University Java courses | ⭐ |
| [web-dev-frontend](presets/web-dev-frontend/) | React, Vue, Tailwind developers | ⭐ |
| [web-dev-fullstack](presets/web-dev-fullstack/) | Fullstack with Node.js, DBs | ⭐⭐ |
| [c-cpp-systems](presets/c-cpp-systems/) | Systems programmers | ⭐⭐ |
| [data-science](presets/data-science/) | Data scientists, ML engineers | ⭐⭐ |
| [devops-cloud](presets/devops-cloud/) | DevOps, Cloud, Infra | ⭐⭐ |
| [mobile-flutter](presets/mobile-flutter/) | Flutter developers | ⭐⭐ |
| [rust-systems](presets/rust-systems/) | Rust developers | ⭐⭐⭐ |
| [go-backend](presets/go-backend/) | Go developers | ⭐⭐ |
| [minimal-zen](presets/minimal-zen/) | Writers, minimalist coders | ⭐ |
| [streamer-content-creator](presets/streamer-content-creator/) | YouTubers, streamers | ⭐ |
| [remote-ssh-server](presets/remote-ssh-server/) | Remote server workers | ⭐⭐ |

## How It Works

```
[Pick a preset] → [Run installer] → [Open VS Code]
      ↓                ↓                  ↓
   quiz.sh        install.sh        Profit! 🎉
   or web          or web
```

Each preset includes:
- **settings.json** - Editor configuration
- **extensions.json** - Recommended VS Code extensions
- **keybindings.json** - Custom keyboard shortcuts
- **code-snippets** - Productivity snippets for your language

## Manual Installation

If you prefer to install manually:

1. Copy `settings.json` to `~/.config/Code/User/settings.json` (Linux/Mac) or `%APPDATA%\Code\User\settings.json` (Windows)
2. Copy `extensions.json` to the same directory
3. Copy `keybindings.json` to the same directory
4. VS Code will prompt you to install extensions from `extensions.json`

## Web Configurator

Want to see all presets visually? Open [web/index.html](web/index.html) in your browser - no server required.

## Contributing

Found a bug? Want to add a new preset? Check out [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License - use it however you want.
