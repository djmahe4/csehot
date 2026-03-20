# Lab 1 – Security Fundamentals

> ⚠️ **LEGAL NOTICE:** This lab uses only localhost. No external systems are scanned.

**Objective:** Understand the CIA Triad, OSI model attack mapping, and use bash to check open ports.

**Estimated Time:** 30 minutes

**Prerequisites:** Termux or Linux terminal, bash

---

## Task 1: CIA Triad Mapping Exercise

For each scenario, identify which CIA property is violated:

| Scenario | CIA Property Violated |
|----------|----------------------|
| An attacker intercepts your HTTPS traffic | ? |
| A ransomware encrypts all your files | ? |
| A DDoS attack takes down a website | ? |
| A hacker modifies database records | ? |
| An insider leaks confidential employee data | ? |

**Answers:**
1. Confidentiality
2. Confidentiality + Availability
3. Availability
4. Integrity
5. Confidentiality

---

## Task 2: OSI Attack Mapping

Match each attack to its OSI layer:

| Attack | OSI Layer |
|--------|-----------|
| ARP Poisoning | ? |
| SQL Injection | ? |
| SYN Flood | ? |
| IP Spoofing | ? |
| SSL Stripping | ? |

**Answers:** Data Link (2), Application (7), Transport (4), Network (3), Presentation (6)

---

## Task 3: Port Check with /dev/tcp (Bash Built-in)

This technique requires NO external tools – just bash.

```bash
# Check if a port is open (works on any bash system)
# Syntax: /dev/tcp/<host>/<port>

# Check if port 80 is open on scanme.nmap.org
(echo >/dev/tcp/scanme.nmap.org/80) 2>/dev/null \
  && echo "Port 80 OPEN" \
  || echo "Port 80 CLOSED"

# Check SSH port
(echo >/dev/tcp/scanme.nmap.org/22) 2>/dev/null \
  && echo "Port 22 OPEN" \
  || echo "Port 22 CLOSED"

# Script to check multiple ports
#!/bin/bash
HOST="scanme.nmap.org"
PORTS=(21 22 25 80 443 3306 8080)

echo "Port scan of $HOST using /dev/tcp"
echo "────────────────────────────────"
for port in "${PORTS[@]}"; do
  (echo >/dev/tcp/$HOST/$port) 2>/dev/null \
    && echo "  [OPEN]   Port $port" \
    || echo "  [closed] Port $port"
done
```

**Expected Output (partial):**
```
Port scan of scanme.nmap.org using /dev/tcp
────────────────────────────────
  [closed] Port 21
  [OPEN]   Port 22
  [closed] Port 25
  [OPEN]   Port 80
  [OPEN]   Port 443
```

---

## Task 4: Banner Grab with netcat

```bash
# Connect to a web server and grab the HTTP banner
nc scanme.nmap.org 80
# After connecting, type: HEAD / HTTP/1.0
# Then press Enter twice

# Expected output:
# HTTP/1.1 200 OK
# Server: Apache/2.4.x (Ubuntu)
# Date: ...
```

---

## Task 5: Reflection Questions

Answer these in your report:

1. What is the difference between an ethical hacker and a malicious hacker?
2. Name three authorised targets you can legally scan for this course.
3. Which OSI layer does nmap primarily operate at?
4. What does `/dev/tcp` represent in bash?
5. Why is it important to log all scan activities?

---

## Completion Criteria

- [ ] Completed CIA Triad mapping table
- [ ] Completed OSI attack mapping table
- [ ] Successfully ran the /dev/tcp port check script
- [ ] Captured at least one HTTP banner with netcat
- [ ] Answered all 5 reflection questions

**Mark complete:** Run `python cli.py` → Option 2 → `c`

---

*Next: [Lab 2 – Footprinting & Scanning](lab2_scanning.md)*
