#!/usr/bin/env python3
"""
anomaly_detector.py – Statistical anomaly detection in web server logs
CGT 312 Ethical Hacking – Module 5

Detects:
- IP-based anomalies (unusual request volumes)
- Brute-force login patterns
- SQL injection signatures
- Directory traversal attempts
- Scanner tool signatures
- Suspicious time-of-day patterns

Usage:
    python anomaly_detector.py [logfile]
    python anomaly_detector.py labs/sample_access.log
"""

import os
import sys
import re
import json
import datetime
from collections import defaultdict, Counter

# ─── Colours ─────────────────────────────────────────────────────────────────

RED    = "\033[0;31m"
GREEN  = "\033[0;32m"
YELLOW = "\033[1;33m"
CYAN   = "\033[0;36m"
BOLD   = "\033[1m"
NC     = "\033[0m"

# ─── Paths ───────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR   = os.path.dirname(SCRIPT_DIR)
LOG_DIR    = os.path.join(BASE_DIR, "logs", "module5")
SAMPLE_LOG = os.path.join(BASE_DIR, "labs", "sample_access.log")

# ─── Log parser ──────────────────────────────────────────────────────────────

LOG_RE = re.compile(
    r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<time>[^\]]+)\]\s+'
    r'"(?P<request>[^"]*?)"\s+(?P<status>\d{3})\s+(?P<size>\S+)'
)

TIME_RE = re.compile(r'(\d{2})/(\w+)/(\d{4}):(\d{2}):(\d{2}):(\d{2})')

MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}

ATTACK_SIGNATURES = {
    "SQL Injection": re.compile(
        r"(%27|'--|\bOR\b\s+\d+=\d+|\bUNION\b.*\bSELECT\b"
        r"|\bDROP\b\s+\bTABLE\b|\bINSERT\b|\bDELETE\b\s+\bFROM\b)",
        re.IGNORECASE
    ),
    "XSS": re.compile(
        r"(<script|javascript:|onerror=|onload=|eval\(|alert\()",
        re.IGNORECASE
    ),
    "Directory Traversal": re.compile(
        r"(\.\./|%2e%2e|\.\.\\)",
        re.IGNORECASE
    ),
    "Scanner": re.compile(
        r"(nikto|sqlmap|nmap|masscan|acunetix|nessus|openvas|burp)",
        re.IGNORECASE
    ),
    "Sensitive File": re.compile(
        r"(\.env|\.git/|\.htaccess|wp-config|phpmyadmin|/admin"
        r"|\.bak|backup\.sql|\.htpasswd|/etc/passwd)",
        re.IGNORECASE
    ),
}


def parse_log(logfile):
    """Parse access log, return list of entry dicts."""
    entries = []
    with open(logfile) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = LOG_RE.match(line)
            if not m:
                continue
            req = m.group("request").split()
            tm  = TIME_RE.search(m.group("time"))
            ts  = None
            if tm:
                try:
                    ts = datetime.datetime(
                        int(tm.group(3)),
                        MONTHS.get(tm.group(2), 1),
                        int(tm.group(1)),
                        int(tm.group(4)),
                        int(tm.group(5)),
                        int(tm.group(6))
                    )
                except ValueError:
                    pass
            entries.append({
                "ip":      m.group("ip"),
                "time":    m.group("time"),
                "ts":      ts,
                "method":  req[0] if req else "-",
                "path":    req[1] if len(req) > 1 else "-",
                "status":  int(m.group("status")),
                "raw":     line
            })
    return entries


def detect_anomalies(entries):
    """Run all anomaly detectors and return findings."""
    findings = []

    ip_requests  = Counter(e["ip"] for e in entries)
    ip_errors    = defaultdict(list)
    ip_timelines = defaultdict(list)

    for e in entries:
        if e["status"] >= 400:
            ip_errors[e["ip"]].append(e)
        if e["ts"]:
            ip_timelines[e["ip"]].append(e["ts"])

    # ── 1. High request volume ────────────────────────────────────────────

    avg = sum(ip_requests.values()) / len(ip_requests) if ip_requests else 1
    threshold = max(avg * 3, 10)
    for ip, count in ip_requests.most_common():
        if count >= threshold:
            findings.append({
                "severity": "MEDIUM",
                "type":     "High Request Volume",
                "ip":       ip,
                "detail":   f"{count} requests (threshold: {threshold:.0f})",
                "evidence": []
            })

    # ── 2. Brute force (many 401/403) ────────────────────────────────────

    for ip, errors in ip_errors.items():
        auth_fails = [e for e in errors if e["status"] in (401, 403)]
        if len(auth_fails) >= 5:
            findings.append({
                "severity": "HIGH",
                "type":     "Brute Force Attempt",
                "ip":       ip,
                "detail":   f"{len(auth_fails)} authentication failures",
                "evidence": [e["raw"] for e in auth_fails[:3]]
            })

    # ── 3. Attack signature matching ─────────────────────────────────────

    per_ip_attacks = defaultdict(lambda: defaultdict(list))
    for e in entries:
        for attack_name, pattern in ATTACK_SIGNATURES.items():
            if pattern.search(e["path"]) or pattern.search(e["raw"]):
                per_ip_attacks[e["ip"]][attack_name].append(e)

    for ip, attacks in per_ip_attacks.items():
        for attack_type, attack_entries in attacks.items():
            findings.append({
                "severity": "HIGH",
                "type":     attack_type,
                "ip":       ip,
                "detail":   f"{len(attack_entries)} matching request(s)",
                "evidence": [e["raw"] for e in attack_entries[:2]]
            })

    # ── 4. Rapid sequential requests (rate-based) ─────────────────────────

    for ip, times in ip_timelines.items():
        if len(times) < 10:
            continue
        times_sorted = sorted(times)
        # Check if >10 requests within 10 seconds
        for i in range(len(times_sorted) - 9):
            window = (times_sorted[i + 9] - times_sorted[i]).total_seconds()
            if window < 10:
                findings.append({
                    "severity": "MEDIUM",
                    "type":     "Rapid Request Rate",
                    "ip":       ip,
                    "detail":   f"10 requests in {window:.1f}s",
                    "evidence": []
                })
                break

    return findings


def generate_ioc_list(findings):
    """Extract Indicators of Compromise."""
    iocs = {
        "suspicious_ips": list({f["ip"] for f in findings}),
        "attack_types": list({f["type"] for f in findings}),
        "high_severity": [f for f in findings if f["severity"] == "HIGH"],
    }
    return iocs


def print_findings(findings, entries):
    """Pretty-print anomaly findings."""
    print(f"\n{CYAN}{'='*65}{NC}")
    print(f"{CYAN}  ANOMALY DETECTION REPORT{NC}")
    print(f"{CYAN}  Analyzed: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{NC}")
    print(f"{CYAN}  Total log entries: {len(entries)}{NC}")
    print(f"{CYAN}{'='*65}{NC}\n")

    if not findings:
        print(f"{GREEN}  ✔ No anomalies detected.{NC}\n")
        return

    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    findings_sorted = sorted(findings, key=lambda x: severity_order.get(x["severity"], 3))

    print(f"{BOLD}Findings ({len(findings)} total):{NC}\n")

    for i, f in enumerate(findings_sorted, 1):
        colour = RED if f["severity"] == "HIGH" else YELLOW
        print(f"  {colour}[{f['severity']}] #{i} {f['type']}{NC}")
        print(f"         IP:     {f['ip']}")
        print(f"         Detail: {f['detail']}")
        if f.get("evidence"):
            print(f"         Evidence:")
            for ev in f["evidence"][:2]:
                print(f"           {ev[:80]}")
        print()

    iocs = generate_ioc_list(findings)
    print(f"{BOLD}── Indicators of Compromise (IOCs) ─────────────────{NC}")
    print(f"  Suspicious IPs:  {', '.join(iocs['suspicious_ips'])}")
    print(f"  Attack types:    {', '.join(iocs['attack_types'])}")
    print()

    print(f"{BOLD}── Recommendations ─────────────────────────────────{NC}")
    for ip in iocs["suspicious_ips"]:
        print(f"  • Block IP: {ip} in firewall / .htaccess")
    if any(f["type"] == "SQL Injection" for f in findings):
        print("  • Implement parameterised queries / WAF rules for SQLi")
    if any(f["type"] == "Brute Force Attempt" for f in findings):
        print("  • Enable account lockout / CAPTCHA after 5 failed attempts")
    if any(f["type"] == "Directory Traversal" for f in findings):
        print("  • Validate and sanitise all file path inputs")
    print()


def save_report(findings, entries):
    """Save structured report to logs/module5."""
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(LOG_DIR, f"{timestamp}_anomaly_report.json")

    iocs = generate_ioc_list(findings)
    report = {
        "timestamp": timestamp,
        "total_entries": len(entries),
        "findings_count": len(findings),
        "iocs": {
            "suspicious_ips": iocs["suspicious_ips"],
            "attack_types": iocs["attack_types"]
        },
        "findings": findings
    }
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"{GREEN}[+] Report saved: {report_path}{NC}")


def main():
    logfile = sys.argv[1] if len(sys.argv) > 1 else SAMPLE_LOG

    if not os.path.exists(logfile):
        print(f"{RED}[!] Log file not found: {logfile}{NC}")
        print(f"{YELLOW}    Run: python cli.py → Option 6 → b to generate sample log.{NC}")
        sys.exit(1)

    print(f"{CYAN}[*] Anomaly Detector: {logfile}{NC}")
    entries = parse_log(logfile)

    if not entries:
        print(f"{YELLOW}[!] No parseable log entries found.{NC}")
        sys.exit(1)

    print(f"{CYAN}[*] Parsed {len(entries)} log entries{NC}")
    findings = detect_anomalies(entries)
    print_findings(findings, entries)
    save_report(findings, entries)


if __name__ == "__main__":
    main()
