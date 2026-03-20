# Lab 2 – Footprinting & Scanning

> ⚠️ **LEGAL NOTICE:** Only scan authorised targets.
> Authorised targets for this lab: `scanme.nmap.org`, `localhost`/`127.0.0.1`
> Do NOT scan any other IP or domain without explicit written permission.

**Objective:** Perform passive and active reconnaissance using WHOIS, DNS tools, and nmap.

**Estimated Time:** 60 minutes

**Prerequisites:** nmap, whois, dig installed (run `bash setup.sh`)

---

## Task 1: Passive Reconnaissance – WHOIS

```bash
# Step 1: WHOIS domain lookup
whois scanme.nmap.org

# Record the following:
# - Registrar: ___________________
# - Creation Date: _______________
# - Name Servers: ________________
# - Registrant (if visible): _____
```

**Save output:**
```bash
whois scanme.nmap.org > logs/module2/whois_scanme.txt
```

---

## Task 2: DNS Enumeration

```bash
# A record (IPv4 address)
dig scanme.nmap.org A +short

# All records
dig scanme.nmap.org ANY +short

# Reverse DNS lookup (PTR)
dig -x 45.33.32.156 +short

# Name server records
dig scanme.nmap.org NS +short

# Save DNS info
dig scanme.nmap.org ANY > logs/module2/dns_scanme.txt
```

**Record your findings:**
- IP Address: _______________
- Name Servers: _____________

---

## Task 3: Basic nmap Scan

```bash
# Basic TCP scan (top 1000 ports)
nmap scanme.nmap.org

# Record:
# - Open ports found: _______________________
# - Service names: __________________________
```

---

## Task 4: Service Version Detection

```bash
# Service version scan
nmap -sV scanme.nmap.org

# With default scripts
nmap -sV -sC scanme.nmap.org

# Save to log file
nmap -sV -sC scanme.nmap.org -oN logs/module2/nmap_svc_scanme.txt
```

**Fill in the table:**

| Port | State | Service | Version |
|------|-------|---------|---------|
| | | | |
| | | | |
| | | | |

---

## Task 5: OS Detection (requires root/sudo)

```bash
# OS detection
sudo nmap -O scanme.nmap.org

# Expected output includes:
# OS details: Linux 3.x or later
# or similar OS guess
```

---

## Task 6: Full Aggressive Scan

```bash
# Aggressive scan: version + scripts + OS + traceroute
sudo nmap -A -T4 scanme.nmap.org

# Save full output
sudo nmap -A -T4 scanme.nmap.org -oN logs/module2/nmap_full_scanme.txt
```

---

## Task 7: Local Network Scan (Your Own Network Only)

```bash
# Find your IP
ip addr show | grep inet

# Ping sweep – discover live hosts on your network
# Replace 192.168.1 with your actual subnet
nmap -sn 192.168.1.0/24

# Port scan localhost
nmap -sV localhost
nmap -sV 127.0.0.1

# Save
nmap -sn 192.168.1.0/24 -oN logs/module2/network_sweep.txt
```

---

## Task 8: Identify Attack Surface

Based on your scan results, complete this table:

| Port | Service | Version | Known Vulnerability | Risk Level |
|------|---------|---------|---------------------|-----------|
| 22 | SSH | OpenSSH X.X | Check CVEs | Medium |
| 80 | HTTP | Apache X.X | Check CVEs | Medium |
| 443 | HTTPS | | | |
| ... | | | | |

**Research CVEs:** https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=openssh

---

## Task 9: Using scan.sh and network_scan.py

```bash
# Run the automated scan script
bash scripts/scan.sh scanme.nmap.org

# Run the Python wrapper with logging
python scripts/network_scan.py scanme.nmap.org
```

---

## Sample nmap Output

```
Starting Nmap 7.94 ( https://nmap.org ) at 2024-03-20 10:00
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.15s latency).
Not shown: 995 closed tcp ports (reset)
PORT    STATE    SERVICE VERSION
22/tcp  open     ssh     OpenSSH 6.6.1p1 Ubuntu
80/tcp  open     http    Apache httpd 2.4.7
9929/tcp open    nping-echo  Nping echo
31337/tcp open   Elite?
Aggressive OS guesses: Linux 3.11-5.x (96%)
```

---

## Completion Criteria

- [ ] Completed WHOIS lookup and recorded registrar info
- [ ] Completed DNS enumeration (A, NS records found)
- [ ] Ran basic nmap scan, identified open ports
- [ ] Ran service version scan, filled port/version table
- [ ] Ran full aggressive scan, saved output
- [ ] Scanned localhost to see own open services
- [ ] Completed attack surface analysis table

**Mark complete:** Run `python cli.py` → Option 3 → `h`

---

*Next: [Lab 3 – Attacks (Safe Demo)](lab3_attacks.md)*
