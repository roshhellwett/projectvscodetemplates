# Web Dev - Frontend Preset

## Who is this for?
You're building websites with React, Vue, or vanilla JavaScript. You want your code to look beautiful, format automatically, and just work when you hit save.

## What this solves
- Prettier and ESLint fighting each other? Now they work together.
- Writing HTML boilerplate by hand? Emmet does it for you.
- Tag mismatches? Auto Rename Tag fixes them.
- Can't remember file paths? Path Intellisense completes them.

## What your VS Code will feel like
One Dark Pro theme with Material icons. Your code auto-formats the moment you save. Tailwind classes get highlighted. JSX closes automatically. Everything just flows.

## Extensions

| Extension | Why It's Here |
|---|---|
| Prettier | Code formatter that just works |
| ESLint | Catches errors before you commit |
| Auto Rename Tag | Renames HTML/JSX tags automatically |
| Path Intellisense | Complete file paths as you type |
| Tailwind CSS IntelliSense | Tailwind class autocomplete |
| ES7+ Snippets | React/Redux snippets |
| Peacock | Quick theme switching for streams |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `editor.tabSize` | 2 | Web standard |
| `prettier.singleQuote` | true | Consistent with most projects |
| `prettier.semi` | false | No semicolons |
| `emmet.triggerExpansionOnTab` | true | Tab to expand Emmet |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Format Document | `Alt+Shift+F` |
| Toggle Terminal | `` Ctrl+` `` |
| Block Comment | `Ctrl+Shift+/` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `rafce` | React functional component with export |
| `usest` | useState hook |
| `useef` | useEffect with cleanup |
| `twcard` | Tailwind card template |
| `fetchapi` | Async fetch with error handling |
| `clog` | Labeled console.log |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset web-dev-frontend

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → web-dev-frontend.code-profile
```

## Next Step
When you're ready to add a backend, Node.js, or databases, upgrade to [Web Dev Fullstack](../web-dev-fullstack/).
