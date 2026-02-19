# 🎯 OSINT Operational Guide - Quick Reference

**Version:** 2.0 (Dual-Protection Legal)  
**Last Updated:** 2026-02-19  
**Status:** Production Ready  

---

## ⚡ Quick Start (3 Commands)

```powershell
# 1. Verify system is ready
powershell -ExecutionPolicy Bypass -File "VERIFY_OSINT_SETUP.ps1"

# 2. Launch Docker infrastructure
.\LANCER_OSINT.bat

# 3. Start investigation
python docker_orchestrator_osint.py
```

---

## 📋 Common Investigation Workflows

### Workflow #1: Quick IOC Investigation (5 minutes)

```python
from osint_legal_engine import OSINTLegalEngine, IOC, IOCType

# Initialize
engine = OSINTLegalEngine()

# Create quick investigation
report = engine.create_investigation(
    investigation_type="MALWARE_TRACKING",
    title="Fast Check: Suspicious Domain"
)

# Add single IOC
ioc = IOC(
    type=IOCType.DOMAIN,
    value="suspicious-domain.ru",
    confidence=85,
    source_url="https://abuseipdb.com/check",
    first_seen="2026-02-19T10:00:00Z",
    last_seen="2026-02-19T15:30:00Z",
    context="Domain seen in malware C2 traffic",
    severity="high"
)

report.add_ioc(ioc)
engine.finalize_report(report)

# Output: JSON report + Markdown summary
```

### Workflow #2: Criminal Profile Investigation (30 minutes)

```python
from osint_legal_engine import (
    OSINTLegalEngine, CriminalProfile, IOC, IOCType, 
    InvestigationType
)

engine = OSINTLegalEngine()

# Create investigation
report = engine.create_investigation(
    investigation_type=InvestigationType.CYBERCRIMINAL_PROFILING,
    title="Threat Actor Analysis: Emotet Operator"
)

# Build criminal profile
profile = CriminalProfile(
    profile_id="PROFILE_EMOTET_OPERATOR_001",
    aliases=["EmotEt_Master", "Trickbot_Admin"],
    confirmed_activities=[
        "Malware distribution",
        "Banking fraud",
        "Ransom collection"
    ],
    crypto_wallets=[
        "1A1z7agoat3nSVKwuNvaSQvHfnxRi3P9y1",
        "3J98t1WpEZ73CNmYviecrnyiWrnqRhWNLy"
    ],
    confidence=90,
    threat_level="critical"
)

report.add_profile(profile)

# Add supporting IOCs
for ioc_data in iocs_list:
    report.add_ioc(ioc_data)

engine.finalize_report(report)

# Output: Complete criminal profile with signatures
```

### Workflow #3: Authority-Grade Report (1 hour)

```python
from legal_report_generator import LegalReportGenerator, AuthorityLevel

# Initialize report generator
gen = LegalReportGenerator()

# Create investigation report
report = gen.create_investigation_report(
    investigation_id="INV_20260219_EMOTET_C2",
    title="Emotet C2 Infrastructure Analysis",
    findings_count=5,
    authority_level=AuthorityLevel.LAW_ENFORCEMENT
)

# Add evidence with chain of custody
for evidence in evidence_list:
    report.add_evidence(
        evidence_id=f"EV_{i}",
        description=evidence.description,
        source_url=evidence.source,
        confidence=evidence.confidence
    )

# Add findings with evidence linking
for finding in findings:
    report.add_finding(
        title=finding.title,
        description=finding.description,
        evidence_ids=[finding.evidence_ref],
        recommendation=finding.recommendation
    )

# Export legal report
json_report = report.generate_legal_report()
md_report = report.export_markdown()

# Verify integrity
is_valid = report.verify_report()
```

---

## 🔐 Security Checklist (Before Each Investigation)

```
Before Starting Investigation:
☐ Verify Tor connection active (SOCKS5:9050)
☐ Check audit trail encryption key is present
☐ Confirm Docker containers running
☐ Verify network isolation (172.25.0.0/16)
☐ Test signature keys loaded
☐ Confirm legal authority context

Before Finalizing Report:
☐ Verify all IOCs have sources
☐ Confirm confidence levels assigned
☐ Check timestamps are UTC
☐ Validate chain of custody
☐ Test report verification
☐ Confirm signatures applied

Before Distribution:
☐ Select correct authority format (LE/NS/Journalist/PI)
☐ Review anonymity settings
☐ Verify no operator traces
☐ Confirm encryption status
☐ Test authority verification
☐ Create backup copy
```

---

## 🎯 Investigation Types & Templates

| Type | Use Case | Time | Authority |
|------|----------|------|-----------|
| **Scam** | Financial fraud, cons | 15 min | LE + PI |
| **Darknet** | Marketplace operators | 45 min | LE |
| **Exploitation** | CSAM, trafficking | 1+ hour | LE + NS |
| **Malware** | C2, botnet tracking | 30 min | LE + NS |
| **Phishing** | Credential theft rings | 20 min | LE + NS |
| **Trafficking** | Human trafficking | 1+ hour | LE + NS |
| **Profiling** | Threat actor analysis | 1 hour | NS |
| **Intelligence** | APT, nation-state | 2+ hours | NS |

---

## 📊 IOC Quick Reference

### Create IOC (Template)
```python
from osint_legal_engine import IOC, IOCType

ioc = IOC(
    type=IOCType.DOMAIN,                    # Required: IOCType enum
    value="example.ru",                     # Required: actual value
    confidence=85,                          # Required: 0-100%
    source_url="https://...",               # Required: where found
    first_seen="2026-02-19T10:00:00Z",      # Required: ISO timestamp
    last_seen="2026-02-19T15:30:00Z",       # Required: ISO timestamp
    context="Description of indicator",     # Required: what it means
    severity="high",                        # Optional: low/medium/high/critical
    tags=["tag1", "tag2"],                  # Optional: for filtering
    related_iocs=["ID1", "ID2"]             # Optional: linking
)
```

### IOC Types Reference
```
DOMAIN              → malicious.ru, c2.example.com
IP_ADDRESS          → 203.45.67.89, 2001:db8::1
EMAIL               → attacker@email.com
HASH                → MD5, SHA-1, SHA-256, SHA-512
URL                 → https://malware.download/payload
CRYPTO_WALLET       → Bitcoin addresses, Monero wallets
USERNAME            → @hacker_alias, admin_account
PHONE               → +1-555-0123, country code included
FILE_HASH           → malware identification hashes
BITCOIN_ADDRESS     → 1A1z7agoat3nSVKwuNvaSQvHfnxRi3P9y1
```

### Confidence Levels
```
0-25%   = Speculation / Unverified rumors
26-50%  = Low confidence / Single source
51-74%  = Medium confidence / Multiple sources
75-89%  = High confidence / Cross-verified sources
90-100% = Critical / Unanimous verification (71+/71 AV detection)
```

---

## 🏗️ Docker Container Status Commands

```powershell
# Check all containers
docker ps -a | findstr "th3-"

# View logs
docker logs th3-tor                    # Tor routing
docker logs th3-kali                   # Kali Linux
docker logs th3-hackergpt              # Claude AI (port 8000)
docker logs th3-hexstrike              # Dashboard (port 8001)

# Verify Tor is routing correctly
docker exec th3-tor curl --socks5 127.0.0.1:9050 \
  https://check.torproject.org

# Check network
docker network inspect ascended33_osint

# Restart container
docker restart th3-tor

# Stop all
docker-compose -f docker-compose-osint.yml down

# Start all
docker-compose -f docker-compose-osint.yml up -d
```

---

## 💾 Report Export Formats

### JSON Export (System Integration)
```python
# Exports machine-readable report
json_report = engine.export_report_json()
# Includes: signatures, timestamps, IOCs, profiles, chain-of-custody
# Used for: Law enforcement databases, integration systems
```

### Markdown Export (Human Readable)
```python
# Exports formatted report
md_report = engine.export_report_markdown()
# Includes: narrative, IOCs, timeline, findings
# Used for: Briefings, documentation, presentations
```

### PDF Export (Legal Documents)
```python
# Exports court-ready PDF (requires extra setup)
pdf_report = engine.export_report_pdf()
# Includes: signatures verified visually
# Used for: Court presentations, official submissions
```

---

## 🔍 Verification Commands

### Verify Audit Trail
```python
from osint_legal_engine import CryptoAuditTrail

audit = CryptoAuditTrail()
# Verify HMAC signatures
is_valid = audit.verify_audit_trail()
print(f"Audit trail integrity: {is_valid}")

# Export personal audit trail
personal_audit = audit.export_audit_trail()
# Only accessible with personal key
```

### Verify Report Signature
```python
from legal_report_generator import ReportVerifier

is_valid = ReportVerifier.verify_report(report_file)
# Checks: RSA-4096 signature, timestamp, evidence links
# Result: True if all signatures valid
```

### Verify Chain of Custody
```python
is_chain_valid = ReportVerifier.verify_chain_of_custody(report_file)
# Checks: Hash imbrication, timestamps sequential
# Result: True if chain unbroken
```

---

## ⚙️ Configuration

### Environment Variables (docker-compose-osint.yml)
```yaml
ANONYMITY_MODE: "maximum"         # Tor mandatory routing
AUDIT_ENABLED: "true"             # Encrypted audit trail
SIGNATURES_ENABLED: "true"        # RSA-4096 signatures
REPORT_SIGNING: "RSA-4096-PSS"    # Signature method
ENCRYPTION_ALGO: "AES-256-GCM"    # Audit encryption
OPERATOR_ANONYMITY: "hash"        # Operator as SHA-256 hash
```

### Python Configuration
```python
engine = OSINTLegalEngine(
    tor_host="127.0.0.1",
    tor_port=9050,
    encryption_key=b"your-personal-key-here",
    signature_bits=4096,
    audit_trail_enabled=True,
    anonymity_mode="maximum"
)
```

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Tor not connecting | Check Docker: `docker logs th3-tor` |
| Port 8000 in use | `netstat -ano \| findstr :8000` then `taskkill` |
| Python import error | Install: `pip install cryptography docker requests` |
| Signature generation slow | Normal (RSA-4096 can take 30-60s first time) |
| Docker volume permission | Run Docker as administrator |
| Report verification fails | Check file not modified; re-sign |

---

## 📞 Support Resources

**Documentation:**
- `README_OSINT_v2.md` - Architecture overview
- `OSINT_LEGAL_GUIDE.md` - Detailed guide
- `OSINT_LAUNCH_CHECKLIST.md` - Launch procedures
- `EXAMPLE_INVESTIGATION_EMOTET.md` - Real example

**Code Files:**
- `osint_legal_engine.py` - Core engine
- `legal_report_generator.py` - Report generation
- `docker_orchestrator_osint.py` - Container management

**External Help:**
- Docker Docs: https://docs.docker.com/
- Python Cryptography: https://cryptography.io/
- Tor Documentation: https://www.torproject.org/

---

## ✅ Compliance Notes

**Before Investigations:**
1. Verify legal authority to conduct investigation
2. Document chain of command approval
3. Confirm all sources are public (OSINT only)
4. Ensure investigation aligns with jurisdiction

**During Investigations:**
1. Document all source URLs
2. Maintain timestamp accuracy
3. Assign confidence levels consistently
4. Keep audit trail of investigative process

**Report Generation:**
1. Select appropriate authority format
2. Verify all IOC sources
3. Confirm signature validity
4. Test report verification before distribution

---

## 🎓 Next Steps

**Beginner:**
1. Read `OSINT_LEGAL_GUIDE.md`
2. Run `VERIFY_OSINT_SETUP.ps1`
3. Study `EXAMPLE_INVESTIGATION_EMOTET.md`

**Intermediate:**
1. Create test investigation
2. Generate practice reports
3. Test all export formats

**Advanced:**
1. Integrate with LE databases
2. Set up automated feeds
3. Create custom investigation templates

---

**Last Updated:** 2026-02-19  
**Status:** Ready for Production Use ✅
