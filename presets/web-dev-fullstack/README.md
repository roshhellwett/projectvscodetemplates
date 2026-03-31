# Web Dev - Fullstack Preset

## Who is this for?
You're a fullstack developer. You write React on the frontend, Node.js on the backend, and work with databases. You need everything configured to work together seamlessly.

## What this solves
- Frontend and backend tools conflicting? Everything configured together.
- Database queries scattered? SQLTools keeps them organized.
- Docker for local dev? Integrated.
- API testing a nightmare? Set up and ready.

## What your VS Code will feel like
GitHub Dark Default theme. Frontend and backend tools both ready. Database connections available. Docker containers visible. Terminal for both ends.

## Extensions

| Extension | Why It's Here |
|---|---|
| Prettier + ESLint | Frontend formatting |
| Prisma | Database ORM |
| SQLTools | Database management |
| Docker | Container management |
| Python + Pylance | Backend Python support |
| Azure Tools | Cloud deployment |
| Tailwind CSS | Styling |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `editor.tabSize` | 2 | Web standard |
| `prettier.semi` | true | Backend convention |
| `prettier.trailingComma` | es5 | Modern JavaScript |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Format Document | `Ctrl+Shift+F` |
| Toggle Terminal | `` Ctrl+` `` |
| Toggle Sidebar | `Ctrl+B` |
| Docker View | `Ctrl+Shift+D` |
| Block Comment | `Ctrl+Shift+/` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `exproute` | Express router |
| `expmw` | Express middleware |
| `mogs` | Mongoose schema |
| `async` | Async request handler |
| `rafce` | React component |
| `fetchapi` | Fetch wrapper |
| `dcserv` | Docker Compose service |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset web-dev-fullstack

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → web-dev-fullstack.code-profile
```

## You're All Set
This preset covers the full stack. You're ready for any web project.
