#!/usr/bin/env python3
"""
CGT 312 Ethical Hacking – Interactive CLI Launcher
Termux Learning Environment
============================================================
LEGAL NOTICE: For educational use only.
Only test systems you own or have explicit written permission to test.
============================================================
"""

import os
import sys
import json
import subprocess
import datetime

# ─── Colour helpers ──────────────────────────────────────────────────────────

RED    = "\033[0;31m"
GREEN  = "\033[0;32m"
YELLOW = "\033[1;33m"
CYAN   = "\033[0;36m"
BOLD   = "\033[1m"
NC     = "\033[0m"

def red(t):    return f"{RED}{t}{NC}"
def green(t):  return f"{GREEN}{t}{NC}"
def yellow(t): return f"{YELLOW}{t}{NC}"
def cyan(t):   return f"{CYAN}{t}{NC}"
def bold(t):   return f"{BOLD}{t}{NC}"

# ─── Paths ───────────────────────────────────────────────────────────────────

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR  = os.path.join(BASE_DIR, "modules")
LABS_DIR     = os.path.join(BASE_DIR, "labs")
SCRIPTS_DIR  = os.path.join(BASE_DIR, "scripts")
LOGS_DIR     = os.path.join(BASE_DIR, "logs")
REPORTS_DIR  = os.path.join(BASE_DIR, "reports")
PROGRESS_FILE = os.path.join(BASE_DIR, "progress.json")

# ─── Progress tracker ────────────────────────────────────────────────────────

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {
        "module1": {"completed": False, "score": 0, "timestamp": None},
        "module2": {"completed": False, "score": 0, "timestamp": None},
        "module3": {"completed": False, "score": 0, "timestamp": None},
        "module4": {"completed": False, "score": 0, "timestamp": None},
        "module5": {"completed": False, "score": 0, "timestamp": None},
        "ctf":     {"completed": False, "score": 0, "timestamp": None},
    }

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

def mark_complete(progress, module, score=10):
    progress[module]["completed"] = True
    progress[module]["score"] = score
    progress[module]["timestamp"] = datetime.datetime.now().isoformat()
    save_progress(progress)
    print(green(f"\n✔ {module} marked complete! (+{score} pts)"))

# ─── Logging ─────────────────────────────────────────────────────────────────

def save_log(module, content):
    """Save command output to logs/<module>/YYYY-MM-DD_HH-MM-SS.txt"""
    log_dir = os.path.join(LOGS_DIR, module)
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(log_dir, f"{timestamp}.txt")
    with open(log_path, "w") as f:
        f.write(f"# CGT 312 Log – {module} – {timestamp}\n\n")
        f.write(content)
    print(green(f"\n[+] Output saved: {log_path}"))
    return log_path

# ─── Helpers ─────────────────────────────────────────────────────────────────

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def pause():
    input(yellow("\n[Enter] to continue..."))

def run_cmd(cmd, module=None, save=True):
    """Run a shell command, optionally save output to logs."""
    print(cyan(f"\n$ {cmd}\n"))
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=120
        )
        output = result.stdout + result.stderr
        print(output)
        if save and module:
            save_log(module, f"$ {cmd}\n\n{output}")
        return output
    except subprocess.TimeoutExpired:
        print(red("[!] Command timed out after 120 seconds."))
        return ""
    except Exception as e:
        print(red(f"[!] Error: {e}"))
        return ""

def show_file(path):
    """Print a markdown file to the terminal."""
    if os.path.exists(path):
        with open(path) as f:
            print(f.read())
    else:
        print(red(f"[!] File not found: {path}"))

def ethical_warning():
    print(red("""
╔══════════════════════════════════════════════════════╗
║  ⚠  ETHICAL USE WARNING                             ║
║                                                      ║
║  The following techniques are for EDUCATIONAL use.  ║
║  Only run these on systems you OWN or have WRITTEN  ║
║  permission to test. Unauthorized use is ILLEGAL.   ║
╚══════════════════════════════════════════════════════╝
"""))

# ─── Banner ──────────────────────────────────────────────────────────────────

def banner(progress):
    total = sum(v["score"] for v in progress.values())
    completed = sum(1 for v in progress.values() if v["completed"])
    clear()
    print(cyan("""
╔══════════════════════════════════════════════╗
║        CGT 312 Ethical Hacking Lab           ║
║          Termux Learning Environment         ║
╠══════════════════════════════════════════════╣
║  1. Setup Environment                        ║
║  2. Module 1: Fundamentals                   ║
║  3. Module 2: Footprinting & Scanning        ║
║  4. Module 3: Attacks (Safe Practice)        ║
║  5. Module 4: Web Services & IDS             ║
║  6. Module 5: Forensics                      ║
║  7. Run Full Lab Workflow                    ║
║  8. View Logs / Reports                      ║
║  9. CTF Challenges                           ║
║  0. Exit                                     ║
╚══════════════════════════════════════════════╝"""))
    print(green(f"  Score: {total} pts  |  Modules completed: {completed}/6\n"))

# ─── Menu options ─────────────────────────────────────────────────────────────

def option_setup():
    clear()
    print(bold("=== Setup Environment ===\n"))
    print("This will run setup.sh to install all required tools.\n")
    print("Tools: nmap, sqlmap, hydra, nikto, john, netcat, gobuster, whatweb, tshark\n")
    confirm = input(yellow("Run setup.sh now? [y/N]: ")).strip().lower()
    if confirm == "y":
        setup_path = os.path.join(BASE_DIR, "setup.sh")
        os.system(f"bash {setup_path}")
    else:
        print(yellow("Setup skipped. Run 'bash setup.sh' manually."))
    pause()

def option_module1(progress):
    clear()
    ethical_warning()
    print(bold("=== Module 1: Security Fundamentals ===\n"))
    print("Topics: CIA Triad, Threat Actors, OSI/TCP-IP, Legal Frameworks\n")

    sub = input("""
  a) Read module notes
  b) Open-port check (bash /dev/tcp demo)
  c) Mark module as complete
  q) Back

Choice: """).strip().lower()

    if sub == "a":
        show_file(os.path.join(MODULES_DIR, "module1_fundamentals.md"))
        pause()

    elif sub == "b":
        print(bold("\n--- Open Port Check via /dev/tcp ---"))
        print("This checks whether a port is open using only bash built-ins.\n")
        host = input("Target host (e.g. scanme.nmap.org or 127.0.0.1): ").strip()
        port = input("Port to check (e.g. 22, 80): ").strip()
        if host and port:
            cmd = (
                f"(echo >/dev/tcp/{host}/{port}) 2>/dev/null "
                f"&& echo 'Port {port} is OPEN' "
                f"|| echo 'Port {port} is CLOSED/FILTERED'"
            )
            run_cmd(cmd, module="module1")
        pause()

    elif sub == "c":
        mark_complete(progress, "module1")
        pause()

    option_module1(progress) if sub not in ("q", "") else None

def option_module2(progress):
    clear()
    ethical_warning()
    print(bold("=== Module 2: Footprinting & Scanning ===\n"))
    print("Legal targets: scanme.nmap.org | localhost\n")

    sub = input("""
  a) Read module notes
  b) WHOIS lookup
  c) DNS lookup (dig)
  d) nmap – basic scan
  e) nmap – full scan (sV, sC, O)
  f) Run scan.sh (automated)
  g) Run network_scan.py (wrapper + logging)
  h) Mark module as complete
  q) Back

Choice: """).strip().lower()

    if sub == "a":
        show_file(os.path.join(MODULES_DIR, "module2_footprinting.md"))
        pause()

    elif sub == "b":
        target = input("Domain for WHOIS (e.g. example.com): ").strip()
        if target:
            run_cmd(f"whois {target}", module="module2")
        pause()

    elif sub == "c":
        target = input("Domain for DNS lookup (e.g. scanme.nmap.org): ").strip()
        if target:
            run_cmd(f"dig {target} ANY +short", module="module2")
        pause()

    elif sub == "d":
        target = input("Target (e.g. scanme.nmap.org): ").strip()
        if target:
            run_cmd(f"nmap {target}", module="module2")
        pause()

    elif sub == "e":
        target = input("Target (e.g. scanme.nmap.org): ").strip()
        if target:
            run_cmd(f"nmap -sV -sC -O {target}", module="module2")
        pause()

    elif sub == "f":
        target = input("Target for scan.sh (e.g. scanme.nmap.org): ").strip()
        if target:
            script = os.path.join(SCRIPTS_DIR, "scan.sh")
            run_cmd(f"bash {script} {target}", module="module2")
        pause()

    elif sub == "g":
        target = input("Target for network_scan.py: ").strip()
        if target:
            script = os.path.join(SCRIPTS_DIR, "network_scan.py")
            run_cmd(f"python {script} {target}", module="module2")
        pause()

    elif sub == "h":
        mark_complete(progress, "module2")
        pause()

    option_module2(progress) if sub not in ("q", "") else None

def option_module3(progress):
    clear()
    ethical_warning()
    print(bold("=== Module 3: Attacks (Safe Demo Only) ===\n"))
    print("WARNING: Only use on LOCAL targets (DVWA, localhost, your own hash files).\n")

    sub = input("""
  a) Read module notes
  b) Crack a sample hash with john
  c) Hydra brute-force demo (localhost only)
  d) sqlmap demo (testphp.vulnweb.com)
  e) Run password_lab.sh
  f) Run sqlmap_runner.sh
  g) Mark module as complete
  q) Back

Choice: """).strip().lower()

    if sub == "a":
        show_file(os.path.join(MODULES_DIR, "module3_attacks.md"))
        pause()

    elif sub == "b":
        sample_hash = os.path.join(BASE_DIR, "labs", "sample_hashes.txt")
        if not os.path.exists(sample_hash):
            # Create a sample hash file (MD5 of "password123")
            os.makedirs(os.path.dirname(sample_hash), exist_ok=True)
            with open(sample_hash, "w") as fh:
                fh.write("# Sample hashes for john lab\n")
                fh.write("user1:482c811da5d5b4bc6d497ffa98491e38\n")  # password123
                fh.write("user2:5f4dcc3b5aa765d61d8327deb882cf99\n")  # password
            print(green(f"[+] Created sample hash file: {sample_hash}"))
        run_cmd(f"john --wordlist=/usr/share/wordlists/rockyou.txt {sample_hash} --format=raw-md5",
                module="module3")
        pause()

    elif sub == "c":
        print(yellow("\nHydra brute force – localhost SSH demo"))
        print(red("[!] Only run against 127.0.0.1 or your DVWA instance.\n"))
        run_cmd(
            "echo 'admin\nroot\nuser' > /tmp/users.txt && "
            "echo 'password\n123456\nadmin' > /tmp/pass.txt && "
            "hydra -L /tmp/users.txt -P /tmp/pass.txt 127.0.0.1 ssh -t 4 -V 2>&1 | head -30",
            module="module3"
        )
        pause()

    elif sub == "d":
        print(yellow("\nsqlmap demo against testphp.vulnweb.com (authorised target)"))
        run_cmd(
            "sqlmap -u 'http://testphp.vulnweb.com/listproducts.php?cat=1' "
            "--batch --level=1 --risk=1 --dbs 2>&1 | head -60",
            module="module3"
        )
        pause()

    elif sub == "e":
        script = os.path.join(SCRIPTS_DIR, "password_lab.sh")
        run_cmd(f"bash {script}", module="module3")
        pause()

    elif sub == "f":
        script = os.path.join(SCRIPTS_DIR, "sqlmap_runner.sh")
        run_cmd(f"bash {script}", module="module3")
        pause()

    elif sub == "g":
        mark_complete(progress, "module3")
        pause()

    option_module3(progress) if sub not in ("q", "") else None

def option_module4(progress):
    clear()
    ethical_warning()
    print(bold("=== Module 4: Web Services & IDS ===\n"))
    print("Tools: nikto, gobuster, whatweb, tshark\n")

    sub = input("""
  a) Read module notes
  b) nikto – web vulnerability scan
  c) gobuster – directory brute force
  d) whatweb – technology fingerprint
  e) tshark – capture 30 packets
  f) Run web_scan.sh
  g) Run log_analyzer.py
  h) Mark module as complete
  q) Back

Choice: """).strip().lower()

    if sub == "a":
        show_file(os.path.join(MODULES_DIR, "module4_web_ids.md"))
        pause()

    elif sub == "b":
        target = input("Target URL (e.g. http://testphp.vulnweb.com): ").strip()
        if target:
            run_cmd(f"nikto -h {target} 2>&1 | head -60", module="module4")
        pause()

    elif sub == "c":
        target = input("Target URL (e.g. http://testphp.vulnweb.com): ").strip()
        wordlist = "/usr/share/wordlists/dirb/common.txt"
        if target:
            run_cmd(f"gobuster dir -u {target} -w {wordlist} 2>&1 | head -40",
                    module="module4")
        pause()

    elif sub == "d":
        target = input("Target URL (e.g. http://testphp.vulnweb.com): ").strip()
        if target:
            run_cmd(f"whatweb -v {target}", module="module4")
        pause()

    elif sub == "e":
        iface = input("Network interface (e.g. wlan0, lo): ").strip() or "lo"
        run_cmd(f"tshark -i {iface} -c 30 2>&1", module="module4")
        pause()

    elif sub == "f":
        script = os.path.join(SCRIPTS_DIR, "web_scan.sh")
        run_cmd(f"bash {script}", module="module4")
        pause()

    elif sub == "g":
        script = os.path.join(SCRIPTS_DIR, "log_analyzer.py")
        run_cmd(f"python {script}", module="module4")
        pause()

    elif sub == "h":
        mark_complete(progress, "module4")
        pause()

    option_module4(progress) if sub not in ("q", "") else None

def option_module5(progress):
    clear()
    print(bold("=== Module 5: Digital Forensics ===\n"))
    print("Tools: grep, awk, sort, uniq, log_parser.sh, anomaly_detector.py\n")

    sub = input("""
  a) Read module notes
  b) Analyze sample access.log (grep/awk)
  c) Detect brute-force attempts in log
  d) Top IPs by request count
  e) Run log_parser.sh
  f) Run anomaly_detector.py
  g) Mark module as complete
  q) Back

Choice: """).strip().lower()

    if sub == "a":
        show_file(os.path.join(MODULES_DIR, "module5_forensics.md"))
        pause()

    elif sub == "b":
        log = os.path.join(BASE_DIR, "labs", "sample_access.log")
        if not os.path.exists(log):
            _create_sample_log(log)
        run_cmd(f"cat {log}", module="module5")
        pause()

    elif sub == "c":
        log = os.path.join(BASE_DIR, "labs", "sample_access.log")
        if not os.path.exists(log):
            _create_sample_log(log)
        # >10 failed logins from same IP
        run_cmd(
            f"grep '401\\|403' {log} | awk '{{print $1}}' | sort | uniq -c | sort -rn | head -10",
            module="module5"
        )
        pause()

    elif sub == "d":
        log = os.path.join(BASE_DIR, "labs", "sample_access.log")
        if not os.path.exists(log):
            _create_sample_log(log)
        run_cmd(
            f"awk '{{print $1}}' {log} | sort | uniq -c | sort -rn | head -20",
            module="module5"
        )
        pause()

    elif sub == "e":
        script = os.path.join(SCRIPTS_DIR, "log_parser.sh")
        run_cmd(f"bash {script}", module="module5")
        pause()

    elif sub == "f":
        script = os.path.join(SCRIPTS_DIR, "anomaly_detector.py")
        run_cmd(f"python {script}", module="module5")
        pause()

    elif sub == "g":
        mark_complete(progress, "module5")
        pause()

    option_module5(progress) if sub not in ("q", "") else None

def _create_sample_log(path):
    """Generate a sample Apache access log for forensics labs."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sample = (
        '192.168.1.100 - - [20/Mar/2024:10:00:01 +0000] "GET / HTTP/1.1" 200 1234\n'
        '10.0.0.5 - - [20/Mar/2024:10:00:05 +0000] "GET /admin HTTP/1.1" 401 512\n'
        '10.0.0.5 - - [20/Mar/2024:10:00:06 +0000] "POST /admin/login HTTP/1.1" 401 512\n'
        '10.0.0.5 - - [20/Mar/2024:10:00:07 +0000] "POST /admin/login HTTP/1.1" 401 512\n'
        '10.0.0.5 - - [20/Mar/2024:10:00:08 +0000] "POST /admin/login HTTP/1.1" 401 512\n'
        '10.0.0.5 - - [20/Mar/2024:10:00:09 +0000] "POST /admin/login HTTP/1.1" 401 512\n'
        '10.0.0.5 - - [20/Mar/2024:10:00:10 +0000] "POST /admin/login HTTP/1.1" 401 512\n'
        '192.168.1.200 - - [20/Mar/2024:10:00:15 +0000] "GET /index.php?id=1 HTTP/1.1" 200 4567\n'
        '192.168.1.200 - - [20/Mar/2024:10:00:16 +0000] "GET /index.php?id=1 OR 1=1 HTTP/1.1" 500 123\n'
        '172.16.0.99 - - [20/Mar/2024:10:01:00 +0000] "GET /robots.txt HTTP/1.1" 200 89\n'
        '172.16.0.99 - - [20/Mar/2024:10:01:01 +0000] "GET /.git/config HTTP/1.1" 404 0\n'
        '192.168.1.100 - - [20/Mar/2024:10:02:00 +0000] "GET /about.html HTTP/1.1" 200 2300\n'
        '10.0.0.5 - - [20/Mar/2024:10:02:05 +0000] "POST /admin/login HTTP/1.1" 401 512\n'
        '10.0.0.5 - - [20/Mar/2024:10:02:06 +0000] "POST /admin/login HTTP/1.1" 200 1024\n'
    )
    with open(path, "w") as f:
        f.write(sample)
    print(green(f"[+] Sample access log created: {path}"))

def option_full_workflow(progress):
    clear()
    ethical_warning()
    print(bold("=== Full Lab Workflow ===\n"))
    print("This runs a complete reconnaissance + web scan on scanme.nmap.org\n")
    print(yellow("[!] This only targets authorised public demo servers.\n"))
    confirm = input("Proceed? [y/N]: ").strip().lower()
    if confirm != "y":
        return

    target = "scanme.nmap.org"
    web_target = "http://testphp.vulnweb.com"

    print(bold("\n[Step 1] WHOIS Lookup"))
    run_cmd(f"whois {target} 2>&1 | head -30", module="module2")

    print(bold("\n[Step 2] DNS Lookup"))
    run_cmd(f"dig {target} A +short", module="module2")

    print(bold("\n[Step 3] nmap Scan"))
    run_cmd(f"nmap -sV -sC {target} 2>&1 | head -50", module="module2")

    print(bold("\n[Step 4] whatweb Fingerprint"))
    run_cmd(f"whatweb {web_target}", module="module4")

    print(bold("\n[Step 5] nikto Web Scan"))
    run_cmd(f"nikto -h {web_target} 2>&1 | head -40", module="module4")

    mark_complete(progress, "module2", score=15)
    mark_complete(progress, "module4", score=15)
    pause()

def option_view_logs(progress):
    clear()
    print(bold("=== Logs / Reports ===\n"))

    # Show progress table
    print(bold("─── Progress Tracker ───────────────────────"))
    total = 0
    for mod, data in progress.items():
        status = green("✔ Complete") if data["completed"] else yellow("○ Pending")
        score  = data["score"]
        total += score
        ts     = data["timestamp"][:10] if data["timestamp"] else "—"
        print(f"  {mod:<10} {status:<20} {score:>3} pts   {ts}")
    print(f"\n  Total Score: {bold(str(total))} pts\n")

    # List log files
    print(bold("─── Saved Logs ──────────────────────────────"))
    found = False
    for mod in ["module1", "module2", "module3", "module4", "module5"]:
        log_dir = os.path.join(LOGS_DIR, mod)
        if os.path.isdir(log_dir):
            files = [f for f in os.listdir(log_dir) if f.endswith(".txt")]
            if files:
                found = True
                print(f"\n  {cyan(mod)}:")
                for fn in sorted(files)[-5:]:  # show last 5
                    print(f"    logs/{mod}/{fn}")
    if not found:
        print("  No logs yet. Complete some labs first.")

    # Report template
    print(bold("\n─── Report Template ─────────────────────────"))
    print(f"  {os.path.join(REPORTS_DIR, 'template.md')}")
    pause()

def option_ctf(progress):
    clear()
    print(bold("=== CTF Challenges ===\n"))
    print("Solve these challenges to earn bonus points!\n")

    challenges = [
        ("CTF 1", "What does 'CIA' stand for in cybersecurity?",
         ["confidentiality integrity availability",
          "cia", "confidentiality, integrity, availability"]),
        ("CTF 2", "What nmap flag detects service versions?",
         ["-sv", "-sV"]),
        ("CTF 3", "What HTTP status code means 'Unauthorized'?",
         ["401"]),
        ("CTF 4", "What tool cracks password hashes using wordlists?",
         ["john", "john the ripper"]),
        ("CTF 5", "What is the default port for SSH?",
         ["22"]),
    ]

    score = 0
    for name, question, answers in challenges:
        print(cyan(f"\n[{name}] {question}"))
        ans = input("Your answer: ").strip().lower()
        if any(ans == a.lower() for a in answers):
            print(green("  ✔ Correct! +2 pts"))
            score += 2
        else:
            print(red(f"  ✘ Incorrect. Answer: {answers[0]}"))

    print(bold(f"\nCTF Score: {score}/10"))
    if score >= 6:
        mark_complete(progress, "ctf", score=score)
    pause()

# ─── Main loop ────────────────────────────────────────────────────────────────

def main():
    progress = load_progress()

    while True:
        banner(progress)
        choice = input("Select option: ").strip()

        if choice == "1":
            option_setup()
        elif choice == "2":
            option_module1(progress)
        elif choice == "3":
            option_module2(progress)
        elif choice == "4":
            option_module3(progress)
        elif choice == "5":
            option_module4(progress)
        elif choice == "6":
            option_module5(progress)
        elif choice == "7":
            option_full_workflow(progress)
        elif choice == "8":
            option_view_logs(progress)
        elif choice == "9":
            option_ctf(progress)
        elif choice == "0":
            print(green("\nGoodbye! Keep hacking ethically. 🛡️\n"))
            sys.exit(0)
        else:
            print(red("[!] Invalid option."))

if __name__ == "__main__":
    main()
