# Password Tools Cheat Sheet

> ⚠️ These tools are for EDUCATIONAL USE ONLY.
> Only use on systems you own or have explicit written permission to test.
> Never target real accounts or systems without authorisation.

---

## john (John the Ripper)

### Basic Usage

```bash
# Crack with wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Specify hash format
john --wordlist=wordlist.txt hashes.txt --format=raw-md5
john --wordlist=wordlist.txt hashes.txt --format=raw-sha1
john --wordlist=wordlist.txt hashes.txt --format=raw-sha256
john --wordlist=wordlist.txt hashes.txt --format=bcrypt

# Auto-detect format
john --wordlist=wordlist.txt hashes.txt

# Show cracked passwords
john --show hashes.txt
john --show --format=raw-md5 hashes.txt

# List all supported formats
john --list=formats
john --list=formats | grep MD5

# Brute force (no wordlist – slow)
john hashes.txt --incremental

# Rules (mangling)
john --wordlist=wordlist.txt hashes.txt --rules

# Restore interrupted session
john --restore

# Status check (while running, press any key)
```

### Hash File Format

```bash
# Format: username:hash
echo "admin:5f4dcc3b5aa765d61d8327deb882cf99" > hashes.txt    # MD5
echo "user1:482c811da5d5b4bc6d497ffa98491e38" >> hashes.txt    # MD5

# /etc/shadow format (Linux)
# username:$6$salt$hash:...
# john /etc/shadow   (run as root)

# /etc/passwd + /etc/shadow combined
unshadow /etc/passwd /etc/shadow > combined.txt
john --wordlist=rockyou.txt combined.txt
```

### Generate Sample Hashes

```bash
# MD5
echo -n "password123" | md5sum
# Output: 482c811da5d5b4bc6d497ffa98491e38

# SHA1
echo -n "password123" | sha1sum

# SHA256
echo -n "password123" | sha256sum

# Python – multiple algorithms
python3 -c "
import hashlib
pw = 'password123'
print('MD5:   ', hashlib.md5(pw.encode()).hexdigest())
print('SHA1:  ', hashlib.sha1(pw.encode()).hexdigest())
print('SHA256:', hashlib.sha256(pw.encode()).hexdigest())
"
```

---

## hydra

> ⚠️ ONLY use against localhost, your own DVWA, or explicitly authorised systems.

### Basic Syntax

```bash
hydra [options] <target> <protocol>
```

### Protocol Examples

```bash
# SSH brute force (localhost only)
hydra -l admin -P /usr/share/wordlists/rockyou.txt 127.0.0.1 ssh

# FTP
hydra -l admin -P passwords.txt 127.0.0.1 ftp

# HTTP Basic Auth
hydra -l admin -P passwords.txt target.com http-get /protected/

# HTTP POST form
hydra -l admin -P passwords.txt target.com \
  http-post-form "/login.php:user=^USER^&pass=^PASS^:Invalid credentials"

# HTTPS POST form
hydra -l admin -P passwords.txt -s 443 target.com \
  https-post-form "/login:user=^USER^&pass=^PASS^:Invalid"

# Telnet
hydra -l root -P passwords.txt 127.0.0.1 telnet

# MySQL
hydra -l root -P passwords.txt 127.0.0.1 mysql

# RDP
hydra -l administrator -P passwords.txt 127.0.0.1 rdp

# SMTP
hydra -l user@example.com -P passwords.txt mail.example.com smtp
```

### Key Flags

| Flag | Description |
|------|-------------|
| `-l <user>` | Single username |
| `-L <file>` | Username list |
| `-p <pass>` | Single password |
| `-P <file>` | Password list |
| `-t 4` | Threads (keep low to avoid lockout) |
| `-V` | Verbose – show each attempt |
| `-f` | Stop after first successful login |
| `-o <file>` | Save results to file |
| `-s <port>` | Custom port |
| `-e nsr` | Try null pass, same as username, reverse |
| `-w 30` | Wait 30 seconds between attempts |
| `-I` | Ignore existing restore file |

### DVWA Demo (local)

```bash
# First, get the PHPSESSID and security token
# Log into DVWA at http://127.0.0.1/dvwa/login.php with admin/password
# Then run:

hydra -l admin -P /usr/share/wordlists/rockyou.txt 127.0.0.1 \
  http-post-form \
  "/dvwa/login.php:username=^USER^&password=^PASS^&Login=Login:Login failed" \
  -V -t 4
```

---

## Wordlists

```bash
# Common wordlist locations
/usr/share/wordlists/rockyou.txt            # 14M passwords
/usr/share/wordlists/dirb/common.txt        # web dirs
/usr/share/wordlists/metasploit/            # Metasploit wordlists
/data/data/com.termux/files/usr/share/wordlists/  # Termux

# If rockyou.txt is compressed
gunzip /usr/share/wordlists/rockyou.txt.gz

# Create a small custom wordlist
cat > /tmp/wordlist.txt << 'EOF'
password
123456
admin
password123
qwerty
letmein
welcome
monkey
dragon
master
EOF

# Generate password mutations
echo "password" | john --stdout --rules
```

---

## hashcat (Alternative to john)

```bash
# If hashcat is available
# -m = hash type, -a = attack mode

# MD5 (-m 0) with wordlist (-a 0)
hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt

# SHA1 (-m 100)
hashcat -m 100 -a 0 hashes.txt wordlist.txt

# bcrypt (-m 3200)
hashcat -m 3200 -a 0 hashes.txt wordlist.txt

# Show results
hashcat -m 0 hashes.txt --show

# Hash type reference
# 0    = MD5
# 100  = SHA1
# 1400 = SHA256
# 1800 = sha512crypt (Linux shadow)
# 3200 = bcrypt
# 5500 = NetNTLMv1
# 5600 = NetNTLMv2
```
