#!/usr/bin/env python3
"""
log_analyzer.py – Web traffic log analyzer
CGT 312 Ethical Hacking – Module 4 (IDS Simulation)

Analyses Apache/Nginx access logs to identify:
- Top IPs by request count
- Suspicious request patterns
- Potential attack signatures
- HTTP error rates

Usage:
    python log_analyzer.py [logfile]
    python log_analyzer.py labs/sample_access.log
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
LOG_DIR    = os.path.join(BASE_DIR, "logs", "module4")
SAMPLE_LOG = os.path.join(BASE_DIR, "labs", "sample_access.log")

# ─── Attack signature patterns ───────────────────────────────────────────────

SQLI_PATTERNS = re.compile(
    r"(%27|'|--|;|\bor\b\s+\d+=\d+|union\b.*\bselect\b|select\b.*\bfrom\b"
    r"|\bdrop\s+table\b|insert\b.*\binto\b|\bdelete\b.*\bfrom\b)",
    re.IGNORECASE
)

XSS_PATTERNS = re.compile(
    r"(<script|javascript:|onerror=|onload=|onfocus=|eval\(|alert\()",
    re.IGNORECASE
)

TRAVERSAL_PATTERNS = re.compile(
    r"(\.\./|%2e%2e|%252e%252e|\.\.\\|%2f\.\.)",
    re.IGNORECASE
)

SCANNER_PATTERNS = re.compile(
    r"(nikto|nmap|masscan|sqlmap|acunetix|nessus|openvas|burpsuite|zgrab)",
    re.IGNORECASE
)

SENSITIVE_PATHS = re.compile(
    r"(\.env|\.git|wp-admin|phpmyadmin|/admin|\.htaccess|\.htpasswd"
    r"|/etc/passwd|web\.config|\.bak|\.old|backup)",
    re.IGNORECASE
)

# ─── Apache log parser ────────────────────────────────────────────────────────

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+)\s+'          # IP address
    r'\S+\s+'                  # ident
    r'\S+\s+'                  # user
    r'\[(?P<time>[^\]]+)\]\s+' # timestamp
    r'"(?P<request>[^"]*?)"\s+' # request line
    r'(?P<status>\d{3})\s+'    # status code
    r'(?P<size>\S+)'           # bytes
)


def parse_line(line):
    """Parse a single Apache access log line."""
    m = LOG_PATTERN.match(line.strip())
    if not m:
        return None
    req = m.group("request").split()
    return {
        "ip":      m.group("ip"),
        "time":    m.group("time"),
        "method":  req[0] if len(req) > 0 else "-",
        "path":    req[1] if len(req) > 1 else "-",
        "status":  int(m.group("status")),
        "size":    m.group("size"),
        "raw":     line.strip()
    }


def analyze(logfile):
    """Analyse log file and return findings."""
    if not os.path.exists(logfile):
        print(f"{RED}[!] Log file not found: {logfile}{NC}")
        return None

    entries = []
    with open(logfile) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                parsed = parse_line(line)
                if parsed:
                    entries.append(parsed)

    if not entries:
        print(f"{YELLOW}[!] No parseable entries found.{NC}")
        return None

    # ── Aggregate statistics ──────────────────────────────────────────────

    ip_counts    = Counter(e["ip"] for e in entries)
    status_codes = Counter(e["status"] for e in entries)
    paths        = Counter(e["path"] for e in entries)
    methods      = Counter(e["method"] for e in entries)

    # ── Per-IP 4xx error counts (brute force detection) ───────────────────

    ip_4xx = defaultdict(int)
    ip_401 = defaultdict(int)
    for e in entries:
        if 400 <= e["status"] < 500:
            ip_4xx[e["ip"]] += 1
        if e["status"] == 401:
            ip_401[e["ip"]] += 1

    # ── Attack pattern detection ──────────────────────────────────────────

    alerts = []
    for e in entries:
        path = e["path"]
        if SQLI_PATTERNS.search(path):
            alerts.append({
                "type": "SQL Injection",
                "ip": e["ip"],
                "path": path,
                "time": e["time"],
                "status": e["status"]
            })
        if XSS_PATTERNS.search(path):
            alerts.append({
                "type": "XSS",
                "ip": e["ip"],
                "path": path,
                "time": e["time"],
                "status": e["status"]
            })
        if TRAVERSAL_PATTERNS.search(path):
            alerts.append({
                "type": "Directory Traversal",
                "ip": e["ip"],
                "path": path,
                "time": e["time"],
                "status": e["status"]
            })
        if SCANNER_PATTERNS.search(e.get("raw", "")):
            alerts.append({
                "type": "Scanner Detected",
                "ip": e["ip"],
                "path": path,
                "time": e["time"],
                "status": e["status"]
            })
        if SENSITIVE_PATHS.search(path):
            alerts.append({
                "type": "Sensitive Path Access",
                "ip": e["ip"],
                "path": path,
                "time": e["time"],
                "status": e["status"]
            })

    # ── Brute force detection (>5 failures) ──────────────────────────────

    brute_force_ips = {ip: cnt for ip, cnt in ip_401.items() if cnt >= 5}

    return {
        "total_entries": len(entries),
        "ip_counts": ip_counts,
        "status_codes": status_codes,
        "top_paths": paths,
        "methods": methods,
        "ip_4xx": ip_4xx,
        "ip_401": ip_401,
        "brute_force_ips": brute_force_ips,
        "alerts": alerts
    }


def print_report(results, logfile):
    """Print formatted analysis report."""
    print(f"\n{CYAN}{'='*60}{NC}")
    print(f"{CYAN}  LOG ANALYSIS REPORT{NC}")
    print(f"{CYAN}  File: {logfile}{NC}")
    print(f"{CYAN}  Analyzed: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{NC}")
    print(f"{CYAN}{'='*60}{NC}\n")

    r = results

    print(f"{BOLD}── Summary ─────────────────────────────────────────{NC}")
    print(f"  Total entries:    {r['total_entries']}")
    print(f"  Unique IPs:       {len(r['ip_counts'])}")
    print(f"  Alert count:      {len(r['alerts'])}")
    print(f"  Brute force IPs:  {len(r['brute_force_ips'])}\n")

    print(f"{BOLD}── Top IPs by Request Count ────────────────────────{NC}")
    for ip, cnt in r["ip_counts"].most_common(10):
        bar = "█" * min(cnt, 30)
        fail = r["ip_4xx"].get(ip, 0)
        flag = f" {RED}⚠ {fail} errors{NC}" if fail > 5 else ""
        print(f"  {ip:<20} {cnt:>5} reqs  {CYAN}{bar}{NC}{flag}")
    print()

    print(f"{BOLD}── HTTP Status Codes ───────────────────────────────{NC}")
    for code, cnt in sorted(r["status_codes"].items()):
        colour = GREEN if code < 300 else YELLOW if code < 400 else RED
        print(f"  {colour}{code}{NC}: {cnt}")
    print()

    print(f"{BOLD}── HTTP Methods ────────────────────────────────────{NC}")
    for method, cnt in r["methods"].most_common():
        print(f"  {method:<8} {cnt}")
    print()

    if r["brute_force_ips"]:
        print(f"{RED}── ⚠ Brute Force Detected ──────────────────────────{NC}")
        for ip, cnt in sorted(r["brute_force_ips"].items(), key=lambda x: -x[1]):
            print(f"  {RED}✘ {ip:<20} {cnt} failed login attempts{NC}")
        print()

    if r["alerts"]:
        print(f"{RED}── ⚠ Attack Alerts ──────────────────────────────────{NC}")
        seen = set()
        for alert in r["alerts"]:
            key = (alert["type"], alert["ip"])
            if key not in seen:
                seen.add(key)
                print(f"  {RED}[{alert['type']}]{NC} IP: {alert['ip']} | Path: {alert['path'][:50]}")
        print()
    else:
        print(f"{GREEN}── ✔ No attack patterns detected ───────────────────{NC}\n")

    print(f"{BOLD}── Top Requested Paths ─────────────────────────────{NC}")
    for path, cnt in r["top_paths"].most_common(10):
        print(f"  {cnt:>5}  {path[:60]}")
    print()


def save_report(results, logfile):
    """Save report to logs/module4."""
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(LOG_DIR, f"{timestamp}_log_analysis.json")

    # Convert Counter objects for JSON serialization
    serializable = {
        "total_entries": results["total_entries"],
        "ip_counts": dict(results["ip_counts"].most_common(20)),
        "status_codes": dict(results["status_codes"]),
        "brute_force_ips": results["brute_force_ips"],
        "alerts": results["alerts"],
        "analyzed_file": logfile,
        "timestamp": timestamp
    }
    with open(report_path, "w") as f:
        json.dump(serializable, f, indent=2)
    print(f"{GREEN}[+] Report saved: {report_path}{NC}")


def main():
    logfile = sys.argv[1] if len(sys.argv) > 1 else SAMPLE_LOG

    # Create sample log if needed
    if not os.path.exists(logfile):
        print(f"{YELLOW}[!] Log file not found: {logfile}{NC}")
        print(f"{YELLOW}[*] Run 'python cli.py' → Module 5 to generate a sample log.{NC}")
        sys.exit(1)

    print(f"{CYAN}[*] Analyzing: {logfile}{NC}")
    results = analyze(logfile)
    if results:
        print_report(results, logfile)
        save_report(results, logfile)


if __name__ == "__main__":
    main()
