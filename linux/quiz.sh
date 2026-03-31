#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALLER="$SCRIPT_DIR/install.sh"

cyan='\033[0;36m'
green='\033[0;32m'
yellow='\033[1;33m'
red='\033[0;31m'
reset='\033[0m'

print_header() {
    clear
    printf '%sProject VsCode Templates%s\n' "$cyan" "$reset"
    printf 'Find a good VS Code preset in a few simple steps.\n\n'
}

menu() {
    local prompt="$1"
    shift
    local options=("$@")
    local total="${#options[@]}"
    local choice=""

    while true; do
        printf '%s\n' "$prompt"
        local i=1
        for option in "${options[@]}"; do
            printf '  %s%d.%s %s\n' "$yellow" "$i" "$reset" "$option"
            ((i++))
        done
        printf '\nChoose an option: '
        read -r choice

        if [[ "$choice" =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= total )); then
            echo "$choice"
            return
        fi

        printf '%sPlease enter a number between 1 and %d.%s\n\n' "$red" "$total" "$reset"
    done
}

recommend_preset() {
    local track="$1"
    local level="$2"
    local style="$3"

    case "$track" in
        1)
            if [[ "$style" == "2" ]]; then echo "minimal-zen"; return; fi
            if [[ "$style" == "3" ]]; then echo "streamer-content-creator"; return; fi
            if [[ "$level" == "1" ]]; then echo "python-beginner"; return; fi
            if [[ "$level" == "2" ]]; then echo "data-science"; return; fi
            echo "python-professional"
            ;;
        2)
            if [[ "$level" == "3" ]]; then echo "web-dev-fullstack"; else echo "web-dev-frontend"; fi
            ;;
        3) echo "web-dev-fullstack" ;;
        4) echo "c-cpp-systems" ;;
        5) echo "competitive-programming" ;;
        6) echo "java-student" ;;
        7)
            local lang
            lang="$(menu "Pick the language you want the preset for." "Rust" "Go")"
            if [[ "$lang" == "1" ]]; then echo "rust-systems"; else echo "go-backend"; fi
            ;;
        8) echo "mobile-flutter" ;;
        9)
            if [[ "$style" == "4" ]]; then echo "remote-ssh-server"; else echo "devops-cloud"; fi
            ;;
        10)
            if [[ "$style" == "3" ]]; then echo "streamer-content-creator"; return; fi
            if [[ "$style" == "4" ]]; then echo "remote-ssh-server"; return; fi
            echo "minimal-zen"
            ;;
        *) echo "python-beginner" ;;
    esac
}

main() {
    if [[ ! -x "$INSTALLER" ]]; then
        chmod +x "$INSTALLER" 2>/dev/null || true
    fi

    print_header
    printf 'Answer 3 short questions and I will recommend a preset.\n\n'

    local track
    local level
    local style
    local preset
    local answer

    track="$(menu "What do you mainly do in VS Code?" \
        "Python or data science" \
        "Frontend web development" \
        "Full-stack web development" \
        "C or C++" \
        "Competitive programming" \
        "Java" \
        "Rust or Go" \
        "Mobile with Flutter" \
        "DevOps or cloud work" \
        "Writing, notes, and minimal setup")"

    printf '\n'
    level="$(menu "Which experience level fits you best?" \
        "Complete beginner" \
        "Learning and building projects" \
        "Working professional")"

    printf '\n'
    style="$(menu "What matters most in your setup?" \
        "Balanced everyday coding" \
        "Minimal and distraction-free" \
        "Streaming or recording" \
        "Remote SSH work")"

    preset="$(recommend_preset "$track" "$level" "$style")"

    printf '\n%sRecommended preset:%s %s%s%s\n' "$green" "$reset" "$cyan" "$preset" "$reset"
    printf 'Install it now? [Y/n]: '
    read -r answer

    if [[ "$answer" =~ ^[Nn]$ ]]; then
        printf '\nRun this later when you are ready:\n'
        printf '  ./linux/install.sh --preset %s\n' "$preset"
        exit 0
    fi

    exec "$INSTALLER" --preset "$preset"
}

main "$@"
