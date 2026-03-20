#!/bin/bash
# =============================================================================
# scan.sh – Automated nmap reconnaissance script
# CGT 312 Ethical Hacking – Module 2
# =============================================================================
# Usage: bash scan.sh <target>
# Example: bash scan.sh scanme.nmap.org
#
# LEGAL NOTICE: Only scan systems you own or have explicit written permission.
# Authorised targets: scanme.nmap.org, localhost, 127.0.0.1
# =============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# ─── Check arguments ─────────────────────────────────────────────────────────

if [ $# -eq 0 ]; then
    echo -e "${RED}Usage: bash scan.sh <target>${NC}"
    echo "  Example: bash scan.sh scanme.nmap.org"
    echo "  Example: bash scan.sh 127.0.0.1"
    exit 1
fi

TARGET="$1"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$SCRIPT_DIR/logs/module2"

mkdir -p "$LOG_DIR"

# ─── Ethical warning ─────────────────────────────────────────────────────────

echo -e "${RED}"
echo "╔═══════════════════════════════════════════════╗"
echo "║  ⚠  ETHICAL USE WARNING                      ║"
echo "║  Only scan systems you own or have written   ║"
echo "║  permission to test. Unauthorized scanning   ║"
echo "║  is illegal.                                 ║"
echo "╚═══════════════════════════════════════════════╝"
echo -e "${NC}"

# ─── Check nmap available ────────────────────────────────────────────────────

if ! command -v nmap &>/dev/null; then
    echo -e "${RED}[!] nmap not found. Run: bash setup.sh${NC}"
    exit 1
fi

echo -e "${CYAN}[*] Starting scan of: $TARGET${NC}"
echo -e "${CYAN}[*] Timestamp: $TIMESTAMP${NC}"
echo -e "${CYAN}[*] Logs: $LOG_DIR/${NC}\n"

LOG_FILE="$LOG_DIR/${TIMESTAMP}_${TARGET//./_}.txt"

# ─── Log header ──────────────────────────────────────────────────────────────

{
    echo "# CGT 312 Ethical Hacking – Module 2 Scan"
    echo "# Target: $TARGET"
    echo "# Timestamp: $TIMESTAMP"
    echo "# Tool: nmap"
    echo "# ─────────────────────────────────────────"
} > "$LOG_FILE"

# ─── Phase 1: Host discovery ─────────────────────────────────────────────────

echo -e "${GREEN}[1/4] Host discovery (ping scan)...${NC}"
CMD="nmap -sn $TARGET"
echo -e "${YELLOW}\$ $CMD${NC}"
echo -e "\n## Phase 1: Host Discovery\n\$ $CMD\n" >> "$LOG_FILE"
nmap -sn "$TARGET" 2>&1 | tee -a "$LOG_FILE"
echo ""

# ─── Phase 2: Port scan with service version detection ───────────────────────

echo -e "${GREEN}[2/4] Service version detection (-sV -sC)...${NC}"
CMD="nmap -sV -sC $TARGET"
echo -e "${YELLOW}\$ $CMD${NC}"
echo -e "\n## Phase 2: Service Version + Default Scripts\n\$ $CMD\n" >> "$LOG_FILE"
nmap -sV -sC "$TARGET" 2>&1 | tee -a "$LOG_FILE"
echo ""

# ─── Phase 3: OS detection (attempt – may need root) ─────────────────────────

echo -e "${GREEN}[3/4] OS detection (requires root for best results)...${NC}"
CMD="nmap -O $TARGET"
echo -e "${YELLOW}\$ $CMD${NC}"
echo -e "\n## Phase 3: OS Detection\n\$ $CMD\n" >> "$LOG_FILE"
nmap -O "$TARGET" 2>&1 | tee -a "$LOG_FILE"
echo ""

# ─── Phase 4: Targeted top-port scan with timing ─────────────────────────────

echo -e "${GREEN}[4/4] Full scan: top 1000 ports (-T4)...${NC}"
CMD="nmap -T4 --top-ports 1000 $TARGET"
echo -e "${YELLOW}\$ $CMD${NC}"
echo -e "\n## Phase 4: Top 1000 Ports\n\$ $CMD\n" >> "$LOG_FILE"
nmap -T4 --top-ports 1000 "$TARGET" 2>&1 | tee -a "$LOG_FILE"

# ─── Summary ─────────────────────────────────────────────────────────────────

echo ""
echo -e "${GREEN}════════════════════════════════════════════${NC}"
echo -e "${GREEN}[+] Scan complete!${NC}"
echo -e "${GREEN}[+] Full log saved: $LOG_FILE${NC}"
echo -e "${GREEN}════════════════════════════════════════════${NC}"
