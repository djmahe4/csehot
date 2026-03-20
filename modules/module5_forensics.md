# Module 5 – Digital Forensics

> ⚠️ **LEGAL NOTICE:** Forensic analysis should only be performed on systems you own or have
> explicit authorisation to investigate. Unauthorised access to logs or systems is illegal.

---

## 5.1 What is Digital Forensics?

**Digital forensics** is the process of collecting, preserving, analyzing, and reporting on digital evidence for investigative purposes.

### Forensics Phases

1. **Identification** – recognize potential evidence
2. **Preservation** – prevent alteration (chain of custody)
3. **Collection** – gather evidence systematically
4. **Analysis** – examine evidence for clues
5. **Presentation** – report findings clearly

---

## 5.2 Log Analysis – The Foundation

Logs record system and application activity. Key log types:

| Log Type | Location (Linux) | Contents |
|----------|-----------------|----------|
| Auth log | `/var/log/auth.log` | SSH, sudo, login attempts |
| Syslog | `/var/log/syslog` | General system events |
| Apache access | `/var/log/apache2/access.log` | Web requests |
| Apache error | `/var/log/apache2/error.log` | Server errors |
| Nginx access | `/var/log/nginx/access.log` | Web requests |
| Kernel log | `/var/log/kern.log` | Kernel events |

### Apache Access Log Format (Combined Log Format)
```
%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"
```

**Example:**
```
192.168.1.100 - admin [20/Mar/2024:10:00:01 +0000] "GET /index.php HTTP/1.1" 200 4523 "-" "Mozilla/5.0"
│             │  │     │                            │   │                     │    │
IP           Ident User Timestamp                   Req Status                Size Referrer
```

---

## 5.3 grep – Pattern Matching

```bash
# Find all 404 errors
grep " 404 " /var/log/apache2/access.log

# Find all requests from a specific IP
grep "^192.168.1.100" access.log

# Case-insensitive search
grep -i "sql" access.log

# Count matching lines
grep -c " 401 " access.log

# Show line numbers
grep -n "POST /admin" access.log

# Multiple patterns (OR)
grep -E "401|403|500" access.log

# Find SQL injection attempts
grep -E "(\%27|\'|--|;|union|select|insert|drop)" access.log -i

# Find directory traversal attempts
grep -E "\.\./|%2e%2e%2f" access.log -i

# Find XSS attempts
grep -E "(<script|javascript:|onerror=)" access.log -i
```

---

## 5.4 awk – Field Processing

```bash
# Print only IP addresses (column 1)
awk '{print $1}' access.log

# Print IP and status code
awk '{print $1, $9}' access.log

# Filter by status code
awk '$9 == "401" {print}' access.log

# Count requests per IP
awk '{print $1}' access.log | sort | uniq -c | sort -rn

# Find large responses (>10000 bytes)
awk '$10 > 10000 {print $1, $7, $10}' access.log

# Extract request URLs
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -20
```

---

## 5.5 Detecting Brute-Force Attacks

A brute-force attack generates many failed login attempts from the same IP.

```bash
# Count 401 responses per IP
grep " 401 " access.log | awk '{print $1}' | sort | uniq -c | sort -rn

# Flag IPs with more than 10 failed attempts
awk '$9 == "401" {print $1}' access.log | sort | uniq -c | sort -rn | awk '$1 > 10'

# Find rapid sequential requests (potential automated attack)
awk '{print $4, $1}' access.log | sort | uniq -c | sort -rn | head -20

# SSH brute force in auth.log
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn
```

---

## 5.6 Timeline Reconstruction

```bash
# Show all events in time order for a suspect IP
grep "10.0.0.5" access.log | awk '{print $4, $6, $7, $9}' | sort

# Events between two times
awk '$4 >= "[20/Mar/2024:10:00" && $4 <= "[20/Mar/2024:10:05"' access.log

# Count requests per minute
awk '{print $4}' access.log | cut -d: -f2,3 | sort | uniq -c
```

---

## 5.7 Identifying Suspicious Patterns

### SQL Injection Signs in Logs
```
/index.php?id=1 UNION SELECT
/search?q=' OR '1'='1
/login?user=admin'--
```

### Directory Traversal Signs
```
GET /../../../etc/passwd
GET /%2e%2e/%2e%2e/etc/passwd
```

### Scanner Signatures
```bash
# Detect nikto scans
grep -i "nikto" access.log

# Detect sqlmap
grep -i "sqlmap" access.log

# Detect nmap HTTP scripts
grep -i "nmap" access.log
```

---

## 5.8 sort & uniq Commands

```bash
# Sort alphabetically
sort file.txt

# Sort numerically
sort -n file.txt

# Sort in reverse
sort -r file.txt

# Count unique occurrences
sort file.txt | uniq -c

# Show only duplicates
sort file.txt | uniq -d

# Show only unique lines
sort file.txt | uniq -u

# Combined pipeline: top IPs
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -20
```

---

## 5.9 Forensics Workflow

```
[Suspicious Activity Reported]
         │
         ├─→ Identify affected logs
         │
         ├─→ Preserve logs (copy before analysis)
         │         cp access.log /tmp/evidence_$(date +%s).log
         │
         ├─→ Extract suspect IPs
         │         grep " 401 " access.log | awk '{print $1}' | sort -u
         │
         ├─→ Timeline reconstruction
         │         grep "<suspect_ip>" access.log | sort
         │
         ├─→ Identify attack type (SQLi, brute force, traversal)
         │
         ├─→ Determine impact (what was accessed?)
         │
         └─→ Generate report → /reports/
```

---

## Key Takeaways

- Logs are the primary evidence source in digital forensics
- grep + awk + sort + uniq form a powerful analysis toolkit
- Brute force attacks generate distinctive patterns in logs
- Preserve logs before analysis to maintain chain of custody
- Document findings in a structured report

---

*End of module notes. See [Lab 5](../labs/lab5_forensics.md) for hands-on practice.*
