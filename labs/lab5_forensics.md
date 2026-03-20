# Lab 5 – Digital Forensics

> ⚠️ **LEGAL NOTICE:** Only analyze logs from systems you own or have explicit written permission to investigate.

**Objective:** Analyze a simulated Apache access log to identify attacker IPs, attack types, and timeline.

**Estimated Time:** 60 minutes

**Prerequisites:** bash, grep, awk, sort, python3 installed

---

## The Scenario

You are the security analyst for a web application. An alert fired at 10:05 AM on 20 March 2024.
Your task is to analyze `labs/sample_access.log` to:
1. Identify the attacking IP(s)
2. Determine the attack type(s)
3. Reconstruct the attack timeline
4. Assess the impact
5. Write a findings report

---

## Task 1: Setup – Create Sample Log

The CLI auto-creates a sample log, or run:

```bash
# View the sample log
cat labs/sample_access.log

# If it doesn't exist yet, run the CLI or create it:
python cli.py   # Option 6 → b
```

**Sample Log Content:**
```
192.168.1.100 - - [20/Mar/2024:10:00:01 +0000] "GET / HTTP/1.1" 200 1234
10.0.0.5 - - [20/Mar/2024:10:00:05 +0000] "GET /admin HTTP/1.1" 401 512
10.0.0.5 - - [20/Mar/2024:10:00:06 +0000] "POST /admin/login HTTP/1.1" 401 512
10.0.0.5 - - [20/Mar/2024:10:00:07 +0000] "POST /admin/login HTTP/1.1" 401 512
...
10.0.0.5 - - [20/Mar/2024:10:02:06 +0000] "POST /admin/login HTTP/1.1" 200 1024
```

---

## Task 2: Initial Log Overview

```bash
# Count total log entries
wc -l labs/sample_access.log

# Show all unique IPs
awk '{print $1}' labs/sample_access.log | sort -u

# Count requests per IP
awk '{print $1}' labs/sample_access.log | sort | uniq -c | sort -rn

# Show all unique HTTP methods used
awk '{print $6}' labs/sample_access.log | tr -d '"' | sort -u

# Show all unique status codes
awk '{print $9}' labs/sample_access.log | sort -u
```

**Record:**
- Total entries: ____
- Unique IPs: _______
- Most active IP: ___

---

## Task 3: Detect Brute-Force Attack

```bash
# Count 401 Unauthorized responses per IP
grep " 401 " labs/sample_access.log | awk '{print $1}' | sort | uniq -c | sort -rn

# Flag IPs with > 3 failed attempts
awk '$9 == "401" {print $1}' labs/sample_access.log | \
  sort | uniq -c | sort -rn | awk '$1 > 3 {print "SUSPECTED BRUTE FORCE:", $2, "("$1" attempts)"}'

# Show all activity from the suspicious IP
grep "10.0.0.5" labs/sample_access.log
```

**Questions:**
1. Which IP is brute forcing? ____________
2. How many failed attempts? ____________
3. Did the attack succeed (200 response)? ____

---

## Task 4: Detect SQL Injection Attempts

```bash
# Search for common SQLi patterns
grep -iE "(\%27|'|--|union|select|insert|drop|or\+1)" labs/sample_access.log

# URL-encoded patterns
grep -iE "(\%3D|\%27|\%22|\%3B)" labs/sample_access.log

# Check IP of attacker
grep -iE "(union|select|insert|drop|or\+1)" labs/sample_access.log | awk '{print $1}' | sort -u
```

---

## Task 5: Detect Reconnaissance

```bash
# Find requests to sensitive files
grep -iE "(robots\.txt|\.git|\.env|wp-admin|phpmyadmin|\.bak)" labs/sample_access.log

# Find directory traversal attempts
grep -iE "(\.\./|%2e%2e)" labs/sample_access.log

# Find scanner signatures
grep -iE "(nikto|sqlmap|nmap|masscan|zgrab)" labs/sample_access.log
```

---

## Task 6: Timeline Reconstruction

```bash
# Full timeline for suspect IP 10.0.0.5
grep "10.0.0.5" labs/sample_access.log | awk '{print $4, $6, $7, $9}' | tr -d '['

# Full timeline for all IPs, sorted by time
sort -t[ -k2 labs/sample_access.log | awk '{print $4, $1, $6, $7, $9}'

# Time range of attack
grep "10.0.0.5" labs/sample_access.log | awk '{print $4}' | head -1
grep "10.0.0.5" labs/sample_access.log | awk '{print $4}' | tail -1
```

**Timeline:**
```
Time              IP          Action                  Status
[10:00:05]   10.0.0.5    GET /admin                   401
[10:00:06]   10.0.0.5    POST /admin/login             401
...
[10:02:06]   10.0.0.5    POST /admin/login             200  ← SUCCESS
```

---

## Task 7: Automated Analysis Scripts

```bash
# Run the log parser script
bash scripts/log_parser.sh

# Run the anomaly detector
python scripts/anomaly_detector.py

# Save analysis results
bash scripts/log_parser.sh > logs/module5/log_analysis.txt
```

---

## Task 8: Write Forensics Report

Use the report template:

```bash
# Copy template
cp reports/template.md reports/lab5_forensics_report.md

# Fill in your findings using a text editor
# or view the template
cat reports/template.md
```

**Required Report Sections:**
1. **Executive Summary** – what happened in plain language
2. **Timeline** – chronological events
3. **Attacker IP** – with evidence
4. **Attack Types** – brute force, SQLi, recon?
5. **Impact Assessment** – was the attack successful?
6. **Indicators of Compromise (IOCs)** – IPs, patterns, user agents
7. **Recommendations** – how to prevent this in future

---

## Answer Key (Do NOT peek before trying!)

<details>
<summary>Click to reveal answers</summary>

**Attacking IP:** `10.0.0.5`
- 7 failed login attempts to `/admin/login` (401)
- 1 successful login at 10:02:06 (200)
- This is a **brute-force attack** that succeeded

**SQLi attacker:** `192.168.1.200`
- Tried: `GET /index.php?id=1 OR 1=1` → returned 500 error
- SQL injection attempt detected

**Reconnaissance:** `172.16.0.99`
- Accessed `/robots.txt` → mapping site structure
- Tried `/.git/config` → looking for exposed Git repository

**Recommendations:**
- Block IP `10.0.0.5` (or all 3 attacker IPs)
- Implement account lockout after 5 failed attempts
- Enable WAF rules for SQLi patterns
- Remove `.git` directory from web root
- Monitor logs with automated alerting

</details>

---

## Completion Criteria

- [ ] Counted total log entries and unique IPs
- [ ] Detected brute-force attack IP
- [ ] Detected SQL injection attempt IP
- [ ] Detected reconnaissance activity
- [ ] Reconstructed complete attack timeline
- [ ] Ran automated log parser and anomaly detector
- [ ] Completed forensics report

**Mark complete:** Run `python cli.py` → Option 6 → `g`

---

*Congratulations! You have completed all 5 modules. Try the CTF Challenges in Option 9.*
