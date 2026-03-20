# Forensics Command Cheat Sheet

---

## grep

```bash
# Basic search
grep "pattern" file.txt

# Case-insensitive
grep -i "error" access.log

# Show line numbers
grep -n "404" access.log

# Count matches
grep -c "POST" access.log

# Invert match (lines NOT matching)
grep -v "200" access.log

# Multiple patterns (OR)
grep -E "401|403|500" access.log

# Show context (2 lines before and after)
grep -C 2 "FAILED" auth.log

# Recursive search in directory
grep -r "password" /var/log/

# Only show filenames with matches
grep -l "error" *.log

# Whole word match
grep -w "admin" access.log

# Show only the match (not whole line)
grep -o "[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}" access.log

# Extended regex
grep -E "^([0-9]{1,3}\.){3}[0-9]{1,3}" access.log

# Find SQL injection patterns
grep -iE "(%27|'|--|union|select|insert|drop|or\+1)" access.log

# Find XSS patterns
grep -iE "(<script|javascript:|onerror=|onload=)" access.log

# Find directory traversal
grep -iE "(\.\./|%2e%2e|%252e)" access.log

# Find scanner signatures
grep -iE "(nikto|nmap|sqlmap|masscan|python-requests)" access.log
```

---

## awk

```bash
# Print specific column (field)
awk '{print $1}' file.txt           # column 1
awk '{print $1, $4, $9}' access.log # columns 1, 4, 9

# Field separator
awk -F: '{print $1}' /etc/passwd    # colon-separated

# Filter by column value
awk '$9 == "404" {print}' access.log
awk '$9 >= "400" {print}' access.log

# Count occurrences
awk '{count[$1]++} END {for (ip in count) print count[ip], ip}' access.log

# Sum a column
awk '{sum += $10} END {print "Total bytes:", sum}' access.log

# Print line if column matches pattern
awk '$1 ~ /^192\.168/ {print}' access.log

# Multi-condition
awk '$9 == "401" && $1 == "10.0.0.5" {print}' access.log

# Print between patterns
awk '/START/,/END/ {print}' file.txt

# Format output
awk '{printf "%-15s %s\n", $1, $9}' access.log

# Count requests per IP
awk '{print $1}' access.log | sort | uniq -c | sort -rn

# Extract HTTP method and URL
awk '{print $6, $7}' access.log | tr -d '"'

# Find large responses
awk '$10 > 50000 {print $1, $7, $10}' access.log

# Count by status code
awk '{codes[$9]++} END {for (c in codes) print codes[c], c}' access.log | sort -rn
```

---

## sort

```bash
# Sort alphabetically
sort file.txt

# Sort numerically
sort -n numbers.txt

# Sort in reverse
sort -r file.txt
sort -rn numbers.txt

# Sort by specific field (column 1)
sort -k1 file.txt

# Sort by second field numerically
sort -k2n file.txt

# Unique sort (remove duplicates)
sort -u file.txt

# Sort by file size (when using ls -l)
ls -l | sort -k5 -n

# Sort IP addresses correctly
sort -t. -k1,1n -k2,2n -k3,3n -k4,4n ips.txt

# Stable sort (preserve original order for equal elements)
sort -s file.txt
```

---

## uniq

```bash
# Remove duplicate lines (input must be sorted)
sort file.txt | uniq

# Count occurrences
sort file.txt | uniq -c

# Show only duplicates
sort file.txt | uniq -d

# Show only unique (non-repeated) lines
sort file.txt | uniq -u

# Ignore case
sort file.txt | uniq -i

# Combined pipeline: Top 10 IPs
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10
```

---

## cut

```bash
# Cut by delimiter and field
cut -d: -f1 /etc/passwd             # first field (username)
cut -d: -f1,3 /etc/passwd           # fields 1 and 3
cut -d' ' -f1 access.log            # first space-delimited field

# Cut by character position
cut -c1-10 file.txt                 # characters 1-10

# Extract timestamp from Apache log
awk '{print $4}' access.log | cut -d[ -f2 | cut -d: -f2,3
```

---

## tr

```bash
# Delete characters
tr -d '"' <<< '"hello"'             # → hello
tr -d '[]' <<< '[20/Mar/2024]'      # → 20/Mar/2024

# Translate
tr 'a-z' 'A-Z' <<< "hello"         # → HELLO
tr ' ' '\n' <<< "one two three"     # one word per line

# Squeeze repeated characters
tr -s ' ' <<< "too   many   spaces"
```

---

## Common Log Analysis Pipelines

```bash
# Top 10 IPs by request count
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# Count 4xx/5xx errors
grep -E '" [45][0-9]{2} ' access.log | wc -l

# Most requested URLs
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -20

# Hourly request breakdown
awk '{print $4}' access.log | cut -d: -f2 | sort | uniq -c

# IPs with brute-force pattern (>10 failed logins)
awk '$9 == "401" {print $1}' access.log | sort | uniq -c | sort -rn | awk '$1 > 10'

# Show all 500 errors with timestamp
awk '$9 == "500" {print $4, $7}' access.log

# Unique user agents
awk -F'"' '{print $6}' access.log | sort -u

# Extract failed SSH logins from auth.log
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn

# Find POST requests
grep '"POST' access.log

# Timeline for a specific IP
grep "^10.0.0.5" access.log | awk '{print $4, $6, $7, $9}' | sort
```
