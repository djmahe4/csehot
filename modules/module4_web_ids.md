# Module 4 – Web Services & IDS

> ⚠️ **LEGAL NOTICE:** Only scan web applications you own or have explicit written permission to test.
> Authorised targets: `testphp.vulnweb.com`, `http://localhost/dvwa`, local lab only.

---

## 4.1 Web Application Architecture

```
Browser ──HTTP──→ Web Server (Apache/Nginx)
                        │
                   App Layer (PHP/Python/Node)
                        │
                   Database (MySQL/PostgreSQL)
```

Understanding the stack helps identify attack vectors at each layer.

---

## 4.2 nikto – Web Vulnerability Scanner

`nikto` performs comprehensive web server tests, checking for:
- Outdated server software
- Dangerous files/scripts
- Misconfigurations
- Default files/credentials
- SSL/TLS issues

```bash
# Basic scan
nikto -h http://testphp.vulnweb.com

# Scan with specific port
nikto -h http://target -p 8080

# SSL scan
nikto -h https://target -ssl

# Save output
nikto -h http://testphp.vulnweb.com -o logs/module4/nikto.txt

# Scan with authentication
nikto -h http://target -id admin:password

# Tune scan (-T options)
# 0 – File upload
# 1 – Interesting files
# 2 – Misconfiguration
# 3 – Info disclosure
# 4 – XSS
# 5 – Remote file retrieval
# 6 – Denial of service
# 7 – Remote file retrieval (server-side)
# 8 – Command execution
nikto -h http://target -Tuning 4
```

---

## 4.3 gobuster – Directory & File Brute Force

`gobuster` discovers hidden directories, files, and virtual hosts.

```bash
# Directory brute force
gobuster dir -u http://testphp.vulnweb.com -w /usr/share/wordlists/dirb/common.txt

# With file extensions
gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt -x php,html,txt

# DNS subdomain enumeration
gobuster dns -d example.com -w /usr/share/wordlists/subdomains-top1million-5000.txt

# Virtual host discovery
gobuster vhost -u http://target -w /usr/share/wordlists/subdomains-top1million-5000.txt

# Common flags
# -u    target URL
# -w    wordlist path
# -x    file extensions
# -t    threads (default 10)
# -o    output file
# -s    valid status codes (default: 200,204,301,302,307,401,403)
# -v    verbose
gobuster dir -u http://testphp.vulnweb.com \
  -w /usr/share/wordlists/dirb/common.txt \
  -t 20 -o logs/module4/gobuster.txt
```

---

## 4.4 whatweb – Technology Fingerprinting

`whatweb` identifies web technologies: CMS, JavaScript frameworks, server software, analytics.

```bash
# Basic fingerprint
whatweb http://testphp.vulnweb.com

# Verbose output
whatweb -v http://testphp.vulnweb.com

# Aggression levels (1-4)
# 1 – stealthy (1 request)
# 3 – aggressive (more requests)
whatweb -a 3 http://target

# Scan multiple targets from file
whatweb -i targets.txt

# Output formats
whatweb --log-json=output.json http://target
whatweb --log-xml=output.xml http://target
```

---

## 4.5 OWASP Top 10 Web Vulnerabilities

| Rank | Vulnerability |
|------|--------------|
| A01 | Broken Access Control |
| A02 | Cryptographic Failures |
| A03 | Injection (SQLi, XSS, etc.) |
| A04 | Insecure Design |
| A05 | Security Misconfiguration |
| A06 | Vulnerable & Outdated Components |
| A07 | Identification & Authentication Failures |
| A08 | Software & Data Integrity Failures |
| A09 | Security Logging & Monitoring Failures |
| A10 | Server-Side Request Forgery (SSRF) |

---

## 4.6 Intrusion Detection Systems (IDS)

An **IDS** monitors network/system activity for malicious behaviour.

| Type | Description |
|------|-------------|
| **NIDS** | Network-based: monitors traffic |
| **HIDS** | Host-based: monitors system calls, logs |
| **Signature-based** | Matches known attack patterns |
| **Anomaly-based** | Detects deviations from baseline |

### Common IDS Tools
- **Snort** – open-source NIDS
- **Suricata** – high-performance NIDS/NIPS
- **OSSEC** – host-based IDS
- **Zeek (Bro)** – network analysis framework

---

## 4.7 tshark – Traffic Capture & Analysis

`tshark` is the terminal version of Wireshark.

```bash
# List available interfaces
tshark -D

# Capture packets on interface
tshark -i wlan0

# Capture to file
tshark -i wlan0 -w capture.pcap

# Read from file
tshark -r capture.pcap

# Filter: only HTTP traffic
tshark -i wlan0 -f "port 80"

# Display filter
tshark -r capture.pcap -Y "http.request"

# Show specific fields
tshark -r capture.pcap -T fields -e ip.src -e ip.dst -e http.request.uri

# Capture 50 packets and save
tshark -i lo -c 50 -w logs/module4/capture.pcap

# Detect suspicious patterns – many requests from one IP
tshark -r capture.pcap -T fields -e ip.src | sort | uniq -c | sort -rn | head -10
```

---

## 4.8 IDS Evasion Techniques (for awareness)

Security professionals should know how attackers evade IDS:

- **Fragmentation** – split packets across fragments
- **Encryption** – HTTPS hides payload from signature IDS
- **Slow scans** – `-T1` nmap timing avoids rate-based detection
- **Obfuscation** – encode payloads (Base64, URL encoding)
- **Decoy scans** – `nmap -D RND:10` sends scans from fake IPs

These techniques are covered so defenders can tune IDS rules accordingly.

---

## Key Takeaways

- Web scanners reveal misconfigurations and outdated components
- Directory brute forcing can uncover hidden admin panels
- Technology fingerprinting exposes the attack surface
- IDS is a key defensive layer – understand how it works and its limitations

---

*Next: [Module 5 – Digital Forensics](module5_forensics.md)*
