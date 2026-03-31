# Presets Master List

Complete comparison and upgrade paths for all ProjectVSCode Presets.

## Quick Comparison Table

| Preset | For | Font Size | Theme | Extensions | Difficulty |
|--------|-----|-----------|-------|------------|------------|
| python-beginner | Students learning Python | 15px | One Dark Pro | 9 | ⭐ |
| python-professional | Production Python devs | 14px | One Dark Pro | 12 | ⭐⭐ |
| competitive-programming | Contest coders | 14px | Tokyo Night | 8 | ⭐⭐ |
| java-student | University Java | 14px | Dracula | 8 | ⭐ |
| web-dev-frontend | React, Vue, Tailwind | 14px | One Dark Pro | 11 | ⭐ |
| web-dev-fullstack | Fullstack Node.js | 14px | GitHub Dark | 12 | ⭐⭐ |
| c-cpp-systems | Systems programmers | 13px | Monokai | 9 | ⭐⭐ |
| data-science | Data scientists | 14px | GitHub Dark Dimmed | 10 | ⭐⭐ |
| devops-cloud | DevOps, Cloud | 13px | Solarized Dark | 12 | ⭐⭐ |
| mobile-flutter | Flutter developers | 14px | Flutter | 8 | ⭐⭐ |
| rust-systems | Rust developers | 14px | One Dark Pro | 7 | ⭐⭐⭐ |
| go-backend | Go developers | 14px | Monokai | 7 | ⭐⭐ |
| minimal-zen | Writers, minimalists | 15px | Quiet Light | 5 | ⭐ |
| streamer-content-creator | YouTubers, streamers | 17px | One Dark Pro | 10 | ⭐ |
| remote-ssh-server | Remote workers | 13px | Solarized Dark | 7 | ⭐⭐ |

## Preset Upgrade Paths

Not sure which preset to pick? Here's how they connect:

```
python-beginner ────────────────────────────────→ python-professional
                                                        ↓
java-student ──→ competitive-programming ──→ c-cpp-systems
                                                        ↓
web-dev-frontend ─────────────────────────────→ web-dev-fullstack
                                                        ↓
rust-systems ─────────────────────────────────────→ c-cpp-systems
                                                        ↓
go-backend ─────────────────────────────────────→ web-dev-fullstack
                                                        ↓
data-science ──────────────────────────────────→ python-professional
                                                        ↓
devops-cloud ─────────────────────────────────→ remote-ssh-server
                                                        ↓
minimal-zen ────────────────────────────────────→ streamer-content-creator
```

### Standalone Presets (No Upgrade Path)
These presets are complete for their use cases:
- mobile-flutter
- java-student
- competitive-programming
- streamer-content-creator

## By Use Case

### "I'm a university student"
→ [python-beginner](presets/python-beginner/) or [competitive-programming](presets/competitive-programming/)
- python-beginner if you're just learning
- competitive-programming if you're preparing for placements

### "I'm learning web development"
→ [web-dev-frontend](presets/web-dev-frontend/)
- React, Vue, Tailwind all covered
- Prettier + ESLint ready to go

### "I'm freelancing"
→ [web-dev-fullstack](presets/web-dev-fullstack/)
- Frontend + backend + database
- Docker for local dev environments

### "I'm job hunting"
→ [python-professional](presets/python-professional/) or [go-backend](presets/go-backend/)
- Production-ready configurations
- Testing frameworks included

### "I code on stream"
→ [streamer-content-creator](presets/streamer-content-creator/)
- Large fonts visible on camera
- Peacock for quick theme switching

### "I want peace while I code"
→ [minimal-zen](presets/minimal-zen/)
- Hidden sidebars and status bar
- Zen mode built in

### "I work on remote servers"
→ [remote-ssh-server](presets/remote-ssh-server/)
- SSH extensions ready
- Terminal optimized

### "I do DevOps work"
→ [devops-cloud](presets/devops-cloud/)
- Docker, Kubernetes, Terraform
- Cloud CLI tools configured

## Extension Count by Preset

| Category | Preset | Count |
|----------|--------|-------|
| Minimal | minimal-zen | 5 |
| Minimal | remote-ssh-server | 7 |
| Light | rust-systems | 7 |
| Light | competitive-programming | 8 |
| Light | java-student | 8 |
| Light | go-backend | 7 |
| Light | mobile-flutter | 8 |
| Medium | streamer-content-creator | 10 |
| Medium | c-cpp-systems | 9 |
| Medium | python-beginner | 9 |
| Medium | data-science | 10 |
| Medium | web-dev-frontend | 11 |
| Medium | devops-cloud | 12 |
| Heavy | python-professional | 12 |
| Heavy | web-dev-fullstack | 12 |

## Theme Colors

| Preset | Primary Color |
|--------|---------------|
| python-beginner | #519aba (Blue) |
| python-professional | #519aba (Blue) |
| competitive-programming | #7aa2f7 (Purple-Blue) |
| java-student | #bd5794 (Purple) |
| web-dev-frontend | #519aba (Blue) |
| web-dev-fullstack | #4d4d4d (Gray) |
| c-cpp-systems | #F05138 (Red) |
| data-science | #2188ff (Blue) |
| devops-cloud | #65737e (Slate) |
| mobile-flutter | #02569B (Flutter Blue) |
| rust-systems | #dea584 (Rust Orange) |
| go-backend | #00ADD8 (Go Blue) |
| minimal-zen | #eeeeee (Light) |
| streamer-content-creator | #519aba (Blue) |
| remote-ssh-server | #65737e (Slate) |

## Feature Matrix

| Preset | Format on Save | Auto Save | Minimap | Custom Theme |
|--------|---------------|-----------|---------|--------------|
| python-beginner | ✓ | ✓ | ✗ | ✓ |
| python-professional | ✓ | ✓ | ✗ | ✓ |
| competitive-programming | ✓ | ✓ | ✗ | ✓ |
| java-student | ✓ | ✓ | - | ✓ |
| web-dev-frontend | ✓ | ✓ | - | ✓ |
| web-dev-fullstack | ✓ | ✓ | - | ✓ |
| c-cpp-systems | ✓ | ✓ | ✓ | ✓ |
| data-science | ✓ | ✓ | ✓ | ✓ |
| devops-cloud | ✓ | ✓ | ✓ | ✓ |
| mobile-flutter | ✓ | ✓ | - | ✓ |
| rust-systems | ✓ | ✓ | ✗ | ✓ |
| go-backend | ✓ | ✓ | ✗ | ✓ |
| minimal-zen | ✓ | ✓ | ✗ | ✓ |
| streamer-content-creator | ✓ | ✓ | ✗ | ✓ |
| remote-ssh-server | ✗ | ✓ | ✗ | ✓ |
