# nmap Command Cheat Sheet

> ⚠️ Only scan systems you own or have explicit written permission to test.
> Authorised targets: `scanme.nmap.org`, `127.0.0.1`, your own lab network.

---

## Basic Syntax

```bash
nmap [flags] <target>
# target can be: IP, hostname, CIDR, range (192.168.1.1-50)
```

---

## Scan Types

| Command | Description |
|---------|-------------|
| `nmap <target>` | Default TCP SYN scan (top 1000 ports) |
| `nmap -sS <target>` | Stealth SYN scan (requires root) |
| `nmap -sT <target>` | Full TCP connect scan |
| `nmap -sU <target>` | UDP scan |
| `nmap -sN <target>` | Null scan |
| `nmap -sF <target>` | FIN scan |
| `nmap -sX <target>` | Xmas scan |
| `nmap -sA <target>` | ACK scan (firewall detection) |
| `nmap -sn <target>` | Ping sweep (no port scan) |
| `nmap -Pn <target>` | Skip host discovery |

---

## Port Specification

| Command | Description |
|---------|-------------|
| `nmap -p 22 <target>` | Single port |
| `nmap -p 22,80,443 <target>` | Multiple ports |
| `nmap -p 1-1024 <target>` | Port range |
| `nmap -p- <target>` | All 65535 ports |
| `nmap --top-ports 100 <target>` | Top 100 common ports |
| `nmap --top-ports 1000 <target>` | Top 1000 common ports |

---

## Detection & Enumeration

| Command | Description |
|---------|-------------|
| `nmap -sV <target>` | Service version detection |
| `nmap -sC <target>` | Default scripts |
| `nmap -O <target>` | OS detection (requires root) |
| `nmap -A <target>` | Aggressive (sV + sC + O + traceroute) |
| `nmap --version-intensity 9 <target>` | Maximum version intensity |

---

## Timing Templates

| Flag | Name | Speed |
|------|------|-------|
| `-T0` | Paranoid | Extremely slow, IDS evasion |
| `-T1` | Sneaky | Slow, IDS evasion |
| `-T2` | Polite | Slow, low bandwidth |
| `-T3` | Normal | Default |
| `-T4` | Aggressive | Fast (recommended for labs) |
| `-T5` | Insane | Very fast, may miss results |

---

## Output Formats

| Command | Description |
|---------|-------------|
| `nmap -oN output.txt <target>` | Normal text output |
| `nmap -oX output.xml <target>` | XML output |
| `nmap -oG output.gnmap <target>` | Greppable output |
| `nmap -oA output <target>` | All three formats |
| `nmap -v <target>` | Verbose output |
| `nmap -vv <target>` | Very verbose |

---

## Scripting Engine (NSE)

```bash
# Run default scripts
nmap -sC <target>

# Run a specific script
nmap --script=banner <target>
nmap --script=http-title <target>
nmap --script=ssh-hostkey <target>

# Run script category
nmap --script=vuln <target>         # vulnerability scripts
nmap --script=auth <target>         # authentication checks
nmap --script=discovery <target>    # discovery scripts
nmap --script=exploit <target>      # ⚠ exploitation scripts

# List all scripts
ls /usr/share/nmap/scripts/ | grep http
```

---

## Useful Combinations

```bash
# Quick scan of local network
nmap -sn 192.168.1.0/24

# Comprehensive scan of a target
sudo nmap -A -T4 -p- scanme.nmap.org

# Service scan with output saved
nmap -sV -sC scanme.nmap.org -oN logs/module2/scan.txt

# Scan with NSE vuln scripts
nmap --script=vuln testphp.vulnweb.com

# Firewall/IDS evasion (educational purposes)
nmap -f <target>                    # fragment packets
nmap -D RND:10 <target>             # decoy scan
nmap --source-port 53 <target>      # spoof source port

# Scan from a file of targets
nmap -iL targets.txt

# Banner grabbing
nmap -sV --script=banner <target>
```

---

## Reading nmap Output

```
PORT     STATE    SERVICE  VERSION
22/tcp   open     ssh      OpenSSH 6.6.1p1
80/tcp   open     http     Apache httpd 2.4.7
443/tcp  filtered https
3306/tcp closed   mysql

States:
  open     – port is accepting connections
  closed   – port is reachable but no service
  filtered – port is blocked by firewall
```

---

## Quick Reference – Common Ports

| Port | Service |
|------|---------|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 110 | POP3 |
| 143 | IMAP |
| 443 | HTTPS |
| 445 | SMB |
| 3306 | MySQL |
| 3389 | RDP |
| 5432 | PostgreSQL |
| 8080 | HTTP Alt |
| 8443 | HTTPS Alt |
