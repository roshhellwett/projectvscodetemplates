# Java Student Preset

## Who is this for?
You're a computer science student taking a Java course. You need VS Code to understand your assignments, run your code, and help you learn Java the right way.

## What this solves
- Don't know how to structure a Java project? Maven/Gradle support helps.
- Can't find your errors? Inline error highlighting.
- Forgot to write tests? JUnit is integrated.
- Need to run just one class? Debug configuration ready.

## What your VS Code will feel like
Dracula theme - purple and easy on the eyes. Java extensions loaded. Run/Debug controls visible. Spring Boot dashboard available for web projects.

## Extensions

| Extension | Why It's Here |
|---|---|
| Language Support for Java | Core Java IntelliSense |
| Debugger for Java | Step-through debugging |
| Test Runner for Java | JUnit integration |
| Maven for Java | Build tool support |
| Spring Boot Tools | Spring framework support |
| Java Dependency Viewer | See project structure |

## Key Settings

| Setting | Value | Why |
|---|---|---|
| `editor.tabSize` | 4 | Java convention |
| `java.import.maven.enabled` | true | Maven projects work |
| `java.imports.gradle.enabled` | true | Gradle projects work |
| `java.autobuild.enabled` | true | Auto-compile |

## Keyboard Shortcuts

| Action | Keys |
|---|---|
| Run Main Class | `Shift+F10` |
| Debug Main Class | `Ctrl+Shift+F5` |
| Open Debug View | `Ctrl+Shift+D` |
| Toggle Terminal | `` Ctrl+` `` |
| Run Tests | `Ctrl+Shift+T` |

## Code Snippets

| Prefix | What it does |
|---|---|
| `jmain` | Main method |
| `jclass` | Class with constructor and toString |
| `jscan` | Scanner for input |
| `jtry` | Try-catch block |
| `jtest` | JUnit test |
| `jarrlist` | ArrayList declaration |
| `jhmap` | HashMap declaration |

## Install

```bash
# One-liner
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectvscodetemplates/main/scripts/install.sh) --preset java-student

# Manual
cp settings.json ~/.config/Code/User/settings.json
cp extensions.json ~/.config/Code/User/extensions.json
cp keybindings.json ~/.config/Code/User/keybindings.json

# Profile import
# VS Code → Profiles → Import → java-student.code-profile
```

## Next Step
When you're ready for data structures and algorithms, check out [Competitive Programming](../competitive-programming/) for C++/Java contest preparation.
