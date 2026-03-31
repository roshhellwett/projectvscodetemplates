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

clear_screen() {
    clear
}

print_header() {
    echo -e "${CYAN}"
    echo "  ╔═══════════════════════════════════════════════════════════════╗"
    echo "  ║                                                               ║"
    echo "  ║              🖥️  ProjectVSCode Presets                      ║"
    echo "  ║                                                               ║"
    echo "  ║        Your perfect VS Code setup in 60 seconds               ║"
    echo "  ║                                                               ║"
    echo "  ╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

pause() {
    echo ""
    echo -e "${WHITE}Press ${BOLD}ENTER${NC} ${WHITE}to continue...${NC}"
    read -r
}

get_input() {
    local prompt="$1"
    local options=("${@:2}")
    local valid=false
    local choice=""

    while [ "$valid" = false ]; do
        echo ""
        echo -e "${CYAN}${prompt}${NC}"
        echo ""

        local i=1
        for option in "${options[@]}"; do
            echo -e "  ${WHITE}${i})${NC} ${option}"
            ((i++))
        done

        echo ""
        echo -ne "${YELLOW}Enter your choice (1-${#options[@]}): ${NC}"
        read -r choice

        if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le ${#options[@]} ]; then
            valid=true
        else
            echo -e "${RED}Invalid choice. Please try again.${NC}"
        fi
    done

    echo "$choice"
}

print_result() {
    local preset_id="$1"
    local preset_name="$2"
    local description="$3"

    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   ${GREEN}${BOLD}✅ Your perfect preset: ${preset_name}${NC}"
    echo -e "${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   ${WHITE}${description}${NC}"
    echo -e "${GREEN}║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

ask_install() {
    echo -e "${WHITE}Install now?${NC}"
    echo ""
    echo -e "  ${GREEN}Y${NC}) Yes, install this preset"
    echo -e "  ${RED}N${NC}) No, show manual instructions"
    echo ""
    echo -ne "${YELLOW}Choice [Y/n]: ${NC}"
    read -r answer

    case "$answer" in
        [Nn])
            return 1
            ;;
        *)
            return 0
            ;;
    esac
}

show_manual_instructions() {
    local preset_id="$1"
    echo ""
    echo -e "${CYAN}${BOLD}Manual Installation:${NC}"
    echo ""
    echo -e "${WHITE}1. Navigate to your VS Code settings directory:${NC}"
    echo ""
    echo -e "   ${YELLOW}Linux/Mac:${NC} ~/.config/Code/User/"
    echo -e "   ${YELLOW}Windows:${NC} %APPDATA%\\Code\\User\\"
    echo ""
    echo -e "${WHITE}2. Copy these files from the preset:${NC}"
    echo ""
    echo -e "   - ${CYAN}settings.json${NC}"
    echo -e "   - ${CYAN}extensions.json${NC}"
    echo -e "   - ${CYAN}keybindings.json${NC}"
    echo ""
    echo -e "${WHITE}3. Install the recommended extensions:${NC}"
    echo ""
    echo -e "   VS Code will prompt you to install them from extensions.json"
    echo ""
}

run_installer() {
    local preset_id="$1"
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local installer="$script_dir/install.sh"

    if [ -f "$installer" ]; then
        echo ""
        echo -e "${CYAN}Running installer...${NC}"
        echo ""
        bash "$installer" --preset "$preset_id"
    else
        echo -e "${RED}Installer not found at: $installer${NC}"
        show_manual_instructions "$preset_id"
    fi
}

main() {
    clear_screen
    print_header

    echo ""
    echo -e "${WHITE}Answer 4 quick questions. Get your perfect setup.${NC}"
    pause

    clear_screen
    print_header

    echo -e "${CYAN}${BOLD}Question 1 of 4${NC}"
    echo -e "${WHITE}What do you code?${NC}"
    q1=$(get_input "" \
        "Python / Data Science / ML" \
        "Web (HTML, CSS, JavaScript, React)" \
        "Full-Stack (Frontend + Backend + DB)" \
        "C / C++ (university, systems)" \
        "Competitive Programming (contests, DSA)" \
        "Java (university, Android)" \
        "Rust or Go (systems, backend)" \
        "Mobile (Flutter, React Native)" \
        "DevOps / Cloud / Infra" \
        "I just write and take notes")

    clear_screen
    print_header

    echo -e "${CYAN}${BOLD}Question 2 of 4${NC}"
    echo -e "${WHITE}What's your experience level?${NC}"
    q2=$(get_input "" \
        "Complete beginner (< 6 months)" \
        "Learning (6 months - 2 years)" \
        "Working professional")

    clear_screen
    print_header

    echo -e "${CYAN}${BOLD}Question 3 of 4${NC}"
    echo -e "${WHITE}How do you use VS Code?${NC}"
    q3=$(get_input "" \
        "Just coding" \
        "I stream or record content" \
        "I want minimal distractions" \
        "Remote server / SSH work")

    clear_screen
    print_header

    echo -e "${CYAN}${BOLD}Question 4 of 4${NC}"
    echo -e "${WHITE}What's your operating system?${NC}"
    q4=$(get_input "" \
        "Linux / Mac" \
        "Windows")

    clear_screen
    print_header

    local preset_id=""
    local preset_name=""
    local description=""

    case "$q1" in
        1)
            case "$q3" in
                2) preset_id="streamer-content-creator"; preset_name="Streamer & Content Creator"; description="Optimized for recording and streaming. Large fonts, theme switching." ;;
                3) preset_id="minimal-zen"; preset_name="Minimal Zen"; description="Distraction-free writing. Hidden sidebars, peaceful colors." ;;
                *) 
                    case "$q2" in
                        1) preset_id="python-beginner"; preset_name="Python Beginner"; description="Large fonts, auto-formatting, inline errors. Perfect for learning." ;;
                        *) preset_id="python-professional"; preset_name="Python Professional"; description="Type checking, testing tools, production-ready configuration." ;;
                    esac
                    ;;
            esac
            ;;
        2)
            case "$q2" in
                1) preset_id="web-dev-frontend"; preset_name="Web Dev - Frontend"; description="React, Vue, Tailwind. Prettier + ESLint configured." ;;
                *) preset_id="web-dev-frontend"; preset_name="Web Dev - Frontend"; description="React, Vue, Tailwind. Prettier + ESLint configured." ;;
            esac
            ;;
        3)
            preset_id="web-dev-fullstack"
            preset_name="Web Dev - Fullstack"
            description="Complete fullstack setup. Node.js, databases, Docker support."
            ;;
        4)
            preset_id="c-cpp-systems"
            preset_name="C/C++ Systems"
            description="Low-level C/C++ with CMake, Makefile, and debugger support."
            ;;
        5)
            preset_id="competitive-programming"
            preset_name="Competitive Programming"
            description="One-key run with input.txt, contest snippets, Tokyo Night theme."
            ;;
        6)
            preset_id="java-student"
            preset_name="Java Student"
            description="University-ready Java with Maven/Gradle and JUnit testing."
            ;;
        7)
            echo ""
            echo -e "${CYAN}${BOLD}Which language?${NC}"
            lang_choice=$(get_input "" \
                "Rust" \
                "Go")
            case "$lang_choice" in
                1) preset_id="rust-systems"; preset_name="Rust Systems"; description="Memory safety tooling, Clippy, rust-analyzer, Cargo integration." ;;
                2) preset_id="go-backend"; preset_name="Go Backend"; description="Go development with gofmt, testing, and debugging workflows." ;;
            esac
            ;;
        8)
            preset_id="mobile-flutter"
            preset_name="Mobile (Flutter)"
            description="Flutter and Dart with hot reload optimization."
            ;;
        9)
            preset_id="devops-cloud"
            preset_name="DevOps & Cloud"
            description="Docker, Kubernetes, Terraform, and cloud CLI tools."
            ;;
        10)
            case "$q3" in
                2) preset_id="streamer-content-creator"; preset_name="Streamer & Content Creator"; description="High contrast, large fonts, beautiful on camera." ;;
                3) preset_id="minimal-zen"; preset_name="Minimal Zen"; description="Distraction-free writing. Hidden sidebars, peaceful colors." ;;
                4) preset_id="remote-ssh-server"; preset_name="Remote SSH Server"; description="Work on remote servers via SSH with native feel." ;;
                *) preset_id="minimal-zen"; preset_name="Minimal Zen"; description="Distraction-free writing. Hidden sidebars, peaceful colors." ;;
            esac
            ;;
    esac

    if [ -z "$preset_id" ]; then
        preset_id="python-beginner"
        preset_name="Python Beginner"
        description="Large fonts, auto-formatting, inline errors. Perfect for learning."
    fi

    print_result "$preset_id" "$preset_name" "$description"

    if ask_install; then
        run_installer "$preset_id"
    else
        show_manual_instructions "$preset_id"
    fi

    echo ""
    echo -e "${GREEN}Thank you for using ProjectVSCode Presets!${NC}"
    echo ""
}

main "$@"
