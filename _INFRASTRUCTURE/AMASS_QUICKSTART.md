# 🔍 AMASS Setup Complete - Quick Reference

**Status**: ✅ Configured & Ready to Use  
**Date**: 2025-02-25  
**Version**: 1.0

---

## 📦 Files Created

```
_INFRASTRUCTURE/
├── amass_config.yaml              (9.4 KB) - Configuration file
├── amass_orchestrator.py          (12.8 KB) - Python orchestrator
├── amass_hexstrike.py             (6.8 KB) - HexStrike wrapper
├── amass_parameters.json          (8.6 KB) - Parameter schema
└── AMASS_INTEGRATION_GUIDE.md     (10.5 KB) - Full documentation
```

---

## 🚀 Quick Start (Pick One)

### **Option 1: Via Python Orchestrator**
```bash
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains example.com target.com \
  --brute-force \
  --output-dir /vault/REPORT/Classified/amass
```

### **Option 2: Via HexStrike CLI**
```python
python3 _INFRASTRUCTURE/amass_hexstrike.py config.json
```

### **Option 3: Direct AMASS Command**
```bash
amass enum \
  -d example.com \
  -brute \
  -w /usr/share/amass/wordlists/subdomains-top1million-5000.txt \
  -r 8.8.8.8,1.1.1.1,9.9.9.9 \
  -json /vault/REPORT/amass_results.json
```

### **Option 4: Via HexStrike Tools GUI** (from your screenshot)
In the dropdown, select **AMASS** and configure:
```json
{
  "custom": "parameters"
}
```

---

## ⚙️ Configuration File

Edit `_INFRASTRUCTURE/amass_config.yaml`:

```yaml
# Domains to scan
scope:
  domains:
    - example.com
    - target.com
  include_subdomains: true

# Brute force
brute_force:
  enabled: true
  wordlist: /usr/share/amass/wordlists/subdomains-top1million-5000.txt

# DNS resolvers
dns:
  resolvers:
    - 8.8.8.8
    - 1.1.1.1
    - 9.9.9.9

# Integration with Tor (optional)
integration:
  tor_enabled: false
  tor_socks5: socks5://th3-tor:9050
```

---

## 📊 Parameters Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `domains` | array | [] | Target domains |
| `brute_force` | bool | true | Enable brute forcing |
| `wordlist` | string | top1M | Wordlist to use |
| `dns_resolvers` | array | [8.8.8.8, ...] | DNS servers |
| `max_workers` | int | 50 | Concurrent workers |
| `timeout` | int | 30 | Query timeout (sec) |
| `tor_proxy` | string | null | Tor SOCKS5 URL |
| `verbose` | bool | true | Verbose output |
| `output_dir` | string | /vault/REPORT | Output location |

---

## 💡 Common Use Cases

### **1. Quick Scan**
```bash
python3 amass_orchestrator.py --domains example.com
```
⏱️ **Time**: 2-5 min | 🎯 **Passive only**

### **2. Comprehensive Scan**
```bash
python3 amass_orchestrator.py \
  --domains example.com \
  --brute-force \
  --verbose
```
⏱️ **Time**: 10-30 min | 🎯 **Includes brute force**

### **3. Anonymous Scan**
```bash
python3 amass_orchestrator.py \
  --domains example.com \
  --tor-proxy socks5://th3-tor:9050
```
⏱️ **Time**: 15-40 min | 🎯 **Routed via Tor**

### **4. Multiple Domains**
```bash
python3 amass_orchestrator.py \
  --domains domain1.com domain2.com domain3.com \
  --brute-force
```
⏱️ **Time**: 30-120 min | 🎯 **All domains**

---

## 📁 Output Structure

Results saved in `/vault/REPORT/Classified/amass/`:

```
amass/
├── example.com_subdomains.txt       ← Plain text list
├── target.com_subdomains.txt
├── amass_results_20250225_144530.json    ← Structured data
├── amass_report_20250225_144530.md       ← Markdown report
└── amass.log                        ← Execution logs
```

---

## 📄 Example Output

### **Plain Text Results**
```
www.example.com
api.example.com
mail.example.com
staging.example.com
dev.example.com
admin.example.com
... (38 more)
```

### **JSON Results**
```json
{
  "timestamp": "2025-02-25T14:45:30",
  "domains": [
    {
      "domain": "example.com",
      "status": "success",
      "subdomains_found": 42,
      "subdomains": [
        "www.example.com",
        "api.example.com",
        ...
      ]
    }
  ]
}
```

---

## ✨ Key Features

✅ DNS Enumeration  
✅ Subdomain Brute Force  
✅ Certificate Transparency Logs  
✅ Multiple Data Sources  
✅ Tor Support (Anonymous)  
✅ JSON/CSV/HTML Export  
✅ HexStrike Integration  
✅ Obsidian Caching  

---

## 🔐 Security Notes

⚠️ **Passive scanning** (without brute force) is safe  
⚠️ **Brute forcing** may trigger IDS/WAF  
⚠️ **Always use Tor** if anonymity is needed  
✓ **Check local laws** before scanning  
✓ **Get authorization** from domain owner  

---

## 🧪 Test AMASS Installation

```bash
# Check if AMASS is installed
amass --version

# If not installed:
apt-get install amass      # Linux
brew install amass         # macOS
docker pull owasp/amass    # Docker
```

---

## 🔗 HexStrike Tools GUI Integration

From your screenshot, here's how to configure AMASS in HexStrike:

```
1. Open HexStrike Tools
2. Select Tool: AMASS (from dropdown)
3. Configuration:
   {
     "domains": ["example.com"],
     "brute_force": true,
     "output_dir": "/vault/REPORT/Classified/amass"
   }
4. Priority: Normal
5. Click "Launch Task"
```

---

## 📞 Common Commands

```bash
# See all parameters
cat _INFRASTRUCTURE/amass_parameters.json | jq '.'

# Run with custom config
python3 amass_orchestrator.py --config amass_config.yaml

# View results
cat /vault/REPORT/Classified/amass/amass_results_*.json | jq '.'

# Count subdomains
wc -l /vault/REPORT/Classified/amass/*_subdomains.txt

# View report
cat /vault/REPORT/Classified/amass/amass_report_*.md
```

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| `amass: command not found` | Install AMASS: `apt-get install amass` |
| `No subdomains found` | Check domain is public, try without Tor |
| `Proxy connection failed` | Verify Tor is running: `docker ps \| grep tor` |
| `Slow enumeration` | Reduce `max_workers` or disable brute force |
| `Permission denied` | Check output directory permissions: `chmod 777 /vault` |

---

## ✅ Configuration Checklist

- [ ] AMASS installed (`amass --version`)
- [ ] Configuration file created (`amass_config.yaml`)
- [ ] Domains defined in config
- [ ] Output directory writable
- [ ] (Optional) Tor configured if anonymity needed
- [ ] (Optional) API keys added for premium sources
- [ ] Test run successful

---

## 📊 Presets

Pre-configured scanning profiles in `amass_parameters.json`:

| Preset | Time | Intensity | Best For |
|--------|------|-----------|----------|
| `quick_scan` | 2-5 min | Low | Quick checks |
| `comprehensive` | 15-30 min | Medium | Full scan |
| `thorough` | 60-120 min | High | Exhaustive |
| `anonymous` | 20-40 min | Medium | Privacy |
| `minimal` | 1-3 min | Very Low | Testing |

---

## 🎯 Next Steps

1. **Test basic scan**
   ```bash
   python3 _INFRASTRUCTURE/amass_orchestrator.py --domains example.com
   ```

2. **Check results**
   ```bash
   cat /vault/REPORT/Classified/amass/example.com_subdomains.txt
   ```

3. **Try with Tor**
   ```bash
   python3 _INFRASTRUCTURE/amass_orchestrator.py \
     --domains example.com \
     --tor-proxy socks5://th3-tor:9050
   ```

4. **Integrate with HexStrike**
   - Use HexStrike Tools GUI
   - Select AMASS from dropdown
   - Configure parameters
   - Click "Launch Task"

---

## 📚 Documentation

- **Full Guide**: `AMASS_INTEGRATION_GUIDE.md`
- **Parameters**: `amass_parameters.json`
- **Configuration**: `amass_config.yaml`
- **Code**: `amass_orchestrator.py`

---

## 🔗 External Resources

- **AMASS GitHub**: https://github.com/OWASP/Amass
- **AMASS Docs**: https://owasp.org/www-project-amass/
- **OWASP**: https://owasp.org

---

**All set! AMASS is configured and ready to use.** 🚀

Start with:
```bash
python3 _INFRASTRUCTURE/amass_orchestrator.py --domains example.com
```
