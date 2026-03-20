# Module 2 – Footprinting & Scanning

> ⚠️ **LEGAL NOTICE:** Only scan systems you own or have explicit written permission to test.
> Authorised public targets: `scanme.nmap.org`, `testphp.vulnweb.com`, localhost.

---

## 2.1 Footprinting

**Footprinting** (reconnaissance) is the first phase of ethical hacking – collecting as much information as possible about a target before launching any tests.

### Passive Reconnaissance (no direct contact)
- Google Dorking
- WHOIS lookups
- DNS records
- Social media / OSINT
- Shodan / Censys

### Active Reconnaissance (direct contact)
- Ping sweeps
- Port scanning
- Banner grabbing
- DNS zone transfer attempts

---

## 2.2 WHOIS Lookup

`whois` queries domain registration databases:

```bash
whois example.com
whois 93.184.216.34   # Reverse WHOIS on IP
```

**What you learn:** registrant name, registrar, name servers, creation/expiry dates.

---

## 2.3 DNS Enumeration

DNS (Domain Name System) maps domains to IPs. Key record types:

| Record | Purpose |
|--------|---------|
| A | IPv4 address |
| AAAA | IPv6 address |
| MX | Mail server |
| NS | Name server |
| TXT | Text (SPF, DKIM, etc.) |
| CNAME | Alias |

```bash
dig scanme.nmap.org ANY +short       # All records
dig scanme.nmap.org A                # IPv4 address
dig scanme.nmap.org MX               # Mail servers
nslookup scanme.nmap.org             # Simple lookup
dnsenum scanme.nmap.org              # Enumeration tool
```

---

## 2.4 nmap – Network Mapper

`nmap` is the industry-standard network scanner. It discovers hosts, open ports, services, and OS details.

### Basic Scan Types

| Flag | Purpose |
|------|---------|
| (none) | TCP SYN scan (default) |
| `-sS` | Stealth SYN scan |
| `-sT` | TCP connect scan |
| `-sU` | UDP scan |
| `-sV` | Version detection |
| `-sC` | Default scripts |
| `-O`  | OS detection |
| `-A`  | Aggressive (sV + sC + O + traceroute) |
| `-p-` | Scan ALL 65535 ports |
| `-p 22,80,443` | Specific ports |
| `--top-ports 100` | Top 100 common ports |

### Output Formats

```bash
nmap -oN output.txt target      # Normal text
nmap -oX output.xml target      # XML
nmap -oG output.gnmap target    # Greppable
nmap -oA output target          # All formats
```

### Timing Templates

| Flag | Speed | Use Case |
|------|-------|---------|
| `-T0` | Paranoid | IDS evasion |
| `-T1` | Sneaky | IDS evasion |
| `-T3` | Normal | Default |
| `-T4` | Aggressive | Fast scan |
| `-T5` | Insane | Very fast |

### Common Scan Examples

```bash
# Basic scan
nmap scanme.nmap.org

# Service version + default scripts
nmap -sV -sC scanme.nmap.org

# OS detection (requires root/sudo)
sudo nmap -O scanme.nmap.org

# Full aggressive scan
sudo nmap -A -T4 scanme.nmap.org

# Scan entire subnet
nmap 192.168.1.0/24

# Ping sweep (discover live hosts)
nmap -sn 192.168.1.0/24

# Scan specific ports
nmap -p 21,22,80,443,3306 scanme.nmap.org

# Save output
nmap -sV -oN logs/module2/scan.txt scanme.nmap.org
```

---

## 2.5 Banner Grabbing

Banner grabbing reveals software versions from service banners:

```bash
# Using netcat
nc scanme.nmap.org 80
# Then type: HEAD / HTTP/1.0  (press Enter twice)

# Using curl
curl -I http://scanme.nmap.org

# Using nmap scripts
nmap -sV --script=banner scanme.nmap.org
```

---

## 2.6 Identifying Attack Surface

After scanning, identify:

1. **Open ports** – each open port is a potential entry point
2. **Running services** – check for known CVEs
3. **OS version** – unpatched OS has known exploits
4. **Outdated software** – e.g., Apache 2.2, PHP 5.x

Tools to check CVEs:
- `searchsploit <service>`
- `https://cve.mitre.org`
- `https://nvd.nist.gov`

---

## 2.7 Network Scan Workflow

```
[Start]
   │
   ├─→ WHOIS + DNS Enumeration (passive)
   │
   ├─→ Ping Sweep: nmap -sn 192.168.x.0/24
   │
   ├─→ Port Scan: nmap -sV -sC <target>
   │
   ├─→ OS Detection: nmap -O <target>
   │
   ├─→ Banner Grab: nc / curl
   │
   └─→ Document attack surface → /logs/module2/
```

---

## Key Takeaways

- Passive recon leaves no traces; active recon does
- nmap is your primary scanning tool
- Always save outputs for analysis and reporting
- Understand what each open port means for risk

---

*Next: [Module 3 – Attacks (Safe Demo)](module3_attacks.md)*
