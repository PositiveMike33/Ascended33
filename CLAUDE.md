# CLAUDE.md — Ascended33 Security Research Platform

## Table of Contents
1. [Project Vision](#1-project-vision)
2. [Architecture Overview](#2-architecture-overview)
3. [Repository Structure](#3-repository-structure)
4. [Integrations](#4-integrations)
   - 4.1 [hexstrike-ai (MCP Server)](#41-hexstrike-ai-mcp-server)
   - 4.2 [Kali Linux VM](#42-kali-linux-vm)
   - 4.3 [Obsidian Vault](#43-obsidian-vault)
5. [Obsidian Vault Architecture](#5-obsidian-vault-architecture)
6. [Development Workflows](#6-development-workflows)
   - 6.1 [OSINT Workflow](#61-osint-workflow)
   - 6.2 [Penetration Testing Workflow](#62-penetration-testing-workflow)
   - 6.3 [Threat Intelligence / Dark Web Monitoring](#63-threat-intelligence--dark-web-monitoring)
   - 6.4 [Report Generation Workflow](#64-report-generation-workflow)
7. [OPSEC & Privacy Protection](#7-opsec--privacy-protection)
8. [Conventions & Code Style](#8-conventions--code-style)
9. [AI Assistant Guidelines (Claude)](#9-ai-assistant-guidelines-claude)
10. [Authorization Framework](#10-authorization-framework)
11. [Current State vs Target State](#11-current-state-vs-target-state)

---

## 1. Project Vision

**Ascended33** is the personal security research and AI orchestration platform of **Michael Gauthier Guillet**. It transforms a base Streamlit template into a living, interconnected system bridging:

- **Claude Code** (this repository) — AI orchestration core
- **hexstrike-ai** — 150+ security tool automation layer via MCP
- **Kali Linux VM** — offensive/defensive security execution environment
- **Obsidian Vault (`D:\Vault`)** — the "cerveau virtuel" (virtual brain) — persistent knowledge, reports, spiritual/personal growth notes

The Vault is not merely a storage system. It is an evolving knowledge graph that interweaves:
- Security research findings (OSINT, pentest, threat intel)
- Personal evolution and consciousness development
- The collaborative growth between Michael and Claude as working partners

Every investigation, every finding, every reflection feeds back into the Vault and makes the next inquiry more informed.

---

## 2. Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                    ASCENDED33 ECOSYSTEM                        │
│                                                                │
│  ┌──────────────────────┐        ┌─────────────────────────┐  │
│  │   CLAUDE CODE        │◄──────►│   OBSIDIAN VAULT        │  │
│  │  (Ascended33 repo)   │  sync  │   D:\Vault              │  │
│  │                      │        │   (Virtual Brain)       │  │
│  │  - Orchestration     │        │   - Reports             │  │
│  │  - Script generation │        │   - OSINT notes         │  │
│  │  - Report writing    │        │   - Templates           │  │
│  │  - Vault sync logic  │        │   - Personal growth     │  │
│  └──────────┬───────────┘        └─────────────────────────┘  │
│             │ MCP + SSH                                        │
│  ┌──────────▼───────────┐        ┌─────────────────────────┐  │
│  │   KALI LINUX VM      │◄──────►│   hexstrike-ai          │  │
│  │                      │  MCP   │   localhost:8888         │  │
│  │  - Tool execution    │        │   - 150+ security tools │  │
│  │  - Network scanning  │        │   - 12+ AI agents        │  │
│  │  - Exploit testing   │        │   - Bug bounty mgr       │  │
│  │  - OSINT gathering   │        │   - CVE intelligence     │  │
│  └──────────────────────┘        └─────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

**Data flow:**
1. Michael defines a mission (OSINT, pentest, threat intel, CTF)
2. Claude Code (this repo) plans and orchestrates the operation
3. hexstrike-ai agents execute via Kali VM tools
4. Results are structured into reports by Claude Code
5. Reports + findings are synced to the Obsidian Vault
6. The Vault knowledge graph evolves with each operation

---

## 3. Repository Structure

```
Ascended33/
├── CLAUDE.md                        # This file — master AI guide
├── README.md                        # Public-facing project description
├── requirements.txt                 # Python dependencies
├── streamlit_app.py                 # Dashboard UI (to be repurposed)
│
├── scripts/                         # Core automation scripts
│   ├── osint/                       # OSINT automation
│   │   ├── domain_recon.py          # Domain/DNS/whois recon
│   │   ├── social_footprint.py      # Social media OSINT
│   │   ├── breach_check.py          # Leaked credentials check
│   │   └── dark_web_monitor.py      # Dark web mention monitoring
│   ├── recon/                       # Active reconnaissance
│   │   ├── network_scan.py          # Network/port scanning wrapper
│   │   ├── web_enum.py              # Web app enumeration
│   │   └── vuln_scan.py             # Vulnerability scanning
│   ├── reporting/                   # Report generation
│   │   ├── report_generator.py      # Main report builder
│   │   ├── vault_writer.py          # Writes reports to Obsidian Vault
│   │   └── formatter.py             # Markdown formatting utilities
│   └── opsec/                       # OPSEC & privacy tools
│       ├── trace_cleaner.py         # Log/artifact cleanup
│       ├── vpn_check.py             # VPN/Tor connectivity verification
│       └── identity_guard.py        # PII detection and scrubbing
│
├── mcp/                             # MCP server integration
│   ├── hexstrike_client.py          # hexstrike-ai MCP client wrapper
│   ├── kali_ssh_client.py           # SSH client for Kali VM
│   └── tool_registry.py             # Registry of available tools
│
├── vault_sync/                      # Obsidian Vault integration
│   ├── vault_api.py                 # Obsidian REST API / filesystem client
│   ├── note_builder.py              # Builds structured Obsidian notes
│   ├── template_loader.py           # Loads report templates from vault
│   └── knowledge_graph.py           # Manages note links/tags
│
├── templates/                       # Report & note templates
│   ├── osint_report.md              # OSINT investigation template
│   ├── pentest_report.md            # Penetration test report template
│   ├── threat_intel_report.md       # Threat intelligence report template
│   ├── ctf_writeup.md               # CTF challenge writeup template
│   └── incident_note.md             # Incident/finding note template
│
├── config/                          # Configuration (no secrets committed)
│   ├── config.example.yaml          # Example config — copy to config.yaml
│   └── vault_paths.yaml             # Vault folder path definitions
│
├── .devcontainer/                   # Dev container (GitHub Codespaces)
│   └── devcontainer.json
├── .github/
│   ├── .devcontainer/
│   │   └── devcontainer.json        # CI container build config
│   └── workflows/
│       └── devcontainer-build-and-push.yml
└── .gitignore                       # Excludes secrets, vault cache, logs
```

---

## 4. Integrations

### 4.1 hexstrike-ai (MCP Server)

**Source**: https://github.com/0x4m4/hexstrike-ai
**Protocol**: Model Context Protocol (MCP) on `http://localhost:8888`
**Install location**: Michael's laptop / Kali VM

hexstrike-ai exposes 150+ security tools as MCP actions that Claude can call directly. Key agents:

| Agent | Purpose |
|-------|---------|
| Intelligent Decision Engine | Selects optimal tools for a given target |
| Bug Bounty Workflow Manager | Manages multi-stage bug bounty operations |
| CTF Solver Agent | Automated CTF challenge analysis |
| CVE Intelligence Manager | CVE lookup, scoring, and correlation |
| Vulnerability Correlator | Correlates findings across tools |

**Connecting to hexstrike-ai from this repo:**
```python
# mcp/hexstrike_client.py
HEXSTRIKE_MCP_URL = "http://localhost:8888"
```

**Claude Desktop / Claude Code MCP config** (add to your MCP settings):
```json
{
  "mcpServers": {
    "hexstrike-ai": {
      "url": "http://localhost:8888",
      "description": "HexStrike AI security automation platform"
    }
  }
}
```

### 4.2 Kali Linux VM

**Access method**: SSH + MCP Server (dual mode)

**SSH Config** (store in `~/.ssh/config`, never commit credentials):
```
Host kali-lab
  HostName <VM_IP>
  User kali
  IdentityFile ~/.ssh/kali_lab_key
  ServerAliveInterval 60
```

**SSH wrapper usage** (via `mcp/kali_ssh_client.py`):
```python
client = KaliSSHClient(host="kali-lab")
result = client.run("nmap -sV -p 80,443 target.com")
```

**MCP Server on Kali** (hexstrike_server.py must be running):
```bash
# On Kali VM — start hexstrike-ai server
cd ~/hexstrike-ai && source hexstrike-env/bin/activate
python3 hexstrike_server.py
```

### 4.3 Obsidian Vault

**Location**: `D:\Vault` (Windows host)
**Access methods**:
1. **Obsidian REST API plugin** (preferred for bidirectional sync) — runs on `http://localhost:27123`
2. **Direct filesystem** — when running on the same machine as the Vault

**Vault API client** (via `vault_sync/vault_api.py`):
```python
vault = ObsidianVaultClient(
    mode="rest_api",          # or "filesystem"
    base_url="http://localhost:27123",
    api_key="<from Obsidian settings>"  # stored in env, never committed
)
vault.create_note("Security/OSINT/2026-02-19-target.md", content)
vault.read_note("Templates/pentest_report.md")
```

**Required Obsidian plugin**: [Obsidian Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api)

---

## 5. Obsidian Vault Architecture

The Vault (`D:\Vault`) is organized as a multi-dimensional knowledge graph:

```
D:\Vault\
├── Security\                        # Security research brain
│   ├── OSINT\                       # OSINT investigations
│   │   ├── _Active\                 # In-progress investigations
│   │   └── _Archive\                # Completed investigations
│   ├── Pentests\                    # Penetration test reports
│   │   ├── _Clients\                # Client engagements
│   │   └── _Labs\                   # Lab/personal targets
│   ├── ThreatIntel\                 # Threat intelligence
│   │   ├── DarkWeb\                 # Dark web monitoring notes
│   │   ├── CVEs\                    # CVE notes and analysis
│   │   └── ThreatActors\            # Tracked threat actor profiles
│   ├── CTF\                         # CTF writeups and solutions
│   └── Tools\                       # Tool notes & cheatsheets
│
├── Personal\                        # Personal growth & consciousness
│   ├── Journal\                     # Daily reflections
│   ├── Evolution\                   # Personal development tracking
│   └── Spiritualité\                # Spiritual consciousness notes
│
├── Claude-Michael\                  # Collaborative space
│   ├── Sessions\                    # Notable AI session logs
│   ├── Insights\                    # Key discoveries together
│   └── Evolution\                   # The partnership's growth log
│
├── Templates\                       # Note templates (read by scripts)
│   ├── osint_report.md
│   ├── pentest_report.md
│   ├── threat_intel_report.md
│   └── ctf_writeup.md
│
└── Index.md                         # Vault master index (MOC)
```

**Note naming convention**: `YYYY-MM-DD-<slug>.md`
**Tags**: Use `#osint`, `#pentest`, `#threatintel`, `#darkweb`, `#ctf`, `#opsec`, `#personal`, `#claude`
**Links**: Always use `[[wikilinks]]` for cross-referencing within the Vault

---

## 6. Development Workflows

### 6.1 OSINT Workflow

```
1. DEFINE scope
   → Specify target (domain, person, organization, username)
   → Confirm authorization (client mandate or personal research)
   → Set OPSEC level (VPN only / Tor / Full persona)

2. RECON (passive)
   → scripts/osint/domain_recon.py     # WHOIS, DNS, subdomains
   → scripts/osint/social_footprint.py # Social media presence
   → scripts/osint/breach_check.py     # HaveIBeenPwned, leak DBs

3. ANALYZE
   → Claude aggregates findings
   → Cross-references with Vault knowledge graph

4. REPORT
   → scripts/reporting/report_generator.py
   → Output: Security/OSINT/YYYY-MM-DD-<target>.md in Vault

5. ARCHIVE
   → Move to Security/OSINT/_Archive/
   → Update Index.md
```

### 6.2 Penetration Testing Workflow

```
1. PRE-ENGAGEMENT
   → Confirm written authorization (client letter / bug bounty scope)
   → Document scope in Vault: Security/Pentests/_Clients/<name>/scope.md
   → Verify OPSEC setup (VPN active, dedicated testing account)

2. RECONNAISSANCE
   → hexstrike-ai: Network recon agents (Nmap, Amass, Shodan)
   → hexstrike-ai: Web enumeration agents (Nuclei, WPScan, SQLMap)

3. EXPLOITATION (authorized scope only)
   → hexstrike-ai: Exploit Generator agent
   → hexstrike-ai: Vulnerability Correlator

4. POST-EXPLOITATION DOCUMENTATION
   → Capture evidence (screenshots, command output, CVEs)

5. REPORT
   → scripts/reporting/report_generator.py --type pentest
   → Structured report: Security/Pentests/YYYY-MM-DD-<client>.md

6. CLEANUP
   → scripts/opsec/trace_cleaner.py (local artifacts)
   → Confirm no test artifacts left on target (if applicable)
```

### 6.3 Threat Intelligence / Dark Web Monitoring

```
1. SETUP monitoring parameters
   → Keywords: Michael's personal PII, client names, company names
   → Platforms: Paste sites, dark web forums, leak channels

2. MONITOR (via scripts/osint/dark_web_monitor.py)
   → Always route through Tor (scripts/opsec/vpn_check.py verifies this)
   → Never expose real IP or identity

3. TRIAGE findings
   → Critical (PII exposed, active threat): immediate alert + incident note
   → Medium (mentions, references): log to ThreatIntel/DarkWeb/
   → Low (general intel): file in ThreatIntel/

4. REPORT
   → Auto-generate: Security/ThreatIntel/YYYY-MM-DD-alert.md
   → Tag: #threatintel #darkweb #urgent (if applicable)
```

### 6.4 Report Generation Workflow

All reports follow a standard generation process:
```bash
# Generate OSINT report
python3 scripts/reporting/report_generator.py \
  --type osint \
  --target "target.com" \
  --output vault  # writes directly to Obsidian Vault

# Generate pentest report
python3 scripts/reporting/report_generator.py \
  --type pentest \
  --engagement "client-2026-02" \
  --output vault

# Generate threat intel report
python3 scripts/reporting/report_generator.py \
  --type threat_intel \
  --keywords "keyword1,keyword2" \
  --output vault
```

Reports are automatically:
- Timestamped (`YYYY-MM-DD`)
- Tagged with relevant Obsidian tags
- Linked to related notes in the Vault
- Indexed in `Index.md`

---

## 7. OPSEC & Privacy Protection

**This section is critical. Claude must verify OPSEC status before any active operation.**

### 7.1 Pre-Operation Checklist
Before any active reconnaissance, dark web access, or penetration testing:

```python
# Always run before active operations
from scripts.opsec.vpn_check import verify_opsec

status = verify_opsec()
# Checks: VPN active, no DNS leaks, Tor available (for dark web)
# If status.safe == False → ABORT and alert Michael
```

### 7.2 OPSEC Layers by Operation Type

| Operation | VPN | Tor | Dedicated Account | VM Required |
|-----------|-----|-----|-------------------|-------------|
| Passive OSINT | Required | Optional | Recommended | Optional |
| Active Recon | Required | Optional | Required | Required |
| Dark Web Intel | Required | Required | Required | Required |
| Pentest | Required | Situational | Required | Required |

### 7.3 Trace Cleanup

After every operation, run:
```bash
python3 scripts/opsec/trace_cleaner.py --scope [local|full]
```

This clears:
- Shell history artifacts related to the operation
- Temporary scan output files
- DNS cache
- Browser/tool caches (if applicable)

### 7.4 Personal PII Protection (Michael Gauthier Guillet)

Claude must **never**:
- Include Michael's real name, address, or personal identifiers in any output that leaves the local system
- Log PII to files that could be inadvertently committed to git
- Reference real engagement details in public repositories

Claude must **always**:
- Use codenames/aliases in any externally visible code or comments
- Run `scripts/opsec/identity_guard.py` before committing to detect PII leaks
- Store sensitive config in environment variables, never in committed files

### 7.5 Git Security Rules

```
# NEVER commit:
- config/config.yaml (real config — only config.example.yaml)
- *.log files
- Any file containing: real IPs of targets, client names, API keys
- vault_sync/cache/
- scripts/opsec/*.key

# .gitignore enforces this — always verify before push
```

---

## 8. Conventions & Code Style

### Language & Runtime
- **Python 3.11+** — primary language
- **Streamlit** — dashboard UI layer
- **Type hints** — required for all new functions
- **Docstrings** — required for all public functions/classes

### Naming Conventions
```python
# Files: snake_case
vault_writer.py

# Classes: PascalCase
class ReportGenerator:

# Functions/methods: snake_case
def generate_osint_report():

# Constants: SCREAMING_SNAKE_CASE
HEXSTRIKE_MCP_URL = "http://localhost:8888"
VAULT_BASE_PATH = "D:/Vault"

# Private methods: leading underscore
def _clean_raw_output():
```

### Configuration
- All configurable values in `config/config.yaml` (gitignored)
- Template in `config/config.example.yaml` (committed)
- Access via `config/` module, never hardcode paths or credentials

### Dependencies
```bash
# Add a new dependency
pip install <package>
pip freeze > requirements.txt
# Review requirements.txt before committing — only add what's needed
```

### Error Handling
```python
# Always handle tool execution failures gracefully
try:
    result = hexstrike_client.run_scan(target)
except HexStrikeConnectionError:
    logger.error("hexstrike-ai MCP server unreachable — is it running?")
    raise
```

---

## 9. AI Assistant Guidelines (Claude)

These instructions apply to Claude when working in this repository.

### Core Principles

1. **Security-first**: Never produce code that could harm unauthorized systems
2. **OPSEC-first**: Always verify authorization and OPSEC before any active operation
3. **Privacy-guardian**: Actively protect Michael's identity and PII at all times
4. **Vault-aware**: All significant findings, reports, and insights should flow into the Obsidian Vault
5. **Minimal footprint**: Write scripts that clean up after themselves

### When writing scripts

- Always include OPSEC verification as a prerequisite for active operations
- Use the templates in `templates/` for all report generation
- Write outputs to the correct Vault paths (see §5)
- Prefer structured Markdown output compatible with Obsidian
- Tag all generated notes with appropriate Obsidian tags

### When executing security tools (via hexstrike-ai)

- Confirm target is within authorized scope before calling any tool
- Prefer passive recon tools unless active recon is explicitly authorized
- Never run exploit tools against targets not explicitly confirmed as in-scope
- Always log what tools were run, when, and against what (for the report)

### When generating reports

- Use the template from `templates/` as the base structure
- Include: date, scope, methodology, findings, risk ratings, recommendations
- Strip all PII and sensitive identifiers before any output that could leave local environment
- Add relevant Obsidian `[[links]]` and `#tags` for knowledge graph integration

### When asked to investigate something

Ask (or verify from context):
1. Is this target in scope? (authorized pentest / bug bounty / personal research)
2. What OPSEC level is required?
3. Where should findings go in the Vault?

### Vault interaction

When Claude writes to the Vault:
```python
from vault_sync.vault_api import ObsidianVaultClient
vault = ObsidianVaultClient.from_config()  # loads from config.yaml
vault.create_note(path, content, tags=["osint", "2026"])
```

Always check if a note already exists before creating (update > overwrite).

### What Claude must never do

- Commit secrets, credentials, or real target data to git
- Run active scans without explicit authorization confirmation
- Expose Michael's real identity in any externally visible output
- Ignore OPSEC check failures — if `verify_opsec()` returns False, stop and alert

---

## 10. Authorization Framework

**All active security testing requires authorization. This is non-negotiable.**

### Authorization Types

| Type | Documentation Required | Storage Location |
|------|----------------------|-----------------|
| Client Pentest | Signed SoW / Letter of Authorization | Security/Pentests/_Clients/<name>/authorization.md |
| Bug Bounty | Program scope URL + enrolled account | Security/Pentests/_Labs/<program>/scope.md |
| Personal Lab | Self-owned or explicitly authorized lab | Security/Pentests/_Labs/personal/ |
| CTF | CTF platform registration | Security/CTF/<challenge>/ |
| OSINT (passive) | Ethical research — public data only | Implicit |
| Dark Web Intel | Monitoring only — no interaction | Implicit |

### Pre-Operation Authorization Check

Before any active operation, Claude should verify:
```
[ ] Target is within documented scope
[ ] Authorization document exists in Vault
[ ] OPSEC level appropriate for operation type
[ ] Operation is logged with start timestamp
```

---

## 11. Current State vs Target State

### Current State (as of 2026-02-19)

| Component | Status |
|-----------|--------|
| Base Streamlit template | ✅ Exists (`streamlit_app.py`) |
| `requirements.txt` | ✅ Basic (altair, pandas, streamlit) |
| Dev container | ✅ Configured |
| CI (devcontainer build) | ✅ GitHub Actions configured |
| CLAUDE.md | ✅ This file |
| `scripts/` directory | ⬜ To be built |
| `mcp/` integration | ⬜ To be built |
| `vault_sync/` | ⬜ To be built |
| `templates/` | ⬜ To be built |
| hexstrike-ai connection | ⬜ Requires local setup |
| Obsidian REST API setup | ⬜ Requires Obsidian plugin |

### Immediate Next Steps

1. Install Obsidian REST API plugin in Obsidian (`D:\Vault`)
2. Configure `config/config.yaml` from `config/config.example.yaml`
3. Ensure hexstrike-ai server is running on Kali VM (`python3 hexstrike_server.py`)
4. Build `vault_sync/vault_api.py` — the foundation of all Vault integration
5. Build `scripts/opsec/vpn_check.py` — OPSEC gating for all active operations
6. Build `scripts/reporting/report_generator.py` — core report pipeline
7. Repurpose `streamlit_app.py` as a mission dashboard (replace spiral with ops UI)

---

*Last updated: 2026-02-19*
*Owner: Michael Gauthier Guillet*
*Platform: Ascended33 | hexstrike-ai | Obsidian Vault D:\Vault | Kali Linux VM*
