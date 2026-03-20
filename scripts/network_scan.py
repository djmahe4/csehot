#!/usr/bin/env python3
"""
network_scan.py – nmap wrapper with structured logging
CGT 312 Ethical Hacking – Module 2

Usage:
    python network_scan.py <target>
    python network_scan.py scanme.nmap.org
    python network_scan.py 127.0.0.1

LEGAL NOTICE: Only scan systems you own or have explicit written permission to test.
"""

import sys
import os
import subprocess
import datetime
import json

# ─── Colours ─────────────────────────────────────────────────────────────────

RED    = "\033[0;31m"
GREEN  = "\033[0;32m"
YELLOW = "\033[1;33m"
CYAN   = "\033[0;36m"
NC     = "\033[0m"

# ─── Paths ───────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR   = os.path.dirname(SCRIPT_DIR)
LOG_DIR    = os.path.join(BASE_DIR, "logs", "module2")


def warn():
    print(f"{RED}")
    print("╔══════════════════════════════════════════════╗")
    print("║  ⚠  ETHICAL USE WARNING                     ║")
    print("║  Only scan systems you own or have written  ║")
    print("║  permission to test.                        ║")
    print("╚══════════════════════════════════════════════╝")
    print(f"{NC}")


def run_nmap(target, flags, label):
    """Run nmap with given flags and return output."""
    cmd = f"nmap {flags} {target}"
    print(f"{CYAN}[*] {label}{NC}")
    print(f"{YELLOW}$ {cmd}{NC}\n")
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=180
        )
        output = result.stdout + result.stderr
        print(output)
        return {"command": cmd, "output": output}
    except subprocess.TimeoutExpired:
        msg = "[!] Command timed out after 180 seconds."
        print(f"{RED}{msg}{NC}")
        return {"command": cmd, "output": msg}
    except Exception as e:
        msg = f"[!] Error: {e}"
        print(f"{RED}{msg}{NC}")
        return {"command": cmd, "output": msg}


def parse_open_ports(nmap_output):
    """Extract open port information from nmap output."""
    ports = []
    for line in nmap_output.splitlines():
        # Match lines like: 22/tcp   open  ssh     OpenSSH 6.6.1
        if "/tcp" in line or "/udp" in line:
            parts = line.split()
            if len(parts) >= 3 and parts[1] == "open":
                port_info = {
                    "port": parts[0],
                    "state": parts[1],
                    "service": parts[2] if len(parts) > 2 else "",
                    "version": " ".join(parts[3:]) if len(parts) > 3 else ""
                }
                ports.append(port_info)
    return ports


def save_results(target, scan_results, timestamp):
    """Save scan results as both text and JSON."""
    os.makedirs(LOG_DIR, exist_ok=True)
    safe_target = target.replace(".", "_").replace("/", "_")

    # Text log
    txt_path = os.path.join(LOG_DIR, f"{timestamp}_{safe_target}.txt")
    with open(txt_path, "w") as f:
        f.write(f"# CGT 312 Network Scan Results\n")
        f.write(f"# Target: {target}\n")
        f.write(f"# Timestamp: {timestamp}\n\n")
        for scan in scan_results:
            f.write(f"\n{'='*60}\n")
            f.write(f"Command: {scan['command']}\n")
            f.write(f"{'='*60}\n")
            f.write(scan["output"])

    # JSON log (structured data)
    json_path = os.path.join(LOG_DIR, f"{timestamp}_{safe_target}.json")
    all_ports = []
    for scan in scan_results:
        all_ports.extend(parse_open_ports(scan["output"]))

    report = {
        "target": target,
        "timestamp": timestamp,
        "open_ports": all_ports,
        "scans": scan_results
    }
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n{GREEN}[+] Text log saved:  {txt_path}{NC}")
    print(f"{GREEN}[+] JSON log saved:  {json_path}{NC}")
    return all_ports


def print_summary(target, open_ports, timestamp):
    """Print a formatted attack surface summary."""
    print(f"\n{CYAN}{'='*60}{NC}")
    print(f"{CYAN}  SCAN SUMMARY: {target}{NC}")
    print(f"{CYAN}  {timestamp}{NC}")
    print(f"{CYAN}{'='*60}{NC}")

    if not open_ports:
        print(f"{YELLOW}  No open ports found (or host is down).{NC}")
    else:
        print(f"{GREEN}  Open Ports ({len(open_ports)} found):{NC}\n")
        print(f"  {'PORT':<15} {'STATE':<10} {'SERVICE':<12} {'VERSION'}")
        print(f"  {'-'*60}")
        for p in open_ports:
            print(f"  {p['port']:<15} {p['state']:<10} {p['service']:<12} {p['version']}")

    print(f"\n  {YELLOW}Attack Surface Notes:{NC}")
    for p in open_ports:
        port_num = p["port"].split("/")[0]
        service = p.get("service", "").lower()
        if "ssh" in service:
            print(f"  • Port {port_num} (SSH) – check for weak credentials, outdated version")
        elif "http" in service:
            print(f"  • Port {port_num} (HTTP) – web application; check for web vulnerabilities")
        elif "ftp" in service:
            print(f"  • Port {port_num} (FTP) – check for anonymous login, cleartext transfer")
        elif "telnet" in service:
            print(f"  • Port {port_num} (Telnet) – unencrypted, HIGH RISK")
        elif "mysql" in service or "3306" in p["port"]:
            print(f"  • Port {port_num} (MySQL) – database exposed, check access controls")
        elif "rdp" in service or "3389" in p["port"]:
            print(f"  • Port {port_num} (RDP) – remote desktop; check for BlueKeep and weak creds")

    print(f"{CYAN}{'='*60}{NC}\n")


def main():
    if len(sys.argv) < 2:
        print(f"{RED}Usage: python network_scan.py <target>{NC}")
        print("  Example: python network_scan.py scanme.nmap.org")
        print("  Example: python network_scan.py 127.0.0.1")
        sys.exit(1)

    target = sys.argv[1]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    warn()
    print(f"{CYAN}[*] Network Scan: {target}{NC}")
    print(f"{CYAN}[*] Timestamp:    {timestamp}{NC}\n")

    # Check nmap is available
    try:
        subprocess.run(["nmap", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(f"{RED}[!] nmap not found. Run: bash setup.sh{NC}")
        sys.exit(1)

    scan_results = []

    # Scan 1: Ping sweep / host check
    scan_results.append(run_nmap(target, "-sn", "Phase 1: Host Discovery"))

    # Scan 2: Service + version detection
    scan_results.append(run_nmap(target, "-sV -sC", "Phase 2: Service Version Detection"))

    # Scan 3: OS detection (best effort, may need root)
    scan_results.append(run_nmap(target, "-O", "Phase 3: OS Detection"))

    # Save results and extract open ports
    open_ports = save_results(target, scan_results, timestamp)

    # Print summary
    print_summary(target, open_ports, timestamp)


if __name__ == "__main__":
    main()
