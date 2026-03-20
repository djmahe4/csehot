#!/usr/bin/env python3
"""
network_scan.py – nmap wrapper with structured logging
CGT 312 Ethical Hacking – Module 2
Used to perform ping scans, port scans, and service version and OS fingerprinting.

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
import xml.etree.ElementTree as ET

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
    # Robustness: use XML output for parsing, but keep shell=True for 'learning purposes'
    cmd = f"nmap {flags} -oX - {target}"
    print(f"{CYAN}[*] {label}{NC}")
    print(f"{YELLOW}$ {cmd}{NC}\n")
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=180
        )
        output = result.stdout + result.stderr
        # If it's XML, don't flood the total terminal output
        if "<?xml" in output:
             print(f"{GREEN}[+] Scan complete (XML output received){NC}")
        else:
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
    """Extract open port information from nmap output using robust XML parsing."""
    ports = []
    if not nmap_output or "<?xml" not in nmap_output:
        return ports
        
    try:
        # Step 1: Extract only the XML block (robustly handle text wrap)
        xml_start = nmap_output.find("<?xml")
        xml_end = nmap_output.find("</nmaprun>")
        if xml_start == -1 or xml_end == -1:
            return ports
        
        xml_content = nmap_output[xml_start : xml_end + len("</nmaprun>")]
        
        # Step 2: Use ElementTree to parse structured data
        root = ET.fromstring(xml_content)
        
        for host in root.findall('host'):
            # Extract hostname if available
            hostname_elem = host.find('hostnames/hostname')
            hostname = hostname_elem.get('name') if hostname_elem is not None else "Unknown"
            
            ports_elem = host.find('ports')
            if ports_elem is None:
                continue
                
            for port in ports_elem.findall('port'):
                state_elem = port.find('state')
                if state_elem is not None and state_elem.get('state') == 'open':
                    port_id = port.get('portid', "?")
                    protocol = port.get('protocol', "tcp")
                    
                    service_elem = port.find('service')
                    if service_elem is not None:
                        # Extract service details with fallbacks
                        service_name = service_elem.get('name', 'Unknown')
                        product = service_elem.get('product', '')
                        version = service_elem.get('version', '')
                        extrainfo = service_elem.get('extrainfo', '')
                        
                        full_version = f"{product} {version} {extrainfo}".strip()
                        if not full_version:
                            full_version = "No version info"
                            
                        port_info = {
                            "port": f"{port_id}/{protocol}",
                            "state": "open",
                            "service": service_name,
                            "version": full_version,
                            "hostname": hostname
                        }
                        ports.append(port_info)
                    else:
                        # Port is open but service identification failed
                        ports.append({
                            "port": f"{port_id}/{protocol}",
                            "state": "open",
                            "service": "Unknown",
                            "version": "Unknown",
                            "hostname": hostname
                        })
    except Exception as e:
        # Only print error if it's truly unexpected XML
        if "<?xml" in nmap_output:
            print(f"{RED}[!] Error parsing nmap XML: {e}{NC}")
        
    return ports


def deduplicate_ports(ports):
    """Deduplicate ports by port number, merging info and maintaining host associations."""
    unique_ports = {}
    for p in ports:
        port_key = p["port"]
        if port_key not in unique_ports:
            unique_ports[port_key] = p
        else:
            # Merge logic: Prefer entries with more version/service detail
            existing = unique_ports[port_key]
            
            # If the new entry has version info and the old one doesn't, upgrade
            if p["version"] != "No version info" and existing["version"] == "No version info":
                unique_ports[port_key] = p
            # If the new entry has a descriptive service name and the old one is 'Unknown'
            elif p["service"] != "Unknown" and existing["service"] == "Unknown":
                unique_ports[port_key] = p
            # Maintain hostname if found in any version
            if p["hostname"] != "Unknown" and existing["hostname"] == "Unknown":
                existing["hostname"] = p["hostname"]
                
    return list(unique_ports.values())


def save_results(target, scan_results, timestamp):
    """Save scan results as both text and JSON."""
    os.makedirs(LOG_DIR, exist_ok=True)
    safe_target = target.replace(".", "_").replace("/", "_")

    # 1. Process and deduplicate ports from all scans
    all_ports = []
    for scan in scan_results:
        all_ports.extend(parse_open_ports(scan["output"]))
    
    all_ports = deduplicate_ports(all_ports)

    # 2. Text log (human-friendly)
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

    # 3. JSON log (structured data for automated analysis)
    json_path = os.path.join(LOG_DIR, f"{timestamp}_{safe_target}.json")
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
        print(f"  {'PORT':<15} {'STATE':<10} {'SERVICE':<15} {'HOSTNAME':<20} {'VERSION'}")
        print(f"  {'-'*85}")
        for p in open_ports:
            print(f"  {p['port']:<15} {p['state']:<10} {p['service']:<15} {p['hostname']:<20} {p['version']}")

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
