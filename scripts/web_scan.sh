#!/bin/bash
# =============================================================================
# web_scan.sh – Web application scanning script
# CGT 312 Ethical Hacking – Module 4
# =============================================================================
# LEGAL NOTICE: Only scan web applications you own or have written permission.
# Authorized: testphp.vulnweb.com (Acunetix), localhost, DVWA.
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$SCRIPT_DIR/logs/module4"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
TARGET="${1:-http://testphp.vulnweb.com}"

mkdir -p "$LOG_DIR"

echo -e "${RED}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║  ⚠  ETHICAL USE WARNING – MODULE 4                  ║"
echo "║                                                      ║"
echo "║  Only scan web apps you OWN or have WRITTEN         ║"
echo "║  permission to test.                                ║"
echo "║  Authorized: testphp.vulnweb.com (Acunetix)        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}[*] Web Scan: $TARGET${NC}"
echo -e "${CYAN}[*] Timestamp: $TIMESTAMP${NC}\n"

LOG_FILE="$LOG_DIR/${TIMESTAMP}_webscan.txt"
{
    echo "# CGT 312 Web Scan"
    echo "# Target: $TARGET"
    echo "# Timestamp: $TIMESTAMP"
    echo "# ─────────────────────────────────────────────────"
} > "$LOG_FILE"

# ─── Step 1: whatweb fingerprint ─────────────────────────────────────────────

echo -e "${GREEN}[Step 1] whatweb – Technology Fingerprint${NC}"
if command -v whatweb &>/dev/null; then
    CMD="whatweb -v $TARGET"
    echo -e "${CYAN}\$ $CMD${NC}\n"
    echo -e "\n## Step 1: whatweb\n\$ $CMD\n" >> "$LOG_FILE"
    whatweb -v "$TARGET" 2>&1 | tee -a "$LOG_FILE"
else
    echo -e "  ${YELLOW}whatweb not found. Run: bash setup.sh${NC}"
fi
echo ""

# ─── Step 2: HTTP header analysis ────────────────────────────────────────────

echo -e "${GREEN}[Step 2] HTTP Header Analysis${NC}"
if command -v curl &>/dev/null; then
    CMD="curl -sI $TARGET"
    echo -e "${CYAN}\$ $CMD${NC}\n"
    echo -e "\n## Step 2: HTTP Headers\n\$ $CMD\n" >> "$LOG_FILE"
    curl -sI "$TARGET" 2>&1 | tee -a "$LOG_FILE"

    # Check for missing security headers
    echo -e "\n${YELLOW}Security Header Audit:${NC}"
    echo -e "\n### Security Header Audit\n" >> "$LOG_FILE"
    HEADERS=$(curl -sI "$TARGET" 2>&1)

    check_header() {
        local header="$1"
        if echo "$HEADERS" | grep -qi "$header"; then
            echo -e "  ${GREEN}✔ $header: PRESENT${NC}"
            echo "  ✔ $header: PRESENT" >> "$LOG_FILE"
        else
            echo -e "  ${RED}✘ $header: MISSING${NC}"
            echo "  ✘ $header: MISSING" >> "$LOG_FILE"
        fi
    }

    check_header "X-Frame-Options"
    check_header "X-XSS-Protection"
    check_header "Strict-Transport-Security"
    check_header "Content-Security-Policy"
    check_header "X-Content-Type-Options"
else
    echo -e "  ${YELLOW}curl not found.${NC}"
fi
echo ""

# ─── Step 3: nikto scan ──────────────────────────────────────────────────────

echo -e "${GREEN}[Step 3] nikto – Web Vulnerability Scanner${NC}"
if command -v nikto &>/dev/null; then
    CMD="nikto -h $TARGET"
    echo -e "${CYAN}\$ $CMD${NC}\n"
    echo -e "\n## Step 3: nikto\n\$ $CMD\n" >> "$LOG_FILE"
    # Limit to 60 lines for readability in script output
    nikto -h "$TARGET" 2>&1 | tee -a "$LOG_FILE" | head -60
    echo -e "\n  (Full output saved to log)"
else
    echo -e "  ${YELLOW}nikto not found. Run: bash setup.sh${NC}"
fi
echo ""

# ─── Step 4: gobuster directory scan ─────────────────────────────────────────

echo -e "${GREEN}[Step 4] gobuster – Directory Brute Force${NC}"
if command -v gobuster &>/dev/null; then
    # Find a wordlist
    WORDLIST=""
    for wl in \
        /usr/share/wordlists/dirb/common.txt \
        /data/data/com.termux/files/usr/share/wordlists/dirb/common.txt \
        /usr/share/dirb/wordlists/common.txt; do
        if [ -f "$wl" ]; then
            WORDLIST="$wl"
            break
        fi
    done

    if [ -n "$WORDLIST" ]; then
        CMD="gobuster dir -u $TARGET -w $WORDLIST -t 20"
        echo -e "${CYAN}\$ $CMD${NC}\n"
        echo -e "\n## Step 4: gobuster\n\$ $CMD\n" >> "$LOG_FILE"
        gobuster dir -u "$TARGET" -w "$WORDLIST" -t 20 2>&1 | \
            tee -a "$LOG_FILE" | head -40
    else
        echo -e "  ${YELLOW}Wordlist not found. Install: pkg install wordlists${NC}"
    fi
else
    echo -e "  ${YELLOW}gobuster not found. Run setup.sh and choose to install gobuster via Go.${NC}"
fi
echo ""

# ─── Summary ─────────────────────────────────────────────────────────────────

echo -e "${GREEN}════════════════════════════════════════════${NC}"
echo -e "${GREEN}[+] Web Scan Complete!${NC}"
echo -e "${GREEN}[+] Log saved: $LOG_FILE${NC}"
echo -e "${GREEN}════════════════════════════════════════════${NC}"
