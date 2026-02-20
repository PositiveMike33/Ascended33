"""
pages/hexstrike_tools.py — Streamlit Dashboard for HexStrike Integration

Provides:
  - Tool browser and launcher
  - Job monitoring
  - Result viewer
  - Performance analytics
"""

import json
import logging
from datetime import datetime, timedelta

import streamlit as st
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="HexStrike Tools",
    page_icon="⚔️",
    layout="wide",
)

logger = logging.getLogger(__name__)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .tool-card {
        background: #161b22;
        border: 2px solid #30363d;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
    }
    .tool-card:hover {
        border-color: #58a6ff;
        background: #0d1117;
    }
    .status-running { color: #3fb950; }
    .status-pending { color: #d29922; }
    .status-failed { color: #f85149; }
    .status-completed { color: #3fb950; }
    .metric { font-size: 1.2em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ── Initialize session state ───────────────────────────────────────────────────
if "hexstrike_client" not in st.session_state:
    from mcp.hexstrike_wrapper import HexStrikeClient
    st.session_state.hexstrike_client = HexStrikeClient()

if "worker" not in st.session_state:
    from workers.hexstrike_worker import get_worker
    st.session_state.worker = get_worker()

if "vault_client" not in st.session_state:
    try:
        from vault_sync.vault_api import ObsidianVaultClient
        st.session_state.vault_client = ObsidianVaultClient.from_config()
    except:
        st.session_state.vault_client = None


# ── Header ─────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.title("⚔️ HexStrike Tools")
    st.caption("Security research and vulnerability scanning platform")

with col2:
    health = st.session_state.hexstrike_client.get_info()
    if health:
        st.success("🟢 HexStrike CONNECTED")
    else:
        st.warning("⚠️ HexStrike Connecting...")

with col3:
    if st.button("🔄 Refresh"):
        st.rerun()


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Navigation")
    
    page = st.radio(
        "Select view:",
        ["🚀 Launch Tool", "📊 Monitor Jobs", "📈 Results", "⚙️ Settings"],
        label_visibility="collapsed",
    )
    
    st.markdown("---")
    
    st.markdown("### Server Status")
    if st.session_state.hexstrike_client.is_healthy:
        st.success("✅ Server Healthy")
    elif st.session_state.hexstrike_client.is_reachable:
        st.warning("⚙️ Server Ready")
    else:
        st.info("🔄 Service Initializing...")
    
    info = st.session_state.hexstrike_client.get_info()
    if info:
        st.caption(f"Version: {info.get('version', 'Unknown')}")


# ── Page: Launch Tool ──────────────────────────────────────────────────────────
if page == "🚀 Launch Tool":
    st.header("Launch HexStrike Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Get available tools
        tools = st.session_state.hexstrike_client.get_tools()
        
        # Fallback to default tools if server unreachable
        if not tools:
            tools = ["nmap", "masscan", "nuclei", "nessus", "burpsuite", "zaproxy", 
                     "metasploit", "hashcat", "john", "aircrack-ng", "sqlmap", "hydra",
                     "exploitdb", "shodan", "censys", "shodan-cli", "recon-ng", "theHarvester",
                     "maltego", "spiderfoot", "osint-framework", "inurlbr", "paramspider",
                     "arjun", "wfuzz", "dirsearch", "ffuf", "gobuster", "assetfinder",
                     "subfinder", "amass", "crt-sh", "dnsenum", "dnsrecon", "fierce",
                     "whois", "dig", "nslookup", "enum4linux", "snmp-check", "smtp-user-enum",
                     "vnc-brute", "cifs-enum", "ldap-search", "kerberos-enum", "rpcinfo",
                     "finger", "telnet", "ftp-check", "ssh-scan", "imaps-check", "pops-check",
                     "mssql-check", "mysql-check", "postgres-check", "mongodb-check", "redis-check",
                     "elasticsearch-check", "kafka-check", "rabbitmq-check", "cassandra-check",
                     "docker-enum", "kubernetes-enum", "aws-enum", "azure-enum", "gcp-enum",
                     "s3-scanner", "bucket-finder", "cloud-storage-enum", "iam-enum", "lambda-enum",\n                    \"ssl-scanner\", \"certificate-scanner\", \"subdomain-enumeration\", \"web-scraper\", \"api-tester\",\n                    \"graphql-scanner\", \"swagger-parser\", \"openapi-scanner\", \"jwt-cracker\", \"jwtool\",\n                    \"auth-fuzzer\", \"cors-scanner\", \"crlf-injector\", \"xxe-tester\", \"ssti-scanner\",\n                    \"template-engine-fuzzer\", \"code-injection-tester\", \"command-injection-scanner\", \"ldap-injector\", \"xpath-injector\",\n                    \"mongo-injector\", \"nosql-fuzzer\", \"xml-fuzzer\", \"json-fuzzer\", \"protobuf-fuzzer\",\n                    \"serialization-tester\", \"pickle-scanner\", \"yaml-scanner\", \"toml-scanner\", \"ini-scanner\",\n                    \"java-deserialization-scanner\", \"gadget-finder\", \"ysoserial\", \"marshalsec\", \"jexboss\",\n                    \"struts-PoC\", \"spring-boot-scanner\", \"jsp-shell-finder\", \"aspx-shell-finder\", \"php-shell-finder\",\n                    \"webshell-detector\", \"backdoor-scanner\", \"malware-scanner\", \"rootkit-hunter\", \"chkrootkit\",\n                    \"aide\", \"tripwire\", \"osquery\", \"auditd\", \"falco\", \"wazuh-agent\", \"osquery-logger\",\n                    \"yara-scanner\", \"clamscan\", \"rkhunter\", \"tiger\", \"lynis\", \"openscap\", \"oscap-tool\",\n                    \"inspec\", \"serverspec\", \"molecule\", \"testinfra\", \"goss\", \"compliance-checker\", \"prowler\",\n                    \"cloudmapper\", \"cloudtracker\", \"cartography\", \"dome9\", \"forseti\", \"cloudquery\", \"steampipe\",\n                    \"cloudformation-scanner\", \"terraform-scanner\", \"ansible-scanner\", \"docker-bench\", \"kube-bench\",\n                    \"kube-hunter\", \"kube-score\", \"kubeaudit\", \"kubesec\", \"polaris\", \"falco-rules\", \"tracee\"\n            ]\n            st.info(\"ℹ️ Using default tool set (HexStrike server connecting)\")\n        else:\n            st.markdown(\"### Available Tools\")
            
            selected_tool = st.selectbox(
                "Select tool:",
                tools,
                label_visibility="collapsed",
            )
            
            st.markdown(f"#### {selected_tool.upper()}")
            
            # Tool-specific parameters
            params = {}
            
            if selected_tool.lower() == "nmap":
                params["target"] = st.text_input(
                    "Target",
                    placeholder="192.168.1.0/24 or domain.com",
                    help="IP, CIDR, or domain",
                )
                params["scan_type"] = st.selectbox(
                    "Scan type",
                    ["-sV", "-sC", "-sS", "-sT", "-A"],
                )
                params["timing"] = st.slider("Timing template", 0, 5, 3)
            
            elif selected_tool.lower() == "masscan":
                params["target"] = st.text_input(
                    "Target CIDR",
                    placeholder="10.0.0.0/8",
                )
                params["ports"] = st.text_input(
                    "Ports",
                    value="1-1000",
                )
                params["rate"] = st.slider("Packet rate", 100, 10000, 1000)
            
            elif selected_tool.lower() == "nuclei":
                params["target"] = st.text_input(
                    "Target(s)",
                    placeholder="https://example.com",
                )
                params["templates"] = st.multiselect(
                    "Templates",
                    ["cves", "vulnerabilities", "misconfiguration", "web"],
                )
                params["severity"] = st.multiselect(
                    "Severity levels",
                    ["critical", "high", "medium", "low"],
                )
            
            else:
                st.json({"custom": "parameters"})
    
    with col2:
        st.markdown("### Options")
        
        priority = st.selectbox(
            "Priority",
            ["Normal", "High", "Urgent"],
        )
        
        cache_result = st.checkbox("Cache to Obsidian", value=True)
        
        notify = st.checkbox("Send notification when complete", value=False)
        
        st.markdown("---")
        
        # Launch button
        if st.button("🚀 Launch Task", use_container_width=True, type="primary"):
            
            if not params.get("target"):
                st.error("Please enter a target")
            else:
                from workers.hexstrike_worker import TaskPriority
                
                priority_map = {
                    "Normal": TaskPriority.NORMAL,
                    "High": TaskPriority.HIGH,
                    "Urgent": TaskPriority.URGENT,
                }
                
                task_id = st.session_state.worker.submit_task(
                    tool=selected_tool,
                    params=params,
                    priority=priority_map[priority],
                    cache_result=cache_result,
                    callback=None,
                )
                
                st.success(f"✅ Task submitted: `{task_id}`")
                st.balloons()
                
                # Show tracking info
                st.info(f"Monitor progress in the **Monitor Jobs** tab")


# ── Page: Monitor Jobs ─────────────────────────────────────────────────────────
elif page == "📊 Monitor Jobs":
    st.header("Monitor Running Jobs")
    
    # Refresh rate
    col1, col2 = st.columns([3, 1])
    with col2:
        refresh_interval = st.selectbox("Auto-refresh", ["Off", "5s", "10s", "30s"])
    
    # Get all tasks
    all_tasks = st.session_state.worker.get_all_tasks()
    
    if not all_tasks:
        st.info("No tasks submitted yet")
    else:
        # Statistics
        completed = sum(1 for t in all_tasks.values() if t and t["result"] and t["result"]["status"] == "completed")
        running = sum(1 for t in all_tasks.values() if t and t["result"] and t["result"]["status"] == "running")
        failed = sum(1 for t in all_tasks.values() if t and t["result"] and t["result"]["status"] == "failed")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tasks", len(all_tasks))
        with col2:
            st.metric("Completed", completed, "✅")
        with col3:
            st.metric("Running", running, "🔄")
        with col4:
            st.metric("Failed", failed, "❌")
        
        st.markdown("---")
        
        # Task list
        for task_id, task_info in all_tasks.items():
            if task_info is None:
                continue
            
            status = task_info.get("status", "unknown")
            tool = task_info.get("tool", "Unknown")
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**{tool}** — `{task_id[:8]}`")
            
            with col2:
                if status == "completed":
                    st.success(f"✅ {status}")
                elif status == "running":
                    st.info(f"🔄 {status}")
                elif status == "failed":
                    st.error(f"❌ {status}")
                else:
                    st.warning(f"⏳ {status}")
            
            with col3:
                if status == "running":
                    if st.button("Cancel", key=f"cancel_{task_id}"):
                        st.session_state.worker.cancel_task(task_id)
                        st.rerun()


# ── Page: Results ──────────────────────────────────────────────────────────────
elif page == "📈 Results":
    st.header("HexStrike Results")
    
    tabs = st.tabs(["Recent Jobs", "Tool Stats", "Export"])
    
    with tabs[0]:
        st.markdown("### Recent Job Results")
        
        # Get recent tasks
        all_tasks = st.session_state.worker.get_all_tasks()
        completed_tasks = [
            (tid, t) for tid, t in all_tasks.items()
            if t and t["result"] and t["result"]["status"] == "completed"
        ]
        completed_tasks.sort(key=lambda x: x[1]["created_at"], reverse=True)
        
        if not completed_tasks:
            st.info("No completed jobs yet")
        else:
            for task_id, task_info in completed_tasks[:10]:
                with st.expander(f"{task_info['tool']} — {task_id[:8]}"):
                    result = task_info["result"]
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Status", result.get("status", "—"))
                    with col2:
                        st.metric("Duration", f"{result.get('execution_time', 0):.2f}s")
                    with col3:
                        created = datetime.fromisoformat(task_info["created_at"])
                        st.metric("Age", f"{(datetime.now() - created).total_seconds() / 60:.1f}m ago")
                    
                    if result.get("result"):
                        st.json(result["result"])
    
    with tabs[1]:
        st.markdown("### Tool Statistics")
        
        all_tasks = st.session_state.worker.get_all_tasks()
        
        tool_stats = {}
        for tid, t in all_tasks.items():
            if t is None:
                continue
            tool = t.get("tool", "Unknown")
            if tool not in tool_stats:
                tool_stats[tool] = {"count": 0, "completed": 0, "failed": 0}
            tool_stats[tool]["count"] += 1
            if t["result"] and t["result"]["status"] == "completed":
                tool_stats[tool]["completed"] += 1
            elif t["result"] and t["result"]["status"] == "failed":
                tool_stats[tool]["failed"] += 1
        
        if tool_stats:
            for tool, stats in tool_stats.items():
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(f"{tool} — Total", stats["count"])
                with col2:
                    st.metric(f"{tool} — Success", stats["completed"])
                with col3:
                    success_rate = (stats["completed"] / stats["count"] * 100) if stats["count"] > 0 else 0
                    st.metric(f"{tool} — Rate", f"{success_rate:.1f}%")
        else:
            st.info("No tool statistics available yet")
    
    with tabs[2]:
        st.markdown("### Export Results")
        
        all_tasks = st.session_state.worker.get_all_tasks()
        
        if st.button("Export to JSON"):
            json_data = json.dumps(all_tasks, indent=2, default=str)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"hexstrike-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json",
                mime="application/json",
            )


# ── Page: Settings ─────────────────────────────────────────────────────────────
elif page == "⚙️ Settings":
    st.header("HexStrike Settings")
    
    st.markdown("### Server Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"Base URL: {st.session_state.hexstrike_client.base_url}")
        st.info(f"Timeout: {st.session_state.hexstrike_client.timeout}s")
    
    with col2:
        st.info(f"Max retries: {st.session_state.hexstrike_client.max_retries}")
        st.info(f"Caching: {'Enabled' if st.session_state.hexstrike_client.enable_caching else 'Disabled'}")
    
    st.markdown("---")
    st.markdown("### Worker Configuration")
    
    st.info(f"Active workers: {st.session_state.worker.max_workers}")
    st.info(f"Vault caching: {'Enabled' if st.session_state.worker.vault_path else 'Disabled'}")
    
    st.markdown("---")
    st.markdown("### Actions")
    
    if st.button("Clear cache"):
        st.session_state.hexstrike_client.clear_cache()
        st.success("Cache cleared")
    
    if st.button("Test connection"):
        if st.session_state.hexstrike_client.is_reachable:
            st.success("✅ Connection OK")
        else:
            st.error("❌ Connection failed")


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("🔐 HexStrike Tools | Integrated with Ascended33 Security Research Platform")
