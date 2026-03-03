# 🔍 AMASS Configuration for HexStrike - COMPLETE

**Status**: ✅ Fully Configured  
**Date**: 2025-02-25  
**Version**: 1.0  
**Ready**: YES

---

## 🎯 What You Have

Complete AMASS (OWASP OSINT Reconnaissance Framework) integration for HexStrike with:

✅ **5 Configuration Files**
- `amass_config.yaml` - Main configuration
- `amass_orchestrator.py` - Python orchestrator
- `amass_hexstrike.py` - HexStrike integration
- `amass_parameters.json` - Parameter schema for HexStrike
- `AMASS_INTEGRATION_GUIDE.md` - Complete documentation

✅ **4 Documentation Files**
- `AMASS_QUICKSTART.md` - Quick reference (this file)
- `AMASS_INTEGRATION_GUIDE.md` - Full guide
- `README_AMASS_CONFIG.md` - Detailed explanation
- Examples and tutorials

✅ **Ready to Use**
- Pre-configured defaults
- Multiple scanning profiles
- Tor anonymity support
- HexStrike GUI integration
- Output automation

---

## 🚀 START HERE (Choose One)

### **Method 1: CLI (Fastest)**
```bash
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains example.com \
  --brute-force
```

### **Method 2: HexStrike Tools (GUI)**
From your screenshot:
1. Select **AMASS** from dropdown
2. Click "Launch Task"
3. Done!

### **Method 3: Direct AMASS Command**
```bash
amass enum -d example.com -brute -v
```

### **Method 4: Configuration File**
```bash
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --config _INFRASTRUCTURE/amass_config.yaml
```

---

## 📋 Parameters You Need to Know

### **Essential Parameters**

| Parameter | What It Does | Default | Example |
|-----------|-------------|---------|---------|
| `domains` | What to scan | [] | `example.com` |
| `brute_force` | Find more subdomains | true | true/false |
| `wordlist` | Brute force list | top-1M | `all.txt` (slower) |
| `output_dir` | Where to save | /vault/REPORT | any path |

### **Optional Parameters**

| Parameter | What It Does | Default | When to Use |
|-----------|-------------|---------|------------|
| `tor_proxy` | Route via Tor | none | For anonymity |
| `dns_resolvers` | Custom DNS | Google/Cloudflare | Bypass filtering |
| `max_workers` | Speed vs. stealth | 50 | 10=quiet, 200=fast |
| `timeout` | Max wait per query | 30s | 60s for slow networks |
| `verbose` | Show details | true | Debugging |

---

## 💡 5 Real-World Examples

### **Example 1: Quick Company Check**
```bash
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains mycompany.com
```
**Result**: List of all public subdomains (2-5 min)

### **Example 2: Penetration Test**
```bash
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains target.com \
  --brute-force \
  --output-dir /vault/REPORT/pentest_2025
```
**Result**: Comprehensive mapping with brute force (20-40 min)

### **Example 3: Anonymous Reconnaissance**
```bash
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains suspicious-target.com \
  --tor-proxy socks5://th3-tor:9050 \
  --brute-force
```
**Result**: All data routed through Tor for privacy

### **Example 4: Multiple Targets**
```bash
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains target1.com target2.com target3.com \
  --brute-force \
  --output-dir /vault/REPORT/multi_target
```
**Result**: Results for all 3 targets in one scan

### **Example 5: Fast Passive Only**
```bash
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains example.com
```
(No brute-force = faster, public data only)

---

## 📊 Expected Output

### **What You'll Get**

Files in `/vault/REPORT/Classified/amass/`:

```
✓ example.com_subdomains.txt     (Plain text list)
✓ amass_results_*.json           (Detailed JSON)
✓ amass_report_*.md              (Markdown report)
✓ amass.log                      (Execution log)
```

### **Example Results**

```
www.example.com
api.example.com
mail.example.com
app.example.com
admin.example.com
staging.example.com
dev.example.com
...and more
```

---

## ⚡ Performance Guide

| Scan Type | Time | CPU | Memory | Risk |
|-----------|------|-----|--------|------|
| Passive | 2-5 min | Low | 100MB | None |
| Brute Force | 10-30 min | Medium | 500MB | Medium |
| Thorough | 60+ min | High | 1GB+ | High |
| Anonymous | +50% time | Low | Same | None |

**Recommendation**: Start with passive scan, then add brute force if needed.

---

## 🔐 Security Considerations

### ✅ Safe (No Detection Risk)
- Passive DNS queries
- Certificate transparency searches
- Public data sources

### ⚠️ Moderate Risk (May Trigger IDS)
- Brute forcing (creates lots of DNS queries)
- Rate limiting needed (reduce `max_workers`)

### 🚨 High Risk (Will Be Detected)
- Active port scanning
- HTTP probing
- Without proper authorization

### ✓ Best Practice
- Always use **Tor** for sensitive targets
- Get **written authorization** first
- Check **local laws**
- Start with **passive** only
- Slow down with **reduced workers** (10-25)

---

## 🧠 How AMASS Works (Quick Version)

1. **Passive Collection** - Queries public DNS databases
2. **Certificate Search** - Looks at SSL certificate logs
3. **Source Queries** - Searches Google, Shodan, etc.
4. **Brute Force** (optional) - Tries wordlist combinations
5. **Aggregation** - Deduplicates results
6. **Output** - Generates reports

**Total time**: Usually 30-60 seconds (passive) to 30+ minutes (with brute force)

---

## 🔧 Customization Options

### **Change Wordlist (for more comprehensive brute force)**
```yaml
# In amass_config.yaml
brute_force:
  wordlist: /usr/share/amass/wordlists/all.txt  # Larger list
```

### **Change DNS Resolvers**
```yaml
dns:
  resolvers:
    - 8.8.8.8         # Google
    - 1.1.1.1         # Cloudflare
    - 9.9.9.9         # Quad9
```

### **Increase Speed**
```bash
python3 amass_orchestrator.py \
  --domains example.com \
  --max-workers 200  # Default is 50
```

### **Decrease Footprint**
```bash
python3 amass_orchestrator.py \
  --domains example.com \
  --max-workers 10   # Much quieter
```

---

## 🐛 Troubleshooting

### **Problem: "No subdomains found"**
```bash
# Try without brute force first
python3 amass_orchestrator.py --domains example.com
# If that works, the domain exists. Brute force may be slow.
```

### **Problem: "Proxy connection failed"**
```bash
# Check Tor is running
docker ps | grep th3-tor
# Should show: th3-tor  UP
```

### **Problem: "Permission denied"**
```bash
# Fix permissions
chmod 777 /vault/REPORT
```

### **Problem: "amass: command not found"**
```bash
# Install AMASS
apt-get install amass       # Linux
brew install amass         # macOS
docker pull owasp/amass    # Docker
```

---

## 📊 Scan Profiles

Choose the right profile for your needs:

### **Quick (2-5 min)**
```bash
# Just the essentials - passive only
python3 amass_orchestrator.py --domains example.com
```

### **Standard (15-30 min)**
```bash
# Full enumeration with brute force
python3 amass_orchestrator.py --domains example.com --brute-force
```

### **Thorough (60+ min)**
```bash
# Everything including active scanning
# Use only with explicit authorization!
amass enum -d example.com -brute -active
```

### **Stealthy (20-40 min)**
```bash
# Everything but routed through Tor
python3 amass_orchestrator.py \
  --domains example.com \
  --brute-force \
  --tor-proxy socks5://th3-tor:9050
```

---

## 📚 Files Explained

| File | Purpose | When to Use |
|------|---------|------------|
| `amass_config.yaml` | Main configuration | Edit for custom settings |
| `amass_orchestrator.py` | Python runner | Recommended for scripting |
| `amass_hexstrike.py` | HexStrike wrapper | Auto-integration |
| `amass_parameters.json` | Schema for GUI | HexStrike Tools reference |
| `AMASS_INTEGRATION_GUIDE.md` | Complete guide | When you need full details |

---

## ✅ Verification Checklist

Before running, verify:

- [ ] AMASS installed: `amass --version`
- [ ] Config file exists: `_INFRASTRUCTURE/amass_config.yaml`
- [ ] Output directory writable: `ls -la /vault/REPORT`
- [ ] (Optional) Tor running if using it: `docker ps | grep tor`
- [ ] Python 3 installed: `python3 --version`

---

## 🎯 Next Steps

1. **Test Installation**
   ```bash
   amass --version
   ```

2. **Run First Scan**
   ```bash
   python3 _INFRASTRUCTURE/amass_orchestrator.py \
     --domains example.com
   ```

3. **Check Results**
   ```bash
   ls -la /vault/REPORT/Classified/amass/
   ```

4. **Review Output**
   ```bash
   cat /vault/REPORT/Classified/amass/example.com_subdomains.txt
   ```

5. **Try with Your Target**
   ```bash
   python3 _INFRASTRUCTURE/amass_orchestrator.py \
     --domains yourtarget.com \
     --brute-force
   ```

---

## 📞 Quick Command Reference

```bash
# Simplest (passive only)
amass enum -d example.com

# With brute force
amass enum -d example.com -brute

# Custom wordlist
amass enum -d example.com -brute -w /path/to/wordlist.txt

# Custom resolvers
amass enum -d example.com -r 8.8.8.8,1.1.1.1

# Via Tor
amass enum -d example.com -proxy socks5://th3-tor:9050

# JSON output
amass enum -d example.com -json output.json

# Verbose
amass enum -d example.com -v

# Everything
amass enum -d example.com -brute -r 8.8.8.8 -proxy socks5://th3-tor:9050 -json results.json -v
```

---

## 🌟 Why AMASS?

✓ **Comprehensive** - Multiple data sources  
✓ **Fast** - Parallel processing  
✓ **Accurate** - Deduplication  
✓ **Flexible** - Passive or active  
✓ **Stealthy** - Can use Tor  
✓ **Free** - Open source  
✓ **Integrated** - Works with HexStrike  

---

## 📖 Complete Documentation

For more details:
- **Full Guide**: Read `AMASS_INTEGRATION_GUIDE.md`
- **Parameters**: See `amass_parameters.json`
- **Configuration**: Edit `amass_config.yaml`

---

## ✨ You're All Set!

Everything is configured and ready. Choose any method above and start scanning:

```bash
# Easiest way to start:
python3 _INFRASTRUCTURE/amass_orchestrator.py --domains example.com
```

---

**Questions?** Check `AMASS_INTEGRATION_GUIDE.md` for full documentation.

**Ready to scan?** Run the command above! 🚀
