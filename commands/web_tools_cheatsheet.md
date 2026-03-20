# Web Tools Command Cheat Sheet

> ⚠️ Only use these tools on systems you own or have explicit written permission to test.
> Authorized targets: `testphp.vulnweb.com`, `localhost`, DVWA (self-hosted).

---

## nikto

```bash
# Basic scan
nikto -h http://target.com

# Specify port
nikto -h http://target.com -p 8080

# HTTPS target
nikto -h https://target.com -ssl

# Save output (text/html/csv/xml)
nikto -h http://target.com -o output.txt
nikto -h http://target.com -o output.html -Format html

# Scan with authentication
nikto -h http://target.com -id username:password

# Tuning options (-T flag)
# 0 = File upload, 1 = Interesting files, 2 = Misconfiguration
# 3 = Info disclosure, 4 = XSS/Script, 5 = Remote file retrieval
# 6 = DoS, 7 = Remote file retrieval (server), 8 = Command exec
nikto -h http://target.com -Tuning 3

# Verbose display
nikto -h http://target.com -Display V

# Avoid sending X-Nikto headers
nikto -h http://target.com -nointeractive

# Example (authorized target)
nikto -h http://testphp.vulnweb.com -o logs/module4/nikto.txt
```

---

## gobuster

```bash
# Directory brute force
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt

# With file extensions
gobuster dir -u http://target.com \
  -w /usr/share/wordlists/dirb/common.txt \
  -x php,html,txt,bak,old

# DNS subdomain enumeration
gobuster dns -d target.com -w /usr/share/wordlists/dnsx/subdomains.txt

# Virtual host discovery
gobuster vhost -u http://target.com -w subdomains.txt

# Custom status codes
gobuster dir -u http://target.com -w wordlist.txt -s "200,204,301,302,403"

# Set threads
gobuster dir -u http://target.com -w wordlist.txt -t 50

# Set timeout
gobuster dir -u http://target.com -w wordlist.txt --timeout 5s

# Set user-agent
gobuster dir -u http://target.com -w wordlist.txt \
  -a "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# Follow redirects
gobuster dir -u http://target.com -w wordlist.txt -r

# Save output
gobuster dir -u http://target.com -w wordlist.txt -o output.txt

# Wordlist locations (vary by system)
# /usr/share/wordlists/dirb/common.txt
# /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
# /data/data/com.termux/files/usr/share/wordlists/    (Termux)
```

---

## whatweb

```bash
# Basic fingerprint
whatweb http://target.com

# Verbose
whatweb -v http://target.com

# Aggression levels (1-4)
whatweb -a 1 http://target.com   # stealthy (default, 1 request)
whatweb -a 3 http://target.com   # aggressive (many requests)
whatweb -a 4 http://target.com   # heavy (follow every link)

# Scan multiple targets from file
whatweb -i targets.txt

# Output formats
whatweb --log-json=output.json http://target.com
whatweb --log-xml=output.xml http://target.com
whatweb --log-verbose=output.txt http://target.com

# Quiet mode (just the essentials)
whatweb -q http://target.com

# Example (authorized target)
whatweb -v http://testphp.vulnweb.com > logs/module4/whatweb.txt
```

---

## tshark

```bash
# List interfaces
tshark -D

# Capture on interface
tshark -i eth0
tshark -i wlan0
tshark -i lo        # loopback

# Capture N packets
tshark -i lo -c 50

# Capture to file
tshark -i eth0 -w capture.pcap

# Read pcap file
tshark -r capture.pcap

# Capture filter (BPF syntax – applied during capture)
tshark -i eth0 -f "port 80"
tshark -i eth0 -f "host 192.168.1.1"
tshark -i eth0 -f "tcp and not port 22"

# Display filter (applied when reading)
tshark -r capture.pcap -Y "http"
tshark -r capture.pcap -Y "tcp.port == 80"
tshark -r capture.pcap -Y "ip.src == 192.168.1.100"
tshark -r capture.pcap -Y "http.request.method == GET"
tshark -r capture.pcap -Y "dns"

# Extract specific fields
tshark -r capture.pcap -T fields \
  -e ip.src -e ip.dst -e tcp.dstport

# Show HTTP requests
tshark -r capture.pcap -Y "http.request" -T fields \
  -e ip.src -e http.request.method -e http.request.uri

# Count packets per IP
tshark -r capture.pcap -T fields -e ip.src | sort | uniq -c | sort -rn

# Export HTTP objects
tshark -r capture.pcap --export-objects http,/tmp/http_objects/
```

---

## curl (HTTP Testing)

```bash
# GET request
curl http://target.com

# Show headers
curl -I http://target.com

# Follow redirects
curl -L http://target.com

# POST request
curl -X POST http://target.com/login \
  -d "username=admin&password=test"

# POST with JSON
curl -X POST http://target.com/api \
  -H "Content-Type: application/json" \
  -d '{"user":"admin","pass":"test"}'

# Custom headers
curl -H "User-Agent: Mozilla/5.0" http://target.com
curl -H "Cookie: session=abc123" http://target.com

# Basic authentication
curl -u username:password http://target.com

# Save output
curl -o output.html http://target.com

# Verbose (show full request/response)
curl -v http://target.com

# Test for SQLi
curl "http://testphp.vulnweb.com/listproducts.php?cat=1'"
```

---

## sqlmap

```bash
# Basic scan
sqlmap -u "http://target.com/page.php?id=1" --batch

# List databases
sqlmap -u "http://target.com/page.php?id=1" --batch --dbs

# List tables
sqlmap -u "http://target.com/page.php?id=1" --batch -D dbname --tables

# Dump table
sqlmap -u "http://target.com/page.php?id=1" --batch -D dbname -T tablename --dump

# POST request
sqlmap -u "http://target.com/login.php" \
  --data "user=admin&pass=test" --batch

# Increase test level/risk
sqlmap -u "..." --level=3 --risk=2 --batch

# Use random user agent
sqlmap -u "..." --random-agent --batch

# Set threads
sqlmap -u "..." --threads=5 --batch

# Specify cookie
sqlmap -u "..." --cookie="PHPSESSID=abc123" --batch

# Example (authorized target)
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --batch --dbs
```
