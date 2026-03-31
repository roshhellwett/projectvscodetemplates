#!/usr/bin/env bash

set -euo pipefail

VERSION="1.0.0"
REPO_SLUG="zenithopensourceprojects/projectvscodetemplates"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST_PATH="$PROJECT_ROOT/presets/manifest.json"

cyan='\033[0;36m'
green='\033[0;32m'
yellow='\033[1;33m'
red='\033[0;31m'
reset='\033[0m'

print_section() {
    printf '\n%s== %s ==%s\n' "$cyan" "$1" "$reset"
}

print_ok() {
    printf '%s[OK]%s %s\n' "$green" "$reset" "$1"
}

print_warn() {
    printf '%s[!]%s %s\n' "$yellow" "$reset" "$1"
}

print_error() {
    printf '%s[X]%s %s\n' "$red" "$reset" "$1" >&2
}

show_help() {
    cat <<EOF
Project VsCode Templates - Linux Installer

Usage:
  ./install.sh --preset python-beginner
  ./install.sh --list

Options:
  --preset <id>   Install a preset directly
  --list          Show all preset ids
  --version       Show installer version
  --help          Show this help
EOF
}

show_version() {
    echo "Project VsCode Templates Linux Installer v$VERSION"
}

manifest_python() {
    python3 - "$MANIFEST_PATH" "$@" <<'PY'
import json
import sys

manifest_path = sys.argv[1]
mode = sys.argv[2]

with open(manifest_path, "r", encoding="utf-8") as handle:
    data = json.load(handle)

presets = data["presets"]

if mode == "list":
    for preset in presets:
        print(f"{preset['id']}\t{preset['name']}\t{preset['category']}\t{preset['difficulty']}\t{preset['description']}")
elif mode == "exists":
    preset_id = sys.argv[3]
    print("yes" if any(p["id"] == preset_id for p in presets) else "no")
else:
    raise SystemExit(f"Unsupported mode: {mode}")
PY
}

show_presets() {
    print_section "Available Presets"
    while IFS=$'\t' read -r preset_id preset_name preset_category preset_difficulty preset_description; do
        printf '%-28s %s\n' "$preset_id" "$preset_name"
        printf '  %s | %s | %s\n\n' "$preset_category" "$preset_difficulty" "$preset_description"
    done < <(manifest_python list)
}

require_manifest() {
    if [[ ! -f "$MANIFEST_PATH" ]]; then
        print_error "Local manifest not found at $MANIFEST_PATH."
        exit 1
    fi

    if ! command -v python3 >/dev/null 2>&1; then
        print_error "python3 is required to read presets/manifest.json."
        exit 1
    fi
}

detect_config_dir() {
    if [[ "${XDG_CONFIG_HOME:-}" != "" ]]; then
        printf '%s/Code/User\n' "$XDG_CONFIG_HOME"
    else
        printf '%s/.config/Code/User\n' "$HOME"
    fi
}

backup_file() {
    local file="$1"
    if [[ -f "$file" ]]; then
        local stamp
        stamp="$(date +%Y-%m-%d-%H%M%S)"
        cp "$file" "$file.backup.$stamp"
        print_warn "Backed up $file to $file.backup.$stamp"
    fi
}

copy_required_file() {
    local preset_dir="$1"
    local source_name="$2"
    local destination="$3"

    if [[ ! -f "$preset_dir/$source_name" ]]; then
        print_error "Missing required file: $preset_dir/$source_name"
        exit 1
    fi

    cp "$preset_dir/$source_name" "$destination"
    print_ok "$source_name installed"
}

install_extensions() {
    local extensions_file="$1"

    if ! command -v code >/dev/null 2>&1; then
        print_warn "VS Code CLI ('code') was not found. Open VS Code later and install the recommended extensions from extensions.json."
        return
    fi

    print_section "Installing Recommended Extensions"
    python3 - "$extensions_file" <<'PY' | while IFS= read -r extension; do
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as handle:
    data = json.load(handle)

for item in data.get("recommendations", []):
    print(item)
PY
        [[ -z "$extension" ]] && continue
        printf '%sInstalling %s...%s\n' "$yellow" "$extension" "$reset"
        if code --install-extension "$extension" --force >/dev/null 2>&1; then
            print_ok "$extension installed"
        else
            print_warn "$extension could not be installed automatically."
        fi
    done
}

install_preset() {
    local preset_id="$1"
    local exists
    local preset_dir="$PROJECT_ROOT/presets/$preset_id"
    local config_dir
    local snippets_dir
    local snippet_file

    require_manifest
    exists="$(manifest_python exists "$preset_id")"
    if [[ "$exists" != "yes" ]]; then
        print_error "Preset '$preset_id' is not listed in presets/manifest.json."
        exit 1
    fi

    if [[ ! -d "$preset_dir" ]]; then
        print_error "Preset folder not found: $preset_dir"
        exit 1
    fi

    config_dir="$(detect_config_dir)"
    snippets_dir="$config_dir/snippets"
    snippet_file="$preset_id.code-snippets"

    print_section "Installing $preset_id"
    printf 'Target folder: %s\n' "$config_dir"

    mkdir -p "$config_dir" "$snippets_dir"

    backup_file "$config_dir/settings.json"
    copy_required_file "$preset_dir" "settings.json" "$config_dir/settings.json"

    backup_file "$config_dir/extensions.json"
    copy_required_file "$preset_dir" "extensions.json" "$config_dir/extensions.json"

    backup_file "$config_dir/keybindings.json"
    copy_required_file "$preset_dir" "keybindings.json" "$config_dir/keybindings.json"

    if [[ -f "$preset_dir/$snippet_file" ]]; then
        cp "$preset_dir/$snippet_file" "$snippets_dir/$snippet_file"
        print_ok "$snippet_file installed"
    else
        print_warn "No snippets file was found for this preset."
    fi

    install_extensions "$config_dir/extensions.json"

    print_section "Finished"
    print_ok "Preset '$preset_id' is ready."
    echo "Restart VS Code if it was already open."
}

PRESET=""
LIST=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --preset)
            PRESET="${2:-}"
            shift 2
            ;;
        --list)
            LIST=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        --version|-v)
            show_version
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

if [[ "$LIST" == true ]]; then
    require_manifest
    show_presets
elif [[ -n "$PRESET" ]]; then
    install_preset "$PRESET"
else
    show_help
    exit 1
fi
