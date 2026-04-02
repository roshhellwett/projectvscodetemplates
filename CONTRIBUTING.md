# Contributing to ProjectVSCode Presets

Thank you for your interest in contributing! This guide will help you submit new presets or improvements.

## How to Submit a New Preset

### Step 1: Create the Preset Folder

Create a new folder under `presets/` with your preset name:

```
presets/my-awesome-preset/
```

### Step 2: Create Required Files

Every preset MUST include these 5 files:

- [ ] `settings.json` - Editor configuration
- [ ] `extensions.json` - Recommended VS Code extensions
- [ ] `keybindings.json` - Custom keyboard shortcuts
- [ ] `my-awesome-preset.code-snippets` - Language/framework snippets
- [ ] `README.md` - Preset documentation

### Step 3: Update manifest.json

Add your preset to `presets/manifest.json` following this schema:

```json
{
  "id": "my-awesome-preset",
  "name": "My Awesome Preset",
  "category": "professional",
  "track": "backend",
  "difficulty": "intermediate",
  "description": "One sentence description of who this is for",
  "target_user": "Who should use this preset",
  "recommended_theme": "Theme name from VS Code Marketplace",
  "extension_count": 8,
  "tags": ["tag1", "tag2"],
  "connects_to": ["related-preset-id"]
}
```

## Settings Quality Rules

### Do's
- ✅ Every setting MUST have a reason for existing
- ✅ Font sizes between 13px and 18px
- ✅ Different themes per preset (don't repeat themes)
- ✅ Format on save enabled for most presets
- ✅ Test on Linux and Windows

### Don'ts
- ❌ Don't add unused settings
- ❌ Don't copy settings from other presets without customizing
- ❌ Don't exceed 12 extensions per preset
- ❌ Don't use themes not available on VS Code Marketplace
- ❌ Don't add comments in JSON files (VS Code doesn't support them)

## Extension Guidelines

### Rules
1. Maximum 12 extensions per preset
2. Include the EXACT publisher.extensionId format
3. Every extension must have a clear purpose
4. Consider performance impact

### Good Extensions
- Core language support (Pylance, rust-analyzer, etc.)
- Essential tooling (Prettier, ESLint)
- Quality of life (Auto Rename Tag)

### Avoid
- Redundant extensions (two formatters, two linters)
- Niche extensions with limited use
- Extensions that slow down VS Code startup

## Keybinding Guidelines

### Rules
1. Only add keybindings directly relevant to the preset
2. Don't override common VS Code shortcuts (Ctrl+S, Ctrl+C, etc.)
3. Test keybindings don't conflict with popular extensions
4. Document all custom keybindings in README

### Good Keybindings
- Run/build commands for the language
- Toggle terminal
- Quick actions specific to the workflow

### Avoid
- Overriding standard copy/paste
- Conflicts with Vim/Emacs extensions
- Too many keybindings (keep it under 10)

## Snippet Guidelines

### Rules
1. Prefix must be under 10 characters
2. Include a description
3. Snippets must solve REAL repetitive tasks
4. Use proper tab stops and placeholders

### Good Snippets
- Boilerplate templates (main functions, class structures)
- Common patterns (try/catch, async/await)
- Framework-specific shortcuts (React components)

## README Template

Use this structure for every preset README:

```markdown
# Preset Name

## Who is this for?
One paragraph directly addressing the target user.

## What this solves
Bullet points of pain points this preset addresses.

## What your VS Code will feel like
Describe the visual experience.

## Extensions
| Extension | Why It's Here |
|---|---|
| name | reason |

## Key Settings
| Setting | Value | Why |
|---|---|---|
| key | value | reason |

## Keyboard Shortcuts
| Action | Keys |
|---|---|
| action | keys |

## Code Snippets
| Prefix | What it does |
|---|---|
| prefix | description |

## Install
```bash
# commands
```

## Next Step
Upgrade path to related preset (if applicable).
```

## Pull Request Template

```markdown
## Summary
Brief description of changes

## Preset Name
my-new-preset

## Files Changed
- [ ] settings.json
- [ ] extensions.json
- [ ] keybindings.json
- [ ] my-new-preset.code-snippets
- [ ] README.md
- [ ] manifest.json

## Testing
- [ ] Tested on Linux
- [ ] Tested on Windows
- [ ] Extensions install correctly
- [ ] No conflicting keybindings

## Screenshots (optional)
Add before/after screenshots if applicable
```

## Reporting Issues

Found a bug in an existing preset? Please include:
1. Preset name
2. Operating system
3. VS Code version
4. Expected vs actual behavior
5. Steps to reproduce

---

© 2026 [Zenith Open Source Projects](https://zenithopensourceprojects.vercel.app/). All Rights Reserved. Zenith is a Open Source Project Idea's by @roshhellwett
