---
date: 2026-02-14
type: resources
tags: [security, learning, hacking, resources]
---

# 📚 RESSOURCES ETHICAL HACKING — Learning path complet

> Collection curatée de ressources pour apprendre cybersécurité ethiquement.
> **Legal context:** Educational + CTF + Authorized pentesting only.

---

## 🎯 Learning Path Overview

```
BEGINNER (2-4 weeks)
  ↓
INTERMEDIATE (4-8 weeks)
  ↓
ADVANCED (8-12 weeks)
  ↓
CERTIFICATION (3-6 months)
  ↓
PROFESSIONAL
```

---

---

## Phase 1 : BEGINNER — Fundamentals

### 1️⃣ Networking Basics

**What to learn :**
- OSI model (7 layers)
- TCP/IP stack
- DNS, HTTP, HTTPS
- Common ports (22, 80, 443, 3306, etc.)

**Resources :**

| Resource | Type | Time | Cost |
|----------|------|------|------|
| **TryHackMe: Network Fundamentals** | Interactive | 4-6h | Free |
| **Cisco Networking Basics (NetAcad)** | Course | 30h | Free |
| **YouTube: Computerphile Networking** | Videos | 2-3h | Free |
| **"Networks" by Kurose & Ross** | Book | Self-paced | $$ |

**Practice :**
- [ ] Lab : Packet Tracer (free from Cisco)
- [ ] Lab : Wireshark traffic analysis
- [ ] Lab : ping/tracert/nslookup commands

---

### 2️⃣ Linux Command Line

**What to learn :**
- Basic Linux commands
- File system navigation
- User/permission management
- Shell scripting basics

**Resources :**

| Resource | Type | Time | Cost |
|----------|------|------|------|
| **TryHackMe: Linux Fundamentals** | Interactive | 6-8h | Free |
| **Linux Academy basics** | Videos | 10h | Free tier |
| **"The Linux Command Line"** | Book | Self-paced | Free online |
| **OverTheWire: Bandit** | CTF | 8-10h | Free |

**Practice :**
- [ ] Install Linux (dual-boot or VM)
- [ ] Complete OverTheWire Bandit
- [ ] Write 5 shell scripts

---

### 3️⃣ Cryptography Basics

**What to learn :**
- Encryption (symmetric vs. asymmetric)
- Hashing (MD5, SHA)
- Digital signatures
- Common algorithms (AES, RSA)

**Resources :**

| Resource | Type | Time | Cost |
|----------|------|------|------|
| **TryHackMe: Cryptography** | Interactive | 4-6h | Free |
| **Coursera: Cryptography I** | Course | 6 weeks | Free audit |
| **YouTube: 3Blue1Brown Cryptography** | Videos | 3-4h | Free |
| **CryptoHack** | Interactive | Self-paced | Free |

**Practice :**
- [ ] Complete CryptoHack challenges
- [ ] Implement Caesar cipher in Python
- [ ] Understand AES encryption

---

### 4️⃣ Web Basics

**What to learn :**
- HTTP/HTTPS protocol
- HTML/CSS/JavaScript basics
- Request/response cycles
- Browser developer tools

**Resources :**

| Resource | Type | Time | Cost |
|----------|------|------|------|
| **MDN Web Docs** | Reference | Self-paced | Free |
| **TryHackMe: Web Fundamentals** | Interactive | 4-6h | Free |
| **Codecademy: HTML/CSS/JS** | Interactive | 10-15h | Free tier |

**Practice :**
- [ ] Use Chrome DevTools to inspect websites
- [ ] Create simple HTML page
- [ ] Understand HTTP requests in DevTools Network tab

---

### ✅ Phase 1 Checklist

Complete these to move to Phase 2:
- [ ] Understand OSI model
- [ ] Comfortable with Linux command line
- [ ] Know basic encryption concepts
- [ ] Understand HTTP basics
- [ ] Completed at least 1 TryHackMe beginner room
- [ ] Can write simple shell script

---

---

## Phase 2 : INTERMEDIATE — Core Security

### 1️⃣ OWASP Top 10

**What to learn :**
Each of these 10 vulnerability categories:

1. **Injection** (SQLi, OS command injection)
2. **Broken Authentication** (weak passwords, session management)
3. **Sensitive Data Exposure** (encryption failures)
4. **XML External Entities (XXE)**
5. **Broken Access Control** (IDOR, privilege escalation)
6. **Security Misconfiguration**
7. **Cross-Site Scripting (XSS)**
8. **Insecure Deserialization**
9. **Using Components with Known Vulnerabilities**
10. **Insufficient Logging & Monitoring**

**Resources :**

| Vulnerability | Resource | Type | Time |
|---|---|---|---|
| **SQLi** | WebGoat SQLi Lab | Lab | 2h |
| **SQLi** | TryHackMe: SQL Injection | Interactive | 2-3h |
| **XSS** | OWASP WebGoat XSS | Lab | 2-3h |
| **All 10** | PortSwigger: Web Security Academy | Course | 20-30h |
| **All 10** | PentesterLab: Top 10** | Interactive | Self-paced |

**Practice :**
- [ ] Complete WebGoat (all labs)
- [ ] Solve 5 SQLi challenges
- [ ] Solve 5 XSS challenges
- [ ] Understand CSRF, SSRF, XXE

---

### 2️⃣ Reconnaissance & Enumeration

**What to learn :**
- Information gathering
- Passive vs active reconnaissance
- Network scanning (Nmap)
- Web enumeration

**Tools to master :**
- `nmap` — Network mapping
- `whois`, `dig`, `nslookup` — DNS enumeration
- `curl`, `wget` — HTTP requests
- `masscan` — Fast port scanning

**Resources :**

| Tool | Resource | Type | Time |
|------|----------|------|------|
| **Nmap** | TryHackMe: Nmap | Interactive | 3-4h |
| **Nmap** | Nmap documentation + tutorials | Doc | 5-6h |
| **Network scanning** | TryHackMe: Reconnaissance | Interactive | 4-5h |
| **OSINT** | TryHackMe: OSINT | Interactive | 4-5h |

**Practice :**
- [ ] Scan your own network with Nmap
- [ ] Enumerate web application (practice target)
- [ ] Information gathering on company (OSINT)
- [ ] Map attack surface of web app

---

### 3️⃣ Exploitation Basics

**What to learn :**
- Vulnerability assessment
- Exploit development (Python)
- Payloads & shellcode basics
- Post-exploitation basics

**Resources :**

| Topic | Resource | Type | Time |
|-------|----------|------|------|
| **Exploitation** | TryHackMe: Exploitation | Interactive | 5-6h |
| **Metasploit** | TryHackMe: Metasploit | Interactive | 4-5h |
| **Python exploits** | PentesterLab: Python for Pentest | Course | 8-10h |

**Tools to master :**
- `metasploit` — Exploitation framework
- `Burp Suite Community** — Web penetration
- `Python` — Custom exploit coding

---

### 4️⃣ Web Penetration Testing

**What to learn :**
- Web application security testing
- Burp Suite usage
- Common web vulnerabilities
- Manual testing vs automated tools

**Resources :**

| Resource | Type | Time | Cost |
|----------|------|------|------|
| **PortSwigger: Web Academy** | Interactive course | 20-30h | Free |
| **Burp Suite Tutorial** | Official docs | Reference | Free |
| **TryHackMe: Web Security** | Interactive rooms | 15-20h | Free tier |
| **OWASP: Testing Guide** | Reference | Self-paced | Free |

**Practice :**
- [ ] Complete PortSwigger Web Academy
- [ ] Set up Burp Suite + Proxy
- [ ] Penetration test practice site (DVWA)
- [ ] Document findings like professional pentest

---

### ✅ Phase 2 Checklist

- [ ] Understand all OWASP Top 10
- [ ] Can use Nmap for reconnaissance
- [ ] Familiar with Burp Suite basics
- [ ] Completed OWASP WebGoat
- [ ] Completed 10+ TryHackMe rooms (medium difficulty)
- [ ] Can find + exploit simple vulnerabilities
- [ ] Understand post-exploitation basics

---

---

## Phase 3 : ADVANCED — Exploitation & Hardening

### 1️⃣ Advanced Exploitation

**Topics :**
- Custom exploit development
- Memory corruption (buffer overflow, heap spray)
- Reverse engineering basics
- Advanced web exploitation

**Resources :**

| Resource | Type | Time | Cost |
|----------|------|------|------|
| **HackTheBox: Retired Machines** | Lab | Ongoing | $$ |
| **OverTheWire: Narnia, Behemoth** | CTF | 20-30h | Free |
| **Pwnable.kr** | Exploitation challenges | Self-paced | Free |
| **Exploit-DB** | Exploit collection | Reference | Free |

---

### 2️⃣ Reverse Engineering

**Topics :**
- Assembly language basics
- Disassembly (IDA, Ghidra)
- Malware analysis
- Binary patching

**Resources :**

| Resource | Type | Time |
|----------|------|------|
| **TryHackMe: Reverse Engineering** | Interactive | 6-8h |
| **Ghidra Tutorial** | Official docs | 4-5h |
| **picoCTF: Reverse Engineering** | CTF | 10-15h |
| **YouTube: LiveOverflow** | Videos | 20-30h |

---

### 3️⃣ System Hardening & Defense

**Topics :**
- Linux/Windows hardening
- Firewall configuration
- Intrusion detection (IDS/IPS)
- Security monitoring
- Incident response

**Resources :**

| Resource | Type | Time |
|----------|------|------|
| **TryHackMe: Incident Response** | Interactive | 4-6h |
| **NIST Cybersecurity Framework** | Guide | 2-3h |
| **CIS Benchmarks** | Hardening guides | Reference |

---

### ✅ Phase 3 Checklist

- [ ] Complete 10+ HackTheBox machines (medium/hard)
- [ ] Understand buffer overflow exploitation
- [ ] Use reverse engineering tools (IDA/Ghidra)
- [ ] Completed advanced CTF challenges
- [ ] Can perform full web penetration test
- [ ] Understand system hardening basics

---

---

## Phase 4 : CERTIFICATIONS

### Option 1️⃣ : CEH (Certified Ethical Hacker)

**Prerequisites :** 5 years security experience OR CompTIA Security+

**Study plan :** 3-4 months
- Covers : All phases 1-3 + ethical/legal

**Resources :**
- EC-Council: Official courseware
- TryHackMe: CEH prep track
- YouTube: CEH tutorials
- Practice exams: Boson, MeasureUp

**Cost :** ~$1000-1500 (exam + materials)

---

### Option 2️⃣ : OSCP (Offensive Security Certified Professional)

**Prerequisites :** Intermediate hacking knowledge

**Study plan :** 3-6 months
- Covers : Real exploitation + report writing
- Includes : 24h exam (3 machines)

**Resources :**
- Offensive Security: PWK course (~40h videos)
- Hack The Box (OSCP-like machines)
- TjNull's list (60 recommended HTB machines)
- Ippsec YouTube walkthroughs

**Cost :** ~$800-1000 (course + exam)

**Why pick it :** Most respected, hands-on, real-world skills

---

### Option 3️⃣ : CompTIA Security+

**Prerequisites :** CompTIA A+ or experience

**Study plan :** 1-2 months
- Covers : Broad security fundamentals
- Vendor-neutral

**Cost :** ~$400-600

---

### Recommendation 🎯

**Timeline :**
1. Complete Phase 2 (Intermediate) — 2-3 months
2. Get Security+ — easier entry, builds foundation — 1 month
3. Complete Phase 3 (Advanced) — 2-3 months
4. Pursue OSCP — highest respect, most practical — 3-6 months

**Total timeline :** 9-14 months to OSCP = HIGHLY RESPECTED

---

---

## 🏆 CTF Platforms (Practice)

### Beginner-friendly

| Platform | Focus | Difficulty | Cost |
|----------|-------|-----------|------|
| **TryHackMe** | All-in-one | Easy-Medium | Free tier |
| **PicoCTF** | Beginner CTF | Easy | Free |
| **OverTheWire** | Capture flags | Easy-Medium | Free |

### Intermediate

| Platform | Focus | Difficulty | Cost |
|----------|-------|-----------|------|
| **HackTheBox** | Web + Machines | Medium-Hard | $ or free |
| **TryHackMe** | Deep dives | Medium-Hard | $$ |
| **PentesterLab** | Web focused | Medium | $ |

### Advanced

| Platform | Focus | Difficulty | Cost |
|----------|-------|-----------|------|
| **HackTheBox** | Retired machines | Hard | $$ |
| **OffsecLabs** | Exam prep | Hard | $$$ |
| **RootMe** | Diverse challenges | Hard | Free |

---

---

## 📖 Books (Reference & Deep Learning)

| Title | Author | Focus | Level |
|-------|--------|-------|-------|
| **The Web Application Hacker's Handbook** | Stuttard, Pinto | Web security | Intermediate+ |
| **Penetration Testing** | Georgia Weidman | General pentest | Intermediate |
| **The Hacker Playbook** | Peter Kim | Methodology | Intermediate+ |
| **Reverse Engineering for Beginners** | Dennis Yurichev | Reverse eng | Advanced |
| **The Tangled Web** | Michal Zalewski | Web security | Advanced |

---

---

## 🎯 Your Recommended Path

### Month 1-2 : **Phase 1** (Beginner)
```
Week 1-2: Networking + Linux
Week 3: Cryptography + Web basics
Week 4: Complete TryHackMe beginner rooms
Week 5-6: OverTheWire Bandit
```
→ **Goal :** Comfortable with fundamentals

---

### Month 3-4 : **Phase 2** (Intermediate)
```
Week 1-2: OWASP Top 10 (PortSwigger)
Week 3: Reconnaissance (Nmap, OSINT)
Week 4-5: Web exploitation (Burp Suite)
Week 6-8: TryHackMe medium rooms
```
→ **Goal :** Find + exploit real vulnerabilities

---

### Month 5-8 : **Phase 3** (Advanced)
```
Month 1: HackTheBox machines (easy-medium)
Month 2-3: Advanced exploitation + CTFs
Month 4: Reverse engineering basics
```
→ **Goal :** Advanced technical skills

---

### Month 9-14 : **Certification** (Optional but recommended)
```
Month 1: Security+ cert (broad foundation)
Month 2-6: OSCP prep (3-6 months)
```
→ **Goal :** Recognized credential

---

---

## 💡 Learning Tips

### 1️⃣ Do, don't just watch
- ❌ Watch videos passively
- ✅ Follow along + type commands
- ✅ Break things + fix them

### 2️⃣ Document everything
- Create note for each concept
- Walkthrough every CTF
- Keep running knowledge base (YOUR VAULT!)

### 3️⃣ Build projects
- After learning concept → apply it
- Create tool/exploit/app using it
- Add to portfolio

### 4️⃣ Join community
- Discord servers (TryHackMe, HackTheBox)
- Twitter/Reddit security communities
- Local cybersecurity meetups

### 5️⃣ Stay ethical
- Only test systems you own/have permission
- Document authorization
- Practice in legal environments (labs/CTF)
- Never cross the line

---

---

## 🎯 Your next 3 steps

1. **Today :** Start TryHackMe beginner room (30 min)
2. **This week :** Complete Phase 1 Networking (5h)
3. **This month :** Complete Phase 1 fully, start Phase 2

---

## 🔗 Quick Links

- **TryHackMe:** https://tryhackme.com
- **HackTheBox:** https://hackthebox.com
- **PortSwigger Academy:** https://portswigger.net/web-security
- **OverTheWire:** https://overthewire.org
- **PentesterLab:** https://pentesterlab.com
- **OWASP:** https://owasp.org
- **Exploit-DB:** https://exploit-db.com

---

*Document created : 2026-02-14*
*Last updated : 2026-02-14*
*Your personal learning path — follow it!*
