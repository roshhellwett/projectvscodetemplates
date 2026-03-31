#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
NC='\033[0m'

VERSION="1.0.0"
GITHUB_REPO="zenithopensourceprojects/projectvscodetemplates"
INSTALL_URL="https://raw.githubusercontent.com/$GITHUB_REPO/main/scripts/install.sh"

show_help() {
    echo -e "${CYAN}${BOLD}ProjectVSCode Presets Installer${NC}"
    echo ""
    echo "Usage: install.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --preset <name>    Install a specific preset"
    echo "  --list            Show all available presets"
    echo "  --help            Show this help message"
    echo "  --version         Show version"
    echo ""
    echo "Examples:"
    echo "  install.sh --preset python-beginner"
    echo "  install.sh --list"
    echo ""
}

show_version() {
    echo "ProjectVSCode Presets Installer v$VERSION"
}

show_presets() {
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local manifest_file="$script_dir/../presets/manifest.json"

    if [ -f "$manifest_file" ]; then
        echo -e "${CYAN}${BOLD}Available Presets:${NC}"
        echo ""

        python3 -c "
import json
with open('$manifest_file') as f:
    data = json.load(f)
    for preset in data['presets']:
        print(f\"  {preset['id']:30} - {preset['description'][:50]}...\")
        print(f\"    Category: {preset['category']:15} Difficulty: {preset['difficulty']}\")
        print()
\" 2>/dev/null || cat "$manifest_file" | grep -E '"id"|"description"' | head -30
    else
        echo -e "${YELLOW}Fetching preset list from GitHub...${NC}"
        echo ""
        curl -s "https://raw.githubusercontent.com/$GITHUB_REPO/main/presets/manifest.json" 2>/dev/null | \
            python3 -c "
import json, sys
data = json.load(sys.stdin)
for preset in data['presets']:
    print(f\"  {preset['id']:30} - {preset['description'][:50]}...\")
    print(f\"    Category: {preset['category']:15} Difficulty: {preset['difficulty']}\")
    print()
" 2>/dev/null || echo -e "${RED}Could not fetch presets. Check your internet connection.${NC}"
    fi
}

get_preset_dir() {
    local preset_id="$1"
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local local_preset="$script_dir/../presets/$preset_id"
    local remote_preset="https://raw.githubusercontent.com/$GITHUB_REPO/main/presets/$preset_id"

    if [ -d "$local_preset" ] && [ -f "$local_preset/settings.json" ]; then
        echo "$local_preset"
        return 0
    elif curl -s --head "$remote_preset/settings.json" | head -1 | grep -q "200"; then
        echo "$remote_preset"
        return 0
    else
        return 1
    fi
}

detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "linux" ;;
        Darwin*)    echo "mac" ;;
        CYGWIN*)    echo "windows" ;;
        MINGW*)     echo "windows" ;;
        *)          echo "unknown" ;;
    esac
}

get_vscode_config_dir() {
    local os="$1"

    case "$os" in
        linux)
            echo "$HOME/.config/Code/User"
            ;;
        mac)
            echo "$HOME/Library/Application Support/Code/User"
            ;;
        windows)
            echo "$APPDATA/Code/User"
            ;;
        *)
            echo "$HOME/.config/Code/User"
            ;;
    esac
}

backup_existing() {
    local file="$1"
    local backup=""

    if [ -f "$file" ]; then
        local timestamp=$(date +"%Y-%m-%d-%H%M%S")
        backup="${file}.backup.${timestamp}"
        cp "$file" "$backup"
        echo -e "${YELLOW}Backed up existing file to: $backup${NC}"
    fi
}

install_preset() {
    local preset_id="$1"
    local preset_path=""
    local is_remote=false

    echo -e "${CYAN}${BOLD}Installing preset: $preset_id${NC}"
    echo ""

    if ! preset_path=$(get_preset_dir "$preset_id"); then
        echo -e "${RED}Error: Preset '$preset_id' not found.${NC}"
        echo -e "${YELLOW}Run 'install.sh --list' to see available presets.${NC}"
        exit 1
    fi

    if [[ "$preset_path" == http* ]]; then
        is_remote=true
        echo -e "${YELLOW}Using remote preset from GitHub...${NC}"
    else
        echo -e "${YELLOW}Using local preset...${NC}"
    fi

    local os=$(detect_os)
    local config_dir=$(get_vscode_config_dir "$os")

    echo ""
    echo -e "${CYAN}VS Code config directory: $config_dir${NC}"
    echo ""

    if [ ! -d "$config_dir" ]; then
        mkdir -p "$config_dir"
        echo -e "${YELLOW}Created config directory.${NC}"
    fi

    echo -e "${CYAN}${BOLD}Installing settings...${NC}"
    backup_existing "$config_dir/settings.json"

    if [ "$is_remote" = true ]; then
        curl -s "$preset_path/settings.json" -o "$config_dir/settings.json"
    else
        cp "$preset_path/settings.json" "$config_dir/settings.json"
    fi
    echo -e "${GREEN}✓ settings.json installed${NC}"

    echo ""
    echo -e "${CYAN}${BOLD}Installing extensions...${NC}"
    backup_existing "$config_dir/extensions.json"

    if [ "$is_remote" = true ]; then
        curl -s "$preset_path/extensions.json" -o "$config_dir/extensions.json"
    else
        cp "$preset_path/extensions.json" "$config_dir/extensions.json"
    fi
    echo -e "${GREEN}✓ extensions.json installed${NC}"

    echo ""
    echo -e "${CYAN}${BOLD}Installing keybindings...${NC}"
    backup_existing "$config_dir/keybindings.json"

    if [ "$is_remote" = true ]; then
        curl -s "$preset_path/keybindings.json" -o "$config_dir/keybindings.json"
    else
        cp "$preset_path/keybindings.json" "$config_dir/keybindings.json"
    fi
    echo -e "${GREEN}✓ keybindings.json installed${NC}"

    local snippets_dir="$config_dir/snippets"
    if [ ! -d "$snippets_dir" ]; then
        mkdir -p "$snippets_dir"
    fi

    local snippets_file=""
    if [ "$is_remote" = true ]; then
        snippets_file="$snippets_dir/${preset_id}.code-snippets"
        curl -s "${preset_path}.code-snippets" -o "$snippets_file" 2>/dev/null && \
            echo -e "${GREEN}✓ Snippets installed${NC}" || true
    elif [ -f "$preset_path/${preset_id}.code-snippets" ]; then
        cp "$preset_path/${preset_id}.code-snippets" "$snippets_dir/"
        echo -e "${GREEN}✓ Snippets installed${NC}"
    fi

    echo ""
    echo -e "${CYAN}${BOLD}Installing extensions in VS Code...${NC}"
    if command -v code &> /dev/null; then
        while IFS= read -r ext; do
            ext=$(echo "$ext" | tr -d '"' | tr -d '[:space:]')
            if [ -n "$ext" ]; then
                echo -e "${YELLOW}Installing: $ext${NC}"
                code --install-extension "$ext" --force 2>/dev/null || \
                    echo -e "${YELLOW}  (requires VS Code restart)${NC}"
            fi
        done < "$config_dir/extensions.json"
        echo -e "${GREEN}✓ Extensions installation initiated${NC}"
    else
        echo -e "${YELLOW}VS Code CLI not found. Extensions will be suggested when you open VS Code.${NC}"
    fi

    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}                                                              ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   ${GREEN}${BOLD}✅ Preset installed: $preset_id${NC}"
    echo -e "${GREEN}║${NC}                                                              ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   ${WHITE}📁 Settings: $config_dir${NC}"
    echo -e "${GREEN}║${NC}                                                              ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   ${WHITE}📦 Extensions: See extensions.json${NC}"
    echo -e "${GREEN}║${NC}                                                              ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   ${WHITE}🔑 Keybindings: Applied${NC}"
    echo -e "${GREEN}║${NC}                                                              ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   ${WHITE}Restart VS Code for all changes to take effect${NC}"
    echo -e "${GREEN}║${NC}                                                              ${GREEN}║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

PRESET=""
LIST_PRESETS=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --preset)
            PRESET="$2"
            shift 2
            ;;
        --list)
            LIST_PRESETS=true
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
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

if [ "$LIST_PRESETS" = true ]; then
    show_presets
elif [ -n "$PRESET" ]; then
    install_preset "$PRESET"
else
    show_help
    exit 1
fi
