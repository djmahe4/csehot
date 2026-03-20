#!/bin/bash
# =============================================================================
# password_lab.sh – Password cracking lab script
# CGT 312 Ethical Hacking – Module 3
# =============================================================================
# LEGAL NOTICE: ONLY use on your own systems / sample hashes provided.
# Never run against real accounts or systems without explicit written permission.
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
echo "║  ⚠  ETHICAL USE WARNING – MODULE 3                  ║"
echo "║                                                      ║"
echo "║  Password cracking ONLY on:                         ║"
echo "║  • Your own hash files                              ║"
echo "║  • Sample hashes provided in this lab               ║"
echo "║  • Your local DVWA / test systems                   ║"
echo "║                                                      ║"
echo "║  NEVER target real accounts without permission.     ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}[*] Password Lab – Module 3${NC}"
echo -e "${CYAN}[*] Timestamp: $TIMESTAMP${NC}\n"

LOG_FILE="$LOG_DIR/${TIMESTAMP}_password_lab.txt"
{
    echo "# CGT 312 Password Lab"
    echo "# Timestamp: $TIMESTAMP"
    echo "# ─────────────────────────────────────────────────"
} > "$LOG_FILE"

# ─── Step 1: Create sample hashes ────────────────────────────────────────────

echo -e "${GREEN}[Step 1] Creating sample MD5 hash file...${NC}"
HASH_FILE="/tmp/cgt312_lab_hashes.txt"
cat > "$HASH_FILE" << 'EOF'
# Sample hashes for CGT 312 lab (MD5)
# Format: username:md5hash
user1:482c811da5d5b4bc6d497ffa98491e38
user2:5f4dcc3b5aa765d61d8327deb882cf99
user3:25f9e794323b453885f5181f1b624d0b
user4:e10adc3949ba59abbe56e057f20f883e
EOF

echo -e "  Hash file: $HASH_FILE"
cat "$HASH_FILE"
echo -e "\n  ${YELLOW}These are MD5 hashes of common passwords.${NC}\n"

echo -e "## Step 1: Sample Hashes\n$(cat "$HASH_FILE")\n" >> "$LOG_FILE"

# ─── Step 2: Create mini wordlist (if rockyou.txt not available) ──────────────

echo -e "${GREEN}[Step 2] Checking wordlist availability...${NC}"
WORDLIST=""

# Search common wordlist locations
for wl in \
    /usr/share/wordlists/rockyou.txt \
    /data/data/com.termux/files/usr/share/wordlists/rockyou.txt \
    /usr/share/john/password.lst; do
    if [ -f "$wl" ]; then
        WORDLIST="$wl"
        echo -e "  ${GREEN}Found: $wl${NC}"
        break
    fi
done

if [ -z "$WORDLIST" ]; then
    echo -e "  ${YELLOW}rockyou.txt not found – creating mini wordlist${NC}"
    WORDLIST="/tmp/mini_wordlist.txt"
    cat > "$WORDLIST" << 'EOF'
password
123456
password123
123456789
qwerty
abc123
letmein
monkey
1234567890
dragon
master
hello
welcome
admin
root
test
shadow
12345678
1234
superman
batman
EOF
    echo -e "  ${GREEN}Mini wordlist created: $WORDLIST${NC}"
fi
echo ""

echo -e "## Step 2: Wordlist\n$WORDLIST\n" >> "$LOG_FILE"

# ─── Step 3: Crack with john ──────────────────────────────────────────────────

echo -e "${GREEN}[Step 3] Cracking hashes with john...${NC}"

if ! command -v john &>/dev/null; then
    echo -e "  ${YELLOW}john not found – skipping hash cracking.${NC}"
    echo -e "  Install with: pkg install john${NC}"
else
    echo -e "  ${CYAN}\$ john --format=raw-md5 --wordlist=$WORDLIST $HASH_FILE${NC}"
    echo -e "\n## Step 3: John Output\n" >> "$LOG_FILE"

    john --format=raw-md5 --wordlist="$WORDLIST" "$HASH_FILE" 2>&1 | tee -a "$LOG_FILE"

    echo ""
    echo -e "${GREEN}[Step 3b] Showing cracked passwords:${NC}"
    echo -e "  ${CYAN}\$ john --show $HASH_FILE${NC}"
    echo -e "\n## Step 3b: Cracked Passwords\n" >> "$LOG_FILE"
    john --show "$HASH_FILE" 2>&1 | tee -a "$LOG_FILE"
fi
echo ""

# ─── Step 4: Hash generation demo ────────────────────────────────────────────

echo -e "${GREEN}[Step 4] Hash generation examples...${NC}"
echo -e "\n## Step 4: Hash Generation\n" >> "$LOG_FILE"

if command -v python3 &>/dev/null || command -v python &>/dev/null; then
    PY=$(command -v python3 || command -v python)
    HASH_DEMO=$($PY -c "
import hashlib
passwords = ['password', 'password123', 'P@ssw0rd!']
for p in passwords:
    md5 = hashlib.md5(p.encode()).hexdigest()
    sha1 = hashlib.sha1(p.encode()).hexdigest()
    sha256 = hashlib.sha256(p.encode()).hexdigest()
    print(f'Password: {p}')
    print(f'  MD5:    {md5}')
    print(f'  SHA1:   {sha1}')
    print(f'  SHA256: {sha256}')
    print()
")
    echo "$HASH_DEMO"
    echo "$HASH_DEMO" >> "$LOG_FILE"
fi

# ─── Step 5: Summary ─────────────────────────────────────────────────────────

echo -e "${GREEN}════════════════════════════════════════════${NC}"
echo -e "${GREEN}[+] Password Lab Complete!${NC}"
echo -e "${GREEN}[+] Log saved: $LOG_FILE${NC}"
echo -e "${GREEN}════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Key takeaways:${NC}"
echo -e "  • MD5 is broken – all 4 hashes cracked quickly"
echo -e "  • Common passwords are cracked in seconds"
echo -e "  • Use bcrypt or Argon2 for password storage"
echo -e "  • Enforce password complexity and length"
