#!/bin/bash
# =============================================================================
# CGT 312 Ethical Hacking – Termux Setup Script
# Installs all required tools for the course labs
# =============================================================================
# LEGAL NOTICE: Tools installed here are for educational use only.
# Only use on systems you own or have explicit permission to test.
# =============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║      CGT 312 Ethical Hacking Setup           ║"
    echo "║       Termux Tool Installer v1.0             ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
}

warn() {
    echo -e "${RED}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║  ⚠  ETHICAL USE REMINDER                    ║"
    echo "║                                              ║"
    echo "║  These tools are for EDUCATIONAL USE ONLY.  ║"
    echo "║  Only test systems you OWN or have written  ║"
    echo "║  permission to test.                        ║"
    echo "║  Unauthorized use is ILLEGAL.               ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
}

step() {
    echo -e "${GREEN}[+]${NC} $1"
}

info() {
    echo -e "${YELLOW}[*]${NC} $1"
}

# Detect environment (Termux vs regular Linux)
detect_env() {
    if [ -d "/data/data/com.termux" ]; then
        echo "termux"
    else
        echo "linux"
    fi
}

# Update package repositories
update_packages() {
    step "Updating package repositories..."
    ENV=$(detect_env)
    if [ "$ENV" = "termux" ]; then
        pkg update -y && pkg upgrade -y
    else
        sudo apt-get update -y && sudo apt-get upgrade -y
    fi
    echo ""
}

# Install core tools
install_core() {
    step "Installing core tools (nmap, python, git, curl, wget)..."
    ENV=$(detect_env)
    if [ "$ENV" = "termux" ]; then
        pkg install -y git curl wget nmap python python-pip
    else
        sudo apt-get install -y git curl wget nmap python3 python3-pip
    fi
    echo ""
}

# Install attack simulation tools
install_attack_tools() {
    step "Installing attack simulation tools (hydra, sqlmap, john, nikto, whatweb)..."
    ENV=$(detect_env)
    if [ "$ENV" = "termux" ]; then
        pkg install -y hydra sqlmap nikto whatweb john
    else
        sudo apt-get install -y hydra sqlmap nikto whatweb john
    fi
    echo ""
}

# Install network tools
install_network_tools() {
    step "Installing network tools (netcat, tshark)..."
    ENV=$(detect_env)
    if [ "$ENV" = "termux" ]; then
        pkg install -y netcat tshark
    else
        sudo apt-get install -y netcat tshark
    fi
    echo ""
}

# Install Python dependencies
install_python_deps() {
    step "Installing Python dependencies..."
    pip install requests colorama tabulate 2>/dev/null || \
    pip3 install requests colorama tabulate 2>/dev/null || true
    echo ""
}

# Install gobuster via Go
install_gobuster() {
    echo -e "${YELLOW}[?]${NC} Install gobuster (requires Go, ~50MB)? [y/N]: \c"
    read -r ans
    if [[ "$ans" =~ ^[Yy]$ ]]; then
        step "Installing Go and gobuster..."
        ENV=$(detect_env)
        if [ "$ENV" = "termux" ]; then
            pkg install -y golang
        else
            sudo apt-get install -y golang
        fi
        go install github.com/OJ/gobuster/v3@latest 2>/dev/null && \
            step "gobuster installed at $(go env GOPATH)/bin/gobuster" || \
            info "gobuster install failed – you can retry manually: go install github.com/OJ/gobuster/v3@latest"
    else
        info "Skipping gobuster."
    fi
    echo ""
}

# Optional: Metasploit (heavy)
install_metasploit() {
    echo -e "${YELLOW}[?]${NC} Install Metasploit Framework (HEAVY ~1GB, Termux only)? [y/N]: \c"
    read -r ans
    if [[ "$ans" =~ ^[Yy]$ ]]; then
        step "Installing Metasploit via Termux..."
        curl -LO https://github.com/termux/termux-packages/raw/master/packages/metasploit/metasploit-framework_*.deb 2>/dev/null || true
        pkg install -y metasploit || \
            info "Metasploit not available via pkg. Try: pkg install unstable-repo && pkg install metasploit"
    else
        info "Skipping Metasploit."
    fi
    echo ""
}

# Create log directories
setup_dirs() {
    step "Creating log and report directories..."
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    mkdir -p "$SCRIPT_DIR/logs/module1" \
             "$SCRIPT_DIR/logs/module2" \
             "$SCRIPT_DIR/logs/module3" \
             "$SCRIPT_DIR/logs/module4" \
             "$SCRIPT_DIR/logs/module5" \
             "$SCRIPT_DIR/reports"
    chmod +x "$SCRIPT_DIR/scripts/"*.sh 2>/dev/null || true
    echo ""
}

# Verify installations
verify() {
    step "Verifying tool installations..."
    TOOLS=("nmap" "python" "hydra" "nikto" "john" "tshark")
    ALL_OK=true
    for tool in "${TOOLS[@]}"; do
        if command -v "$tool" &>/dev/null; then
            echo -e "  ${GREEN}✔${NC} $tool"
        else
            echo -e "  ${RED}✘${NC} $tool (not found)"
            ALL_OK=false
        fi
    done
    echo ""
    if $ALL_OK; then
        echo -e "${GREEN}[+] All core tools installed successfully!${NC}"
    else
        echo -e "${YELLOW}[!] Some tools missing. Re-run setup.sh or install manually.${NC}"
    fi
    echo ""
}

# Main
main() {
    banner
    warn
    echo -e "${YELLOW}[?]${NC} Continue with installation? [y/N]: \c"
    read -r confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
    echo ""
    update_packages
    install_core
    install_attack_tools
    install_network_tools
    install_python_deps
    install_gobuster
    install_metasploit
    setup_dirs
    verify
    step "Setup complete! Run: python cli.py"
}

main
