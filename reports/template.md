# Penetration Testing / Forensics Report

**Report Date:** ___________________
**Prepared By:** ___________________
**Course:** CGT 312 Ethical Hacking

---

## 1. Executive Summary

> Brief plain-language description of what was found.

_Summary here..._

---

## 2. Scope & Authorisation

| Item | Detail |
|------|--------|
| **Target** | (e.g. scanme.nmap.org / testphp.vulnweb.com / localhost) |
| **Authorisation** | (e.g. Nmap Project / Acunetix / Self-owned) |
| **Date of Test** | |
| **Duration** | |
| **Tester** | |

---

## 3. Tools Used

| Tool | Version | Purpose |
|------|---------|---------|
| nmap | | Network scanning |
| nikto | | Web vulnerability scanning |
| gobuster | | Directory brute forcing |
| whatweb | | Technology fingerprinting |
| sqlmap | | SQL injection testing |
| john | | Password hash cracking |
| hydra | | Login brute forcing |
| tshark | | Traffic capture/analysis |

---

## 4. Findings

### 4.1 Network Findings

| Port | Service | Version | Risk | Notes |
|------|---------|---------|------|-------|
| | | | | |
| | | | | |

### 4.2 Web Application Findings

| # | Type | Location | Severity | Detail |
|---|------|----------|----------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### 4.3 Authentication Findings

| # | Finding | Location | Severity |
|---|---------|----------|----------|
| 1 | | | |

### 4.4 Log / Forensics Findings (Module 5)

| # | Finding | Evidence | Attacker IP | Timeline |
|---|---------|----------|-------------|---------|
| 1 | | | | |

---

## 5. Risk Ratings

| Severity | Count |
|----------|-------|
| Critical | |
| High | |
| Medium | |
| Low | |
| Info | |

---

## 6. Recommendations

| # | Finding | Recommendation | Priority |
|---|---------|---------------|---------|
| 1 | Outdated Apache | Update to latest stable version | High |
| 2 | SQL Injection | Use parameterised queries, WAF | Critical |
| 3 | Missing security headers | Add X-Frame-Options, CSP, HSTS | Medium |
| 4 | Weak passwords | Enforce complexity, length ≥12, MFA | High |
| 5 | Directory listing | Disable Options Indexes in Apache | Medium |

---

## 7. Attack Timeline (Forensics)

```
Time                 IP              Event
─────────────────────────────────────────────────────────
[YYYY-MM-DD HH:MM]   X.X.X.X         First request
[YYYY-MM-DD HH:MM]   X.X.X.X         Reconnaissance
[YYYY-MM-DD HH:MM]   X.X.X.X         Attack commenced
[YYYY-MM-DD HH:MM]   X.X.X.X         Successful access
```

---

## 8. Indicators of Compromise (IOCs)

| Type | Value | Source |
|------|-------|--------|
| IP Address | | access.log |
| User Agent | | access.log |
| URL Pattern | | access.log |

---

## 9. Conclusion

_Overall assessment and final notes..._

---

## 10. Appendices

### Appendix A – Raw Scan Outputs
> See `/logs/` directory for full outputs.

### Appendix B – Evidence Screenshots
> Attach screenshots here.

---

*Report generated using CGT 312 Ethical Hacking Lab – csehot*
