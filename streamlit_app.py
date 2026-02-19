"""
streamlit_app.py — Ascended33 Mission Dashboard

Command center for security research operations:
  - System status (hexstrike-ai, Obsidian Vault, Kali VM)
  - Mission launcher (OSINT, pentest, CTF, dark web scan)
  - Recent reports viewer from Vault
  - Live OSINT results
  - OPSEC verification panel

Run: streamlit run streamlit_app.py
"""

import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ascended33 — Mission Control",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

logging.basicConfig(level=logging.WARNING)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0d1117; }
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
    }
    .status-ok   { color: #3fb950; font-weight: bold; }
    .status-warn { color: #d29922; font-weight: bold; }
    .status-err  { color: #f85149; font-weight: bold; }
    .tag {
        background: #21262d;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 2px 10px;
        font-size: 0.8em;
        margin: 2px;
        display: inline-block;
    }
    h1, h2, h3 { color: #58a6ff; }
    .sidebar .sidebar-content { background: #161b22; }
</style>
""", unsafe_allow_html=True)


# ── Helper: system checks ──────────────────────────────────────────────────────

def _get_hexstrike_url() -> str:
    """Load hexstrike URL from config.yaml (kali_vm.host + mcp_port), fallback to localhost."""
    try:
        import yaml
        cfg_path = Path(__file__).parent / "config" / "config.yaml"
        if cfg_path.exists():
            with cfg_path.open() as f:
                cfg = yaml.safe_load(f)
            # Prefer explicit hexstrike.mcp_url if set
            explicit = cfg.get("hexstrike", {}).get("mcp_url", "")
            if explicit and "localhost" not in explicit:
                return explicit.rstrip("/")
            # Otherwise build from kali_vm settings
            kali = cfg.get("kali_vm", {})
            host = kali.get("host", "")
            port = kali.get("mcp_port", 8888)
            if host and host != "kali-lab":
                return f"http://{host}:{port}"
    except Exception:
        pass
    return "http://localhost:8888"


@st.cache_data(ttl=30)
def check_hexstrike() -> dict:
    try:
        import requests
        url = _get_hexstrike_url()
        r = requests.get(f"{url}/health", timeout=3)
        return {"status": "online", "code": r.status_code, "url": url}
    except Exception as e:
        url = _get_hexstrike_url()
        return {"status": "offline", "error": str(e), "url": url}


@st.cache_data(ttl=15)
def check_docker_containers() -> dict:
    """Check status of Ascended33 Docker containers (tor, kali, hexstrike)."""
    import shutil
    import subprocess

    docker = shutil.which("docker")
    if not docker:
        return {"available": False, "reason": "docker not found in PATH"}

    containers = {
        "tor": "ascended33_tor",
        "kali": "ascended33_kali",
        "hexstrike": "ascended33_hexstrike",
    }
    result: dict = {"available": True}
    for name, cname in containers.items():
        try:
            r = subprocess.run(
                [docker, "inspect", "--format",
                 "{{.State.Status}} {{.State.Health.Status}}", cname],
                capture_output=True, text=True, timeout=5,
            )
            if r.returncode == 0:
                parts = r.stdout.strip().split()
                state = parts[0] if parts else "unknown"
                health = parts[1] if len(parts) > 1 else ""
                result[name] = {"state": state, "health": health}
            else:
                result[name] = {"state": "not found", "health": ""}
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            result[name] = {"state": "error", "health": ""}
    return result


@st.cache_data(ttl=30)
def check_vault() -> dict:
    try:
        import requests
        r = requests.get("http://localhost:27123/", timeout=3)
        return {"status": "online", "code": r.status_code}
    except Exception as e:
        return {"status": "offline", "error": str(e)}


@st.cache_data(ttl=60)
def check_opsec() -> dict:
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from scripts.opsec.vpn_check import verify_opsec
        status = verify_opsec(require_vpn=True, require_tor=False)
        return {
            "safe": status.safe,
            "ip": status.current_ip,
            "tor": status.tor_active,
            "reason": status.reason,
        }
    except Exception as e:
        return {"safe": False, "ip": "unknown", "tor": False, "reason": str(e)}


def status_badge(status: str) -> str:
    if status == "online":
        return '<span class="status-ok">● ONLINE</span>'
    return '<span class="status-err">● OFFLINE</span>'


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ⬡ Ascended33")
    st.markdown("**Mission Control**")
    st.markdown("---")

    # ── Docker containers ─────────────────────────────────────────────────────
    st.markdown("### Docker")
    docker = check_docker_containers()

    if not docker.get("available"):
        st.markdown('<span class="status-warn">⚠ Docker indisponible</span>', unsafe_allow_html=True)
    else:
        def _container_badge(info: dict) -> str:
            state = info.get("state", "unknown")
            health = info.get("health", "")
            if state == "running" and health in ("healthy", ""):
                return '<span class="status-ok">● running</span>'
            if state == "running" and health == "starting":
                return '<span class="status-warn">● starting</span>'
            if state == "not found":
                return '<span class="status-err">● not found</span>'
            return f'<span class="status-err">● {state}</span>'

        tor_info = docker.get("tor", {})
        kali_info = docker.get("kali", {})
        hex_info = docker.get("hexstrike", {})

        st.markdown(f"**Tor:** {_container_badge(tor_info)}", unsafe_allow_html=True)
        if tor_info.get("health") == "healthy":
            st.caption("Circuit actif — trafic anonymisé")
        elif tor_info.get("state") == "running":
            st.caption("Bootstrap en cours…")

        st.markdown(f"**Kali:** {_container_badge(kali_info)}", unsafe_allow_html=True)
        st.markdown(f"**hexstrike:** {_container_badge(hex_info)}", unsafe_allow_html=True)

    st.markdown("---")

    # ── Services ──────────────────────────────────────────────────────────────
    st.markdown("### Services")
    hexstrike = check_hexstrike()
    vault = check_vault()
    opsec = check_opsec()

    st.markdown(
        f"**hexstrike API:** {status_badge(hexstrike['status'])}",
        unsafe_allow_html=True,
    )
    if hexstrike.get("status") == "online":
        st.caption(f"`{hexstrike.get('url', 'localhost:8888')}`")

    st.markdown(
        f"**Obsidian Vault:** {status_badge(vault['status'])}",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── OPSEC ─────────────────────────────────────────────────────────────────
    st.markdown("### OPSEC")
    if opsec.get("safe"):
        st.markdown('<span class="status-ok">● SAFE</span>', unsafe_allow_html=True)
        st.caption(f"IP: `{opsec.get('ip', '?')}` | Tor: {'Oui' if opsec.get('tor') else 'Non'}")
    else:
        st.markdown('<span class="status-warn">⚠ VÉRIFIER</span>', unsafe_allow_html=True)
        st.caption(opsec.get("reason", "Unknown"))

    st.markdown("---")
    st.markdown(f"*{datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    if st.button("🔄 Refresh Status"):
        st.cache_data.clear()
        st.rerun()


# ── Main area tabs ────────────────────────────────────────────────────────────

st.title("⬡ Ascended33 — Mission Control")

tab_launch, tab_osint, tab_reports, tab_opsec, tab_tools = st.tabs([
    "🚀 Launch Mission",
    "🔍 OSINT",
    "📋 Reports",
    "🛡 OPSEC",
    "🔧 Tools",
])


# ── Tab: Launch Mission ───────────────────────────────────────────────────────

with tab_launch:
    st.header("Launch Mission")
    col1, col2 = st.columns(2)

    with col1:
        mission_type = st.selectbox(
            "Mission Type",
            ["OSINT — Domain Recon", "OSINT — Username Hunt", "Breach Check",
             "Dark Web Monitor", "Penetration Test", "CTF Challenge", "Threat Intel"],
        )

        target = st.text_input(
            "Target",
            placeholder="domain.com / username / email / keywords...",
        )

        auth_type = st.selectbox(
            "Authorization",
            ["Personal Research / CTF", "Bug Bounty (in-scope)", "Client Pentest (authorized)"],
        )

    with col2:
        opsec_level = st.selectbox(
            "OPSEC Level",
            ["Standard (VPN)", "Enhanced (VPN + Tor)", "Maximum (full persona)"],
        )

        output_dest = st.multiselect(
            "Output",
            ["Print to dashboard", "Save to Vault", "Local file"],
            default=["Print to dashboard", "Save to Vault"],
        )

        st.markdown("#### Authorization Confirmation")
        confirmed = st.checkbox(
            "I confirm this target is within authorized scope",
            value=False,
        )

    st.markdown("---")

    if st.button("▶ Launch Mission", type="primary", disabled=not (target and confirmed)):
        if not opsec.get("safe") and opsec_level != "Standard (VPN)":
            st.error("⛔ OPSEC check failed. Verify VPN/Tor before launching.")
        else:
            with st.spinner(f"Running {mission_type} on {target}..."):
                results_output = ""
                try:
                    if "Domain Recon" in mission_type:
                        from scripts.osint.domain_recon import DomainRecon
                        recon = DomainRecon(target)
                        results = recon.run_all()
                        results_output = results.summary()

                    elif "Username Hunt" in mission_type:
                        from scripts.osint.social_footprint import SocialFootprint
                        sf = SocialFootprint()
                        results = sf.check_username(target)
                        results_output = results.summary()

                    elif "Breach Check" in mission_type:
                        from scripts.osint.breach_check import BreachChecker
                        checker = BreachChecker()
                        result = checker.check_domain(target)
                        results_output = checker.format_report_section([result])

                    elif "Dark Web" in mission_type:
                        from scripts.osint.dark_web_monitor import DarkWebMonitor
                        monitor = DarkWebMonitor(
                            keywords=target.split(","),
                            use_tor="Tor" in opsec_level,
                        )
                        result = monitor.scan()
                        results_output = result.summary()

                    else:
                        results_output = (
                            f"Mission type '{mission_type}' requires hexstrike-ai.\n"
                            f"Ensure hexstrike-ai MCP server is running at localhost:8888."
                        )

                    st.success("Mission complete.")
                    st.markdown("### Results")
                    st.markdown(results_output)

                    if "Save to Vault" in output_dest and results_output:
                        try:
                            from vault_sync.sync import VaultSync
                            sync = VaultSync()
                            note_type = "osint" if "OSINT" in mission_type else "threat_intel"
                            path = sync.push_report(note_type, results_output, target=target)
                            st.success(f"Saved to Vault: `{path}`")
                        except Exception as ve:
                            st.warning(f"Vault save failed: {ve}")

                except Exception as e:
                    st.error(f"Mission failed: {e}")
                    st.exception(e)
    elif not confirmed and target:
        st.warning("⚠ Please confirm authorization before launching.")


# ── Tab: OSINT ────────────────────────────────────────────────────────────────

with tab_osint:
    st.header("OSINT Tools")

    osint_col1, osint_col2 = st.columns(2)

    with osint_col1:
        st.subheader("Domain Recon")
        domain_input = st.text_input("Domain", key="osint_domain", placeholder="example.com")
        if st.button("Run Domain Recon", key="btn_domain"):
            with st.spinner("Running passive recon..."):
                try:
                    from scripts.osint.domain_recon import DomainRecon
                    r = DomainRecon(domain_input).run_all()
                    st.markdown(f"**DNS A Records**: `{', '.join(r.dns.a_records) or 'none'}`")
                    st.markdown(f"**Registrar**: {r.whois.registrar}")
                    st.markdown(f"**Org**: {r.whois.org} | **Country**: {r.whois.country}")
                    st.markdown(f"**Subdomains (crt.sh)**: {len(r.subdomains)}")
                    if r.subdomains:
                        with st.expander("View subdomains"):
                            for s in r.subdomains[:50]:
                                st.code(s.name)
                    st.markdown(f"**Wayback URLs**: {len(r.wayback_urls)}")
                except Exception as e:
                    st.error(str(e))

        st.subheader("Breach Check")
        breach_domain = st.text_input("Domain/Email", key="breach_input", placeholder="example.com")
        if st.button("Check Breaches", key="btn_breach"):
            with st.spinner("Checking HIBP..."):
                try:
                    from scripts.osint.breach_check import BreachChecker
                    checker = BreachChecker()
                    result = checker.check_domain(breach_domain)
                    if result.breaches_found:
                        st.error(f"Found in {len(result.breaches_found)} breach(es)")
                        for b in result.breaches_found:
                            st.markdown(f"- **{b.name}** ({b.breach_date}) — {b.pwn_count:,} records")
                    else:
                        st.success("No known breaches found for this domain")
                except Exception as e:
                    st.error(str(e))

    with osint_col2:
        st.subheader("Username Hunt")
        username_input = st.text_input("Username", key="osint_user", placeholder="target_username")
        if st.button("Search Platforms", key="btn_user"):
            with st.spinner("Checking platforms..."):
                try:
                    from scripts.osint.social_footprint import SocialFootprint
                    sf = SocialFootprint(delay=0.3)
                    results = sf.check_username(username_input)
                    found = results.found_on
                    not_found = results.not_found_on
                    st.success(f"Found on {len(found)} platforms")
                    for p in found:
                        url = next(r.url for r in results.platform_results if r.platform == p and r.found)
                        st.markdown(f"✅ **{p}**: {url}")
                    if not_found:
                        with st.expander(f"Not found on {len(not_found)} platforms"):
                            st.write(", ".join(not_found))
                except Exception as e:
                    st.error(str(e))

        st.subheader("Password Pwned Check")
        pw_input = st.text_input("Password to check", type="password", key="pw_check",
                                  help="Uses k-anonymity — password never leaves this machine")
        if st.button("Check Password", key="btn_pw"):
            if pw_input:
                try:
                    from scripts.osint.breach_check import BreachChecker
                    result = BreachChecker().check_password(pw_input)
                    if result.is_pwned:
                        st.error(f"⚠ PWNED — Seen {result.occurrence_count:,} times | Risk: {result.risk_level}")
                    else:
                        st.success("✅ Not found in known breach databases")
                except Exception as e:
                    st.error(str(e))


# ── Tab: Reports ──────────────────────────────────────────────────────────────

with tab_reports:
    st.header("Reports")
    st.markdown("Generate structured reports and save to Obsidian Vault.")

    rep_col1, rep_col2 = st.columns([2, 1])
    with rep_col1:
        rep_type = st.selectbox("Report Type", ["osint", "pentest", "threat_intel", "ctf"])
        rep_target = st.text_input("Target / Engagement Name", key="rep_target")
        rep_notes = st.text_area("Additional notes / findings", height=150)

    with rep_col2:
        rep_output = st.selectbox("Output destination", ["vault", "local", "both"])
        st.markdown("")
        st.markdown("")
        if st.button("📄 Generate Report", type="primary"):
            if rep_target:
                try:
                    from scripts.reporting.report_generator import generate_report
                    content = generate_report(
                        rep_type,
                        {
                            "{{target}}": rep_target,
                            "{{client_name}}": rep_target,
                            "{{executive_summary}}": rep_notes or "To be completed.",
                            "{{authorization_type}}": "Research",
                            "{{opsec_level}}": "Standard",
                        },
                        output=rep_output,
                    )
                    st.success(f"Report generated ({len(content):,} chars) → {rep_output}")
                    with st.expander("Preview report"):
                        st.markdown(content[:3000] + ("..." if len(content) > 3000 else ""))
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("Enter a target/engagement name.")

    st.markdown("---")
    st.subheader("Local Output Files")
    output_dir = Path("output")
    if output_dir.exists():
        files = sorted(output_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        if files:
            for f in files[:10]:
                with st.expander(f.name):
                    st.markdown(f.read_text(encoding="utf-8"))
        else:
            st.info("No local reports yet. Generate one above.")
    else:
        st.info("output/ directory not created yet.")


# ── Tab: OPSEC ────────────────────────────────────────────────────────────────

with tab_opsec:
    st.header("OPSEC Panel")

    op_col1, op_col2 = st.columns(2)
    with op_col1:
        st.subheader("Current Status")
        if st.button("🔄 Run OPSEC Check"):
            st.cache_data.clear()
            st.rerun()

        opsec_fresh = check_opsec()
        if opsec_fresh.get("safe"):
            st.success("✅ OPSEC status: SAFE")
        else:
            st.error("⛔ OPSEC status: UNSAFE")

        st.json(opsec_fresh)

    with op_col2:
        st.subheader("Pre-Operation Checklist")
        st.markdown("""
**Before ANY active operation:**
- [ ] VPN is active and connected
- [ ] Tor is running (for dark web / high-sensitivity ops)
- [ ] No personal accounts logged in on test browser
- [ ] Target is confirmed in-scope (authorization documented)
- [ ] Operation logged in Vault with start timestamp
- [ ] Kali VM network interface verified
        """)

        st.subheader("OPSEC Levels")
        st.markdown("""
| Level | Use For | Requirements |
|-------|---------|--------------|
| Standard | Passive OSINT | VPN active |
| Enhanced | Active recon | VPN + Tor |
| Maximum | Dark web, sensitive | VPN + Tor + dedicated persona |
        """)


# ── Tab: Tools ────────────────────────────────────────────────────────────────

with tab_tools:
    st.header("Tools & Integrations")

    tools_col1, tools_col2 = st.columns(2)

    with tools_col1:
        st.subheader("hexstrike-ai")
        hx_status = check_hexstrike()
        if hx_status["status"] == "online":
            st.success(f"hexstrike-ai en ligne — `{hx_status.get('url', 'localhost:8888')}`")

            from mcp.hexstrike_client import HexStrikeClient
            client = HexStrikeClient()
            tools = client.list_tools()

            if tools:
                st.metric("Outils disponibles", len(tools))
                with st.expander("Parcourir les outils"):
                    for t in tools[:30]:
                        st.markdown(f"- **{t.get('name')}**: {t.get('description', '')}")
            else:
                st.info(
                    "Listing d'outils non disponible via l'API courante. "
                    "hexstrike-ai est actif et utilisable depuis les scripts."
                )

            st.markdown("**Commandes Docker utiles :**")
            st.code(
                "docker compose logs -f hexstrike    # logs en direct\n"
                "docker compose exec hexstrike bash   # shell interactif\n"
                "docker compose restart hexstrike     # redémarrer",
                language="bash",
            )
        else:
            st.error("hexstrike-ai est hors ligne")
            st.markdown("**Pour démarrer :**")
            st.code(
                "# Depuis la racine du repo Ascended33\n"
                "docker compose up -d hexstrike\n\n"
                "# Vérifier les logs\n"
                "docker compose logs -f hexstrike",
                language="bash",
            )
            st.info("Tor doit être démarré avant hexstrike (depends_on: service_healthy).")
            st.code("docker compose up -d tor && docker compose up -d hexstrike", language="bash")

    with tools_col2:
        st.subheader("Obsidian Vault")
        vault_status = check_vault()
        if vault_status["status"] == "online":
            st.success("Obsidian Vault REST API online at localhost:27123")
            if st.button("🔄 Full Vault Sync"):
                with st.spinner("Syncing..."):
                    try:
                        from vault_sync.sync import VaultSync
                        sync = VaultSync()
                        result = sync.full_sync()
                        st.success(f"Sync complete: {len(result.pulled)} templates, {result.indexed} notes indexed")
                    except Exception as e:
                        st.error(str(e))
        else:
            st.error("Obsidian Vault API offline")
            st.markdown("""
**To connect:**
1. Open Obsidian with `D:\\Vault`
2. Settings → Community Plugins → Local REST API
3. Enable plugin & copy API key to `config/config.yaml`
            """)

        st.subheader("Vault Quick Search")
        search_query = st.text_input("Search notes", placeholder="target name, tag, keyword...")
        if st.button("Search") and search_query:
            try:
                from vault_sync.sync import VaultSync
                sync = VaultSync()
                results = sync.search_notes(search_query)
                if results:
                    for note in results[:20]:
                        st.markdown(f"- `{note.path}` — {note.title} [{note.note_type}]")
                else:
                    st.info("No notes found.")
            except Exception as e:
                st.warning(str(e))
