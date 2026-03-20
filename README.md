# CGT 312 – Ethical Hacking Lab
## Termux-Based Practical Learning Environment

> ⚠️ **LEGAL NOTICE:** This repository is for **educational purposes only**.
> Only test systems you **own** or have **explicit written permission** to test.
> Unauthorized use of these tools is illegal and unethical.

---

## Overview

This repository provides a complete, structured learning environment for the **CGT 312 Ethical Hacking** course. It is designed to run entirely inside **Termux** (Android) or any Linux terminal, using real industry-standard tools mapped directly to the course syllabus.

```
Core Tools: nmap · sqlmap · hydra · nikto · john · netcat · gobuster · whatweb · tshark
```

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/djmahe4/csehot.git
cd csehot

# 2. Install all tools (Termux or Linux)
bash setup.sh

# 3. Launch the interactive CLI
python cli.py
```

---

## Repository Structure

```
csehot/
│
├── cli.py                  ← Interactive CLI launcher (main entry point)
├── setup.sh                ← Auto-install all tools
├── progress.json           ← Lab completion tracker
├── README.md               ← This file
│
├── modules/                ← Theory notes (one Markdown file per module)
│   ├── module1_fundamentals.md
│   ├── module2_footprinting.md
│   ├── module3_attacks.md
│   ├── module4_web_ids.md
│   └── module5_forensics.md
│
├── labs/                   ← Step-by-step guided lab exercises
│   ├── lab1_fundamentals.md
│   ├── lab2_scanning.md
│   ├── lab3_attacks.md
│   ├── lab4_web_ids.md
│   ├── lab5_forensics.md
│   └── sample_access.log   ← Sample web log for forensics lab
│
├── commands/               ← Categorized command cheat sheets
│   ├── nmap_cheatsheet.md
│   ├── web_tools_cheatsheet.md
│   ├── password_tools_cheatsheet.md
│   └── forensics_cheatsheet.md
│
├── scripts/                ← Automation scripts
│   ├── scan.sh             ← Automated nmap multi-phase scan
│   ├── network_scan.py     ← nmap wrapper with JSON+text logging
│   ├── password_lab.sh     ← john hash cracking lab
│   ├── sqlmap_runner.sh    ← sqlmap demo against authorized target
│   ├── web_scan.sh         ← whatweb + nikto + gobuster + header analysis
│   ├── log_analyzer.py     ← Apache log analysis with attack detection
│   ├── log_parser.sh       ← Bash forensics log parser
│   └── anomaly_detector.py ← Statistical anomaly detection + IOC extraction
│
├── logs/                   ← Auto-saved scan/analysis outputs
│   ├── module1/ … module5/
│
└── reports/                ← User-generated findings
    └── template.md         ← Penetration testing report template
```

---

## CLI Menu

```
╔══════════════════════════════════════════════╗
║        CGT 312 Ethical Hacking Lab           ║
║          Termux Learning Environment         ║
╠══════════════════════════════════════════════╣
║  1. Setup Environment                        ║
║  2. Module 1: Fundamentals                   ║
║  3. Module 2: Footprinting & Scanning        ║
║  4. Module 3: Attacks (Safe Practice)        ║
║  5. Module 4: Web Services & IDS             ║
║  6. Module 5: Forensics                      ║
║  7. Run Full Lab Workflow                    ║
║  8. View Logs / Reports                      ║
║  9. CTF Challenges                           ║
║  0. Exit                                     ║
╚══════════════════════════════════════════════╝
```

Each option:
- Displays relevant commands and theory
- Runs scripts where applicable
- Saves all output to `/logs/<module>/`
- Tracks completion in `progress.json`

---

## Module Summary

| Module | Topic | Key Tools |
|--------|-------|-----------|
| 1 | Security Fundamentals | bash /dev/tcp, netcat |
| 2 | Footprinting & Scanning | nmap, whois, dig |
| 3 | Attacks (Safe Demo) | john, hydra, sqlmap |
| 4 | Web Services & IDS | nikto, gobuster, whatweb, tshark |
| 5 | Digital Forensics | grep, awk, sort, uniq |

---

## Module 1: Security Fundamentals

**Topics:** CIA Triad, Threat Actors, OSI/TCP-IP model, Legal frameworks

```bash
# Lab: Check open ports using bash built-ins (no tools needed)
(echo >/dev/tcp/scanme.nmap.org/80) 2>/dev/null \
  && echo "Port 80 OPEN" || echo "Port 80 CLOSED"
```

→ See [`modules/module1_fundamentals.md`](modules/module1_fundamentals.md)
→ See [`labs/lab1_fundamentals.md`](labs/lab1_fundamentals.md)

---

## Module 2: Footprinting & Scanning

**Focus:** The strongest module – full reconnaissance workflow

```bash
# Authorized target: scanme.nmap.org
whois scanme.nmap.org
dig scanme.nmap.org ANY +short
nmap -sV -sC -O scanme.nmap.org

# Automated scan with logging
bash scripts/scan.sh scanme.nmap.org
python scripts/network_scan.py scanme.nmap.org
```

→ See [`modules/module2_footprinting.md`](modules/module2_footprinting.md)
→ See [`labs/lab2_scanning.md`](labs/lab2_scanning.md)
→ See [`commands/nmap_cheatsheet.md`](commands/nmap_cheatsheet.md)

---

## Module 3: Attacks (Safe Demo Only)

> ⚠️ **ONLY on localhost, DVWA, or explicitly authorized systems.**

```bash
# Crack sample MD5 hashes with john
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
john --show hashes.txt

# sqlmap on authorized test site
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --batch --dbs

# Run lab scripts
bash scripts/password_lab.sh
bash scripts/sqlmap_runner.sh
```

→ See [`modules/module3_attacks.md`](modules/module3_attacks.md)
→ See [`labs/lab3_attacks.md`](labs/lab3_attacks.md)
→ See [`commands/password_tools_cheatsheet.md`](commands/password_tools_cheatsheet.md)

---

## Module 4: Web Services & IDS

```bash
# Technology fingerprint
whatweb -v http://testphp.vulnweb.com

# Vulnerability scan
nikto -h http://testphp.vulnweb.com

# Directory brute force
gobuster dir -u http://testphp.vulnweb.com -w /usr/share/wordlists/dirb/common.txt

# Traffic capture
tshark -i lo -c 30

# Run all web scans and save logs
bash scripts/web_scan.sh
```

→ See [`modules/module4_web_ids.md`](modules/module4_web_ids.md)
→ See [`labs/lab4_web_ids.md`](labs/lab4_web_ids.md)
→ See [`commands/web_tools_cheatsheet.md`](commands/web_tools_cheatsheet.md)

---

## Module 5: Forensics

```bash
# Analyze access log
awk '{print $1}' labs/sample_access.log | sort | uniq -c | sort -rn

# Detect brute-force attempts
awk '$9 == "401" {print $1}' labs/sample_access.log | sort | uniq -c | sort -rn

# Run automated analysis
bash scripts/log_parser.sh
python scripts/anomaly_detector.py
python scripts/log_analyzer.py
```

→ See [`modules/module5_forensics.md`](modules/module5_forensics.md)
→ See [`labs/lab5_forensics.md`](labs/lab5_forensics.md)
→ See [`commands/forensics_cheatsheet.md`](commands/forensics_cheatsheet.md)

---

## Setup Script

```bash
bash setup.sh
```

**Installs:**
- Core: `git`, `curl`, `wget`, `nmap`, `python`, `pip`
- Attack simulation: `hydra`, `sqlmap`, `nikto`, `whatweb`, `john`
- Network: `netcat`, `tshark`
- Optional (prompted): `gobuster` (via Go), `metasploit` (heavy, Termux)

Works on both Termux (Android) and standard Linux.

---

## Logging System

All scan and analysis outputs are automatically saved:

```
logs/
├── module1/    YYYY-MM-DD_HH-MM-SS.txt
├── module2/    YYYY-MM-DD_HH-MM-SS.txt  (+ .json for network_scan.py)
├── module3/    YYYY-MM-DD_HH-MM-SS.txt
├── module4/    YYYY-MM-DD_HH-MM-SS.json
└── module5/    YYYY-MM-DD_HH-MM-SS.txt  (+ .json for anomaly_detector.py)
```

---

## Progress Tracker

`progress.json` tracks module completion and score:

```json
{
  "module1": {"completed": true, "score": 10, "timestamp": "2024-03-20T10:00:00"},
  "module2": {"completed": false, "score": 0, "timestamp": null},
  ...
}
```

View current progress via `python cli.py` → Option 8.

---

## CTF Challenges

The CLI includes 5 CTF-style questions (Option 9) covering:
- CIA Triad definitions
- nmap flag meanings
- HTTP status codes
- Password cracking tools
- Common service ports

Score your knowledge before and after completing the modules.

---

## Authorized Test Targets

| Target | Authorized By | Use |
|--------|-------------|-----|
| `scanme.nmap.org` | Nmap Project (official) | Network scanning |
| `testphp.vulnweb.com` | Acunetix (official) | Web app testing, SQLi demo |
| `127.0.0.1` / `localhost` | Self (you own it) | All modules |
| DVWA (self-hosted) | Self (you host it) | Password, SQLi labs |
| HackTheBox / TryHackMe | Platform (with account) | CTF practice |

> **Never** scan or test any other IP, domain, or system without explicit written permission.

---

## Safety & Ethics

Every module, script, and lab includes:
- Clear ethical use warnings
- Explicit statement of authorized targets only
- Guidance on applicable laws (IT Act 2000, CFAA)
- Defensive mitigations alongside offensive techniques

The philosophy: **understand attacks to build better defenses**.

---

## License

This repository is for **educational use only** under the CGT 312 course framework.
All tool usage must comply with applicable laws and the ethical guidelines stated throughout.
