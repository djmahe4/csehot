# Lab 4 – Web Services & IDS

> ⚠️ **LEGAL NOTICE:** Only scan web applications you own or have explicit written permission to test.
> Authorised targets for this lab: `testphp.vulnweb.com`, `localhost`, DVWA (self-hosted).

**Objective:** Use nikto, gobuster, and whatweb to assess a web application; capture and analyse traffic with tshark.

**Estimated Time:** 75 minutes

**Prerequisites:** nikto, gobuster, whatweb, tshark installed (run `bash setup.sh`)

---

## Task 1: Technology Fingerprinting with whatweb

```bash
# Basic fingerprint of authorised target
whatweb http://testphp.vulnweb.com

# Verbose output for detailed info
whatweb -v http://testphp.vulnweb.com

# Aggressive scan (more requests)
whatweb -a 3 http://testphp.vulnweb.com

# Save output
whatweb -v http://testphp.vulnweb.com > logs/module4/whatweb_testphp.txt
```

**Record findings:**
- Web Server: _______________
- CMS/Framework: ___________
- JavaScript Libraries: _____
- Programming Language: _____

---

## Task 2: Web Vulnerability Scan with nikto

```bash
# Basic nikto scan
nikto -h http://testphp.vulnweb.com

# Save output
nikto -h http://testphp.vulnweb.com -o logs/module4/nikto_testphp.txt

# Scan with specific tuning (information disclosure)
nikto -h http://testphp.vulnweb.com -Tuning 3

# Scan with verbose output
nikto -h http://testphp.vulnweb.com -Display 124
```

**Look for (check all that apply):**
- [ ] Outdated server software version
- [ ] Default files present (readme, changelog)
- [ ] Insecure HTTP methods (PUT, DELETE)
- [ ] Missing security headers
- [ ] Directory listing enabled
- [ ] Vulnerable scripts

---

## Task 3: Directory Brute Forcing with gobuster

```bash
# Check gobuster is available
gobuster version

# Directory scan (common wordlist)
gobuster dir \
  -u http://testphp.vulnweb.com \
  -w /usr/share/wordlists/dirb/common.txt \
  -t 20

# With file extensions
gobuster dir \
  -u http://testphp.vulnweb.com \
  -w /usr/share/wordlists/dirb/common.txt \
  -x php,html,txt,bak \
  -t 20

# Save output
gobuster dir \
  -u http://testphp.vulnweb.com \
  -w /usr/share/wordlists/dirb/common.txt \
  -o logs/module4/gobuster_testphp.txt

# If wordlist not found, try:
ls /usr/share/wordlists/
ls /data/data/com.termux/files/usr/share/wordlists/  # Termux path
```

**Record discovered directories:**
```
/
/images/
/product/
...
```

---

## Task 4: HTTP Header Analysis

```bash
# Check security headers
curl -I http://testphp.vulnweb.com

# Check for HTTPS redirect
curl -I http://testphp.vulnweb.com -L

# Check specific headers with grep
curl -I http://testphp.vulnweb.com | grep -iE "server|x-frame|x-xss|strict|content-security"
```

**Security Header Checklist:**
| Header | Present | Value |
|--------|---------|-------|
| X-Frame-Options | | |
| X-XSS-Protection | | |
| Strict-Transport-Security | | |
| Content-Security-Policy | | |
| X-Content-Type-Options | | |

---

## Task 5: Traffic Capture with tshark

```bash
# List network interfaces
tshark -D

# Capture traffic on loopback (safe, local only)
tshark -i lo -c 30 2>&1

# Capture and save to file
tshark -i lo -c 100 -w logs/module4/capture.pcap 2>&1

# Read capture file
tshark -r logs/module4/capture.pcap 2>&1 | head -30

# Filter HTTP traffic
tshark -r logs/module4/capture.pcap -Y "http" 2>&1 | head -20

# Show source/destination IPs
tshark -r logs/module4/capture.pcap \
  -T fields -e ip.src -e ip.dst -e tcp.dstport \
  2>&1 | sort | uniq -c | sort -rn | head -20
```

---

## Task 6: IDS Simulation – Detect Scan Patterns

```bash
# Capture traffic while running a scan (using background job control)
# Start capture in the background
tshark -i lo -c 500 -w /tmp/scan_capture.pcap 2>&1 &

# Run nmap against localhost (authorised)
nmap -sV localhost

# Wait for nmap to finish, then analyse capture
wait
tshark -r /tmp/scan_capture.pcap -Y "tcp.flags.syn==1" -T fields \
  -e ip.src -e ip.dst -e tcp.dstport 2>&1 | head -30

# Count SYN packets per destination port (port scan signature)
tshark -r /tmp/scan_capture.pcap -Y "tcp.flags.syn==1" \
  -T fields -e tcp.dstport 2>&1 | sort | uniq -c | sort -rn | head -20
```

**Observation:** A port scan generates many SYN packets to different ports – this pattern triggers IDS alerts.

---

## Task 7: Run Automated Scripts

```bash
# Run the web scan script
bash scripts/web_scan.sh

# Run the log analyser (analyses captured data)
python scripts/log_analyzer.py
```

---

## Task 8: Vulnerability Mapping

Based on your nikto and gobuster results, complete this vulnerability report:

| # | Tool | Finding | Severity | Recommendation |
|---|------|---------|----------|----------------|
| 1 | nikto | Outdated Apache version | High | Update to latest |
| 2 | gobuster | /admin/ accessible | High | Restrict access |
| 3 | whatweb | PHP version exposed | Medium | Hide version |
| ... | | | | |

---

## Completion Criteria

- [ ] Ran whatweb and recorded technology stack
- [ ] Ran nikto and identified at least 3 findings
- [ ] Ran gobuster and discovered hidden directories
- [ ] Checked HTTP security headers with curl
- [ ] Captured traffic with tshark
- [ ] Analysed capture to detect port scan pattern
- [ ] Completed vulnerability mapping table

**Mark complete:** Run `python cli.py` → Option 5 → `h`

---

*Next: [Lab 5 – Digital Forensics](lab5_forensics.md)*
