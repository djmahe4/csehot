# Module 1 – Security Fundamentals & Ethics

> ⚠️ **LEGAL NOTICE:** This module is for educational purposes only.
> Always act within the law and with explicit authorisation.

---

## 1.1 What is Ethical Hacking?

**Ethical hacking** (also called **penetration testing** or **white-hat hacking**) is the practice of deliberately probing systems, networks, and applications with authorisation to identify security weaknesses before malicious actors do.

| Type | Colour | Behaviour |
|------|--------|-----------|
| Ethical hacker | White Hat | Authorised, reports findings |
| Malicious hacker | Black Hat | Unauthorised, criminal intent |
| Grey-area hacker | Grey Hat | May act without permission but disclose issues |

---

## 1.2 The CIA Triad

The **CIA Triad** is the foundation of information security:

```
         Confidentiality
              /\
             /  \
            /    \
    Integrity — Availability
```

| Property | Definition | Attack Example |
|----------|-----------|----------------|
| **Confidentiality** | Only authorised parties can access data | Data breach, eavesdropping |
| **Integrity** | Data is accurate and unmodified | Man-in-the-middle, tampering |
| **Availability** | Systems are accessible when needed | DoS/DDoS attacks |

---

## 1.3 Types of Threats

- **Malware** – viruses, worms, ransomware, spyware
- **Phishing** – social engineering via deceptive emails/sites
- **SQL Injection** – inserting malicious SQL into input fields
- **Cross-Site Scripting (XSS)** – injecting scripts into web pages
- **Brute Force** – systematically trying all password combinations
- **DoS / DDoS** – overwhelming a system to deny service
- **Man-in-the-Middle (MitM)** – intercepting communication
- **Zero-Day** – exploiting unknown/unpatched vulnerabilities

---

## 1.4 Legal & Ethical Framework

### Key Laws (India / Global)

| Law | Relevance |
|-----|-----------|
| **IT Act 2000 (India)** | Sections 43, 66, 66C – unauthorised computer access |
| **CFAA (USA)** | Computer Fraud and Abuse Act |
| **GDPR (EU)** | Data protection and privacy |

### The Golden Rule
> **Never test a system you do not own or do not have explicit written permission to test.**

### Authorised Target List for this Course
- `scanme.nmap.org` – officially permitted by Nmap Project
- `testphp.vulnweb.com` – officially permitted by Acunetix
- `127.0.0.1` / `localhost` – your own machine
- DVWA, Metasploitable, HackTheBox (with account)

---

## 1.5 OSI Model & Attack Mapping

| Layer | Name | Protocol Examples | Common Attacks |
|-------|------|------------------|----------------|
| 7 | Application | HTTP, FTP, DNS | SQLi, XSS, Phishing |
| 6 | Presentation | SSL/TLS, JPEG | SSL stripping |
| 5 | Session | NetBIOS, RPC | Session hijacking |
| 4 | Transport | TCP, UDP | SYN flood, port scan |
| 3 | Network | IP, ICMP | IP spoofing, routing attacks |
| 2 | Data Link | Ethernet, ARP | ARP poisoning |
| 1 | Physical | Cables, Wi-Fi | Hardware tapping |

---

## 1.6 TCP/IP vs OSI

```
OSI Model           TCP/IP Model
─────────────────   ─────────────
Application   ┐
Presentation  ├──→  Application
Session       ┘
Transport     ────→  Transport
Network       ────→  Internet
Data Link     ┐
Physical      ┴──→  Network Access
```

---

## 1.7 Attack Phases (Ethical Hacking Methodology)

1. **Reconnaissance** – gather info passively/actively
2. **Scanning** – identify live hosts, open ports, services
3. **Enumeration** – extract detailed info (users, shares)
4. **Exploitation** – gain access using found vulnerabilities
5. **Post-Exploitation** – maintain access, pivot
6. **Reporting** – document findings and mitigations

---

## Key Takeaways

- Ethics and legality are non-negotiable
- CIA Triad underpins all security decisions
- Understand the OSI model to understand where attacks occur
- Always work within scope and with permission

---

*Next: [Module 2 – Footprinting & Scanning](module2_footprinting.md)*
