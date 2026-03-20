#!/bin/bash
# =============================================================================
# log_parser.sh – Apache/Nginx log forensics parser
# CGT 312 Ethical Hacking – Module 5
# =============================================================================
# Usage: bash log_parser.sh [logfile]
# Default: labs/sample_access.log
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$SCRIPT_DIR/logs/module5"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOGFILE="${1:-$SCRIPT_DIR/labs/sample_access.log}"

mkdir -p "$LOG_DIR"

# Check log file exists
if [ ! -f "$LOGFILE" ]; then
    echo -e "${RED}[!] Log file not found: $LOGFILE${NC}"
    echo -e "${YELLOW}    Run: python cli.py → Option 6 → b to generate sample log${NC}"
    exit 1
fi

OUTPUT_FILE="$LOG_DIR/${TIMESTAMP}_log_parse.txt"

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════╗"
echo "║    CGT 312 – Log Forensics Parser             ║"
echo "║    Module 5: Digital Forensics                ║"
echo "╚═══════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}[*] Analyzing: $LOGFILE${NC}"
echo -e "${CYAN}[*] Report:    $OUTPUT_FILE${NC}\n"

{
    echo "# CGT 312 Log Forensics Report"
    echo "# Source: $LOGFILE"
    echo "# Timestamp: $TIMESTAMP"
    echo "# ─────────────────────────────────────────────────"
} > "$OUTPUT_FILE"

# ─── Section 1: Basic stats ───────────────────────────────────────────────────

echo -e "${BOLD}── 1. Basic Statistics ──────────────────────────────${NC}"
echo -e "\n## 1. Basic Statistics\n" >> "$OUTPUT_FILE"

TOTAL=$(wc -l < "$LOGFILE")
UNIQUE_IPS=$(awk '{print $1}' "$LOGFILE" | sort -u | wc -l)
ERRORS=$(grep -cE '" [45][0-9]{2} ' "$LOGFILE" || true)

echo -e "  Total log entries:  ${GREEN}$TOTAL${NC}"
echo -e "  Unique IP addresses: ${GREEN}$UNIQUE_IPS${NC}"
echo -e "  4xx/5xx errors:      ${RED}$ERRORS${NC}"
echo ""

echo "Total entries: $TOTAL" >> "$OUTPUT_FILE"
echo "Unique IPs:    $UNIQUE_IPS" >> "$OUTPUT_FILE"
echo "Errors (4xx/5xx): $ERRORS" >> "$OUTPUT_FILE"

# ─── Section 2: Top IPs ───────────────────────────────────────────────────────

echo -e "${BOLD}── 2. Top 10 IPs by Request Count ──────────────────${NC}"
echo -e "\n## 2. Top IPs\n" >> "$OUTPUT_FILE"

awk '{print $1}' "$LOGFILE" | sort | uniq -c | sort -rn | head -10 | \
while read count ip; do
    echo -e "  ${CYAN}$ip${NC}  →  ${YELLOW}$count requests${NC}"
    echo "  $ip → $count requests" >> "$OUTPUT_FILE"
done
echo ""

# ─── Section 3: HTTP Status Code Summary ─────────────────────────────────────

echo -e "${BOLD}── 3. HTTP Status Code Distribution ────────────────${NC}"
echo -e "\n## 3. Status Codes\n" >> "$OUTPUT_FILE"

awk '{print $9}' "$LOGFILE" | grep -E '^[0-9]{3}$' | sort | uniq -c | sort -rn | \
while read count code; do
    if [ "$code" -lt 300 ]; then
        colour="${GREEN}"
    elif [ "$code" -lt 400 ]; then
        colour="${YELLOW}"
    else
        colour="${RED}"
    fi
    echo -e "  ${colour}HTTP $code${NC}: $count responses"
    echo "  HTTP $code: $count" >> "$OUTPUT_FILE"
done
echo ""

# ─── Section 4: Brute Force Detection ────────────────────────────────────────

echo -e "${BOLD}── 4. Brute Force Detection (401 errors) ────────────${NC}"
echo -e "\n## 4. Brute Force Detection\n" >> "$OUTPUT_FILE"

BF_FOUND=false
awk '$9 == "401" {print $1}' "$LOGFILE" | sort | uniq -c | sort -rn | \
while read count ip; do
    if [ "$count" -ge 3 ]; then
        echo -e "  ${RED}⚠ SUSPECTED BRUTE FORCE:${NC} $ip → $count failed attempts (401)"
        echo "  SUSPECTED BRUTE FORCE: $ip → $count failed attempts" >> "$OUTPUT_FILE"
        BF_FOUND=true
    fi
done

if [ "$BF_FOUND" = false ]; then
    # Check if anything was output
    BF_COUNT=$(awk '$9 == "401" {print $1}' "$LOGFILE" | sort | uniq -c | sort -rn | awk '$1 >= 3' | wc -l)
    if [ "$BF_COUNT" -eq 0 ]; then
        echo -e "  ${GREEN}No brute force patterns detected.${NC}"
        echo "  No brute force patterns detected." >> "$OUTPUT_FILE"
    fi
fi
echo ""

# ─── Section 5: Attack Pattern Detection ─────────────────────────────────────

echo -e "${BOLD}── 5. Attack Pattern Detection ──────────────────────${NC}"
echo -e "\n## 5. Attack Patterns\n" >> "$OUTPUT_FILE"

check_pattern() {
    local name="$1"
    local pattern="$2"
    local count
    count=$(grep -ciE "$pattern" "$LOGFILE" || true)
    if [ "$count" -gt 0 ]; then
        echo -e "  ${RED}⚠ $name:${NC} $count matching request(s)"
        echo "  $name: $count matches" >> "$OUTPUT_FILE"
        grep -iE "$pattern" "$LOGFILE" | awk '{print "    IP:",$1,"Path:",$7}' | head -5
        grep -iE "$pattern" "$LOGFILE" | awk '{print "    "$1,"→",$7}' | head -5 >> "$OUTPUT_FILE"
    else
        echo -e "  ${GREEN}✔ No $name patterns found${NC}"
        echo "  No $name patterns" >> "$OUTPUT_FILE"
    fi
}

check_pattern "SQL Injection" '(%27|OR\+1=1|union.*select|drop\+table)'
check_pattern "XSS" '(<script|javascript:|onerror=)'
check_pattern "Directory Traversal" '(\.\./|%2e%2e)'
check_pattern "Sensitive File Access" '(\.env|\.git|\.htaccess|wp-admin|phpmyadmin)'
check_pattern "Scanner Activity" '(nikto|sqlmap|nmap|masscan)'
echo ""

# ─── Section 6: Top Requested Paths ──────────────────────────────────────────

echo -e "${BOLD}── 6. Top 10 Requested Paths ───────────────────────${NC}"
echo -e "\n## 6. Top Paths\n" >> "$OUTPUT_FILE"

awk '{print $7}' "$LOGFILE" | sort | uniq -c | sort -rn | head -10 | \
while read count path; do
    echo -e "  ${CYAN}$path${NC}  ($count)"
    echo "  $count  $path" >> "$OUTPUT_FILE"
done
echo ""

# ─── Section 7: Timeline for Most Active IP ───────────────────────────────────

echo -e "${BOLD}── 7. Timeline – Most Active IP ────────────────────${NC}"
echo -e "\n## 7. Timeline\n" >> "$OUTPUT_FILE"

TOP_IP=$(awk '{print $1}' "$LOGFILE" | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')
if [ -n "$TOP_IP" ]; then
    echo -e "  Tracing activity for: ${RED}$TOP_IP${NC}\n"
    echo "  IP: $TOP_IP" >> "$OUTPUT_FILE"
    grep "^$TOP_IP" "$LOGFILE" | awk '{print "  ["$4"]", $6, $7, "→", $9}' | tr -d '"[' | \
        tee -a "$OUTPUT_FILE"
fi
echo ""

# ─── Summary ─────────────────────────────────────────────────────────────────

echo -e "${GREEN}════════════════════════════════════════════${NC}"
echo -e "${GREEN}[+] Log Analysis Complete!${NC}"
echo -e "${GREEN}[+] Report: $OUTPUT_FILE${NC}"
echo -e "${GREEN}════════════════════════════════════════════${NC}"
