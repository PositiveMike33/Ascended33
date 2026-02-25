import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
import json
from pathlib import Path
import sys
import asyncio

# Add Ascended33 to path for imports
sys.path.insert(0, 'D:/Vault/Vault/_INFRASTRUCTURE/Ascended33')

try:
    from openwebui_integration import (
        HexStrikeOpenWebUIIntegration,
        CloudModelProvider,
        OpenWebUIClient,
        VaultReportWriter
    )
    OPENWEBUI_AVAILABLE = True
except ImportError:
    OPENWEBUI_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="HexStrike Operations Center",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #1f1f1f;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00d4ff;
        margin: 10px 0;
    }
    .status-active { color: #00ff00; }
    .status-inactive { color: #ff4444; }
    .status-warning { color: #ffaa00; }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("## 🎯 HexStrike Operations Center")
st.sidebar.markdown("---")

if OPENWEBUI_AVAILABLE:
    nav_options = [
        "📊 Dashboard",
        "🔍 Investigations",
        "🤖 AI Analysis (OpenWebUI)",
        "🧠 Vault Intelligence",
        "📈 Reports & Analytics",
        "⚙️ Configuration",
        "📚 Documentation"
    ]
else:
    nav_options = [
        "📊 Dashboard",
        "🔍 Investigations",
        "🧠 Vault Intelligence",
        "📈 Reports & Analytics",
        "⚙️ Configuration",
        "📚 Documentation"
    ]

nav_option = st.sidebar.radio("Navigation", nav_options)

# Vault path check
vault_path = Path("D:/Vault/Vault") if os.path.exists("D:/Vault/Vault") else (Path("/vault") if os.path.exists("/vault") else Path("."))
has_vault = vault_path.exists()

# Initialize session state
if 'openwebui_integration' not in st.session_state:
    st.session_state.openwebui_integration = HexStrikeOpenWebUIIntegration() if OPENWEBUI_AVAILABLE else None

if 'vault_writer' not in st.session_state:
    st.session_state.vault_writer = VaultReportWriter() if OPENWEBUI_AVAILABLE else None

# ============================================================================
# 1. MAIN DASHBOARD
# ============================================================================
if nav_option == "📊 Dashboard":
    st.title("🎯 HexStrike Operations Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Active Investigations",
            value="3",
            delta="+1 this week",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            label="Tor Circuit Status",
            value="🟢 Connected",
            delta="Latency: 245ms",
            delta_color="off"
        )
    
    with col3:
        st.metric(
            label="Reports Generated",
            value="12",
            delta="+2 pending",
            delta_color="off"
        )
    
    with col4:
        st.metric(
            label="Team Members",
            value="4",
            delta="All active",
            delta_color="off"
        )
    
    st.markdown("---")
    
    # Recent Activity
    st.subheader("📋 Recent Activity")
    
    activity_data = {
        "Timestamp": [
            datetime.now() - timedelta(hours=2),
            datetime.now() - timedelta(hours=4),
            datetime.now() - timedelta(hours=6),
            datetime.now() - timedelta(hours=8),
        ],
        "Event": [
            "Investigation Report Generated",
            "Tor Circuit Renewed",
            "New OSINT Data Collected",
            "Team Member Added",
        ],
        "Status": ["✅ Success", "✅ Success", "✅ Success", "✅ Success"],
    }
    
    df_activity = pd.DataFrame(activity_data)
    st.dataframe(df_activity, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Timeline visualization
    st.subheader("📅 Investigations Timeline")
    
    timeline_data = {
        "Investigation": ["Domain OSINT", "Social Media Analysis", "Network Footprint", "Report Compilation"],
        "Start": [0, 2, 4, 6],
        "Duration": [2, 2, 2, 2],
        "Status": ["Completed", "Completed", "In Progress", "Pending"],
    }
    
    df_timeline = pd.DataFrame(timeline_data)
    fig = px.bar(
        df_timeline,
        x="Start",
        y="Investigation",
        color="Status",
        color_discrete_map={
            "Completed": "#00ff00",
            "In Progress": "#ffaa00",
            "Pending": "#ff4444"
        },
        orientation="h",
        title="Current Investigation Timeline"
    )
    fig.update_layout(height=300, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# 2. INVESTIGATIONS
# ============================================================================
elif nav_option == "🔍 Investigations":
    st.title("🔍 Active Investigations")
    
    tab1, tab2, tab3 = st.tabs(["Active Cases", "Assign Task", "Investigation Log"])
    
    with tab1:
        st.subheader("Current Investigations")
        
        investigations = [
            {
                "ID": "INV-2026-001",
                "Target": "acme-corp.com",
                "Type": "OSINT",
                "Assigned": "Agent Smith",
                "Status": "🟢 Active",
                "Progress": 65,
            },
            {
                "ID": "INV-2026-002",
                "Target": "@company_twitter",
                "Type": "Social Media Analysis",
                "Assigned": "Agent Johnson",
                "Status": "🟢 Active",
                "Progress": 40,
            },
            {
                "ID": "INV-2026-003",
                "Target": "192.168.1.0/24",
                "Type": "Network Footprint",
                "Assigned": "Agent Williams",
                "Status": "🟡 Paused",
                "Progress": 30,
            },
        ]
        
        for inv in investigations:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                with col1:
                    st.write(f"**{inv['ID']}**: {inv['Target']}")
                with col2:
                    st.write(f"Type: {inv['Type']}")
                with col3:
                    st.write(f"Assigned: {inv['Assigned']}")
                with col4:
                    st.write(f"{inv['Status']}")
                st.progress(inv['Progress'] / 100)
                st.divider()
    
    with tab2:
        st.subheader("Assign New Task")
        col1, col2 = st.columns(2)
        
        with col1:
            investigation_id = st.text_input("Investigation ID", "INV-2026-")
            task_type = st.selectbox("Task Type", ["OSINT", "Social Media Analysis", "Network Scan", "Report"])
        
        with col2:
            assigned_to = st.selectbox("Assign To", ["Agent Smith", "Agent Johnson", "Agent Williams"])
            priority = st.select_slider("Priority", ["Low", "Medium", "High", "Critical"])
        
        task_description = st.text_area("Task Description")
        
        if st.button("✅ Assign Task"):
            st.success(f"Task assigned to {assigned_to} with {priority} priority")
    
    with tab3:
        st.subheader("Investigation Log")
        st.info("📝 Investigation logs and notes will appear here")

# ============================================================================
# 3. VAULT INTELLIGENCE
# ============================================================================
elif nav_option == "🧠 Vault Intelligence":
    st.title("🧠 Vault Intelligence Hub")
    
    if has_vault:
        st.success("✅ Vault connected and accessible")
        
        col1, col2 = st.columns(2)
        
        with col1:
            search_term = st.text_input("🔍 Search Vault", placeholder="Search investigations, notes, indicators...")
            
            if search_term:
                st.info(f"Searching vault for: '{search_term}'")
                st.write("📁 Results will appear here")
        
        with col2:
            st.subheader("📚 Categories")
            categories = ["Past Investigations", "Indicators Library", "Techniques Catalog", "Report Templates"]
            selected_category = st.selectbox("Browse by category", categories)
            st.write(f"Selected: {selected_category}")
        
        st.markdown("---")
        
        st.subheader("📋 Recent Vault Entries")
        vault_entries = {
            "Date": ["2026-02-22", "2026-02-21", "2026-02-20"],
            "Entry": ["OSINT Methodology Guide", "Domain Indicators Database", "Report Template v2"],
            "Type": ["Guide", "Database", "Template"],
        }
        df_vault = pd.DataFrame(vault_entries)
        st.dataframe(df_vault, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Vault not accessible at /vault")
        st.info("The Vault Intelligence Hub requires the vault-sync container to be running")

# ============================================================================
# 4. REPORTS & ANALYTICS
# ============================================================================
elif nav_option == "📈 Reports & Analytics":
    st.title("📈 Reports & Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Generate Report", "Report History", "Analytics"])
    
    with tab1:
        st.subheader("Generate New Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            report_title = st.text_input("Report Title")
            report_type = st.selectbox("Report Type", [
                "Executive Summary",
                "Technical Findings",
                "OSINT Report",
                "Pentest Report",
                "Risk Assessment"
            ])
        
        with col2:
            investigation_ref = st.selectbox("Reference Investigation", ["INV-2026-001", "INV-2026-002", "INV-2026-003"])
            report_format = st.radio("Format", ["PDF", "Markdown", "HTML"])
        
        findings = st.text_area("Key Findings", height=200)
        
        legal_framework = st.checkbox("✅ Verified under THIRTY3 Legal Framework")
        
        if st.button("📄 Generate Report"):
            if legal_framework:
                st.success("Report generated successfully!")
                st.balloons()
            else:
                st.error("⚠️ Report must be verified under legal framework")
    
    with tab2:
        st.subheader("Report History")
        
        reports = {
            "Date": ["2026-02-22", "2026-02-21", "2026-02-20", "2026-02-19"],
            "Title": ["Monthly Summary", "Domain Analysis", "Social Media Findings", "Network Assessment"],
            "Status": ["✅ Final", "✅ Final", "⏳ Draft", "✅ Final"],
            "Pages": [12, 8, 15, 10],
        }
        df_reports = pd.DataFrame(reports)
        st.dataframe(df_reports, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Reports by Type**")
            report_types = ["Executive Summary", "Technical", "OSINT", "Pentest", "Risk"]
            report_counts = [8, 5, 12, 3, 4]
            fig1 = px.pie(values=report_counts, names=report_types, title="Report Distribution")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.write("**Reports Over Time**")
            dates = pd.date_range(start="2026-02-01", periods=21, freq="D")
            report_daily = [1, 0, 2, 1, 3, 0, 2, 1, 1, 0, 2, 3, 1, 0, 2, 1, 1, 2, 0, 1, 1]
            fig2 = px.line(x=dates, y=report_daily, markers=True, title="Daily Report Generation")
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)

# ============================================================================
# 5. CONFIGURATION
# ============================================================================
elif nav_option == "⚙️ Configuration":
    st.title("⚙️ Configuration")
    
    tab1, tab2, tab3 = st.tabs(["System Status", "Tor Settings", "Team Management"])
    
    with tab1:
        st.subheader("System Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Containers Status**")
            containers = {
                "Container": ["th3-streamlit", "th3-hexstrike", "th3-kali", "th3-tor", "vault-sync"],
                "Status": ["🟢 Running", "🟢 Running", "🟢 Running", "🟢 Running", "🟢 Running"],
                "Port": ["8501", "8001", "5901", "9050", "internal"],
            }
            df_containers = pd.DataFrame(containers)
            st.dataframe(df_containers, use_container_width=True, hide_index=True)
        
        with col2:
            st.write("**Storage**")
            storage = {
                "Location": ["/vault", "/hexstrike/data", "/reports", "Total"],
                "Used": ["2.4 GB", "1.2 GB", "850 MB", "4.45 GB"],
            }
            df_storage = pd.DataFrame(storage)
            st.dataframe(df_storage, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Tor Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Tor Status", "🟢 Connected", "Circuit healthy")
            st.metric("Exit Node", "US - New York", "185.220.101.45")
        
        with col2:
            st.metric("Latency", "245ms", "+5ms")
            st.metric("Circuit Age", "23 minutes", "Rotate in 37 minutes")
        
        st.markdown("---")
        
        if st.button("🔄 Renew Tor Circuit"):
            st.info("Tor circuit renewal initiated...")
            st.success("✅ New circuit established")
    
    with tab3:
        st.subheader("Team Management")
        
        team_members = {
            "Agent": ["Smith", "Johnson", "Williams", "Brown"],
            "Role": ["Lead Analyst", "OSINT Specialist", "Network Expert", "Report Writer"],
            "Status": ["🟢 Active", "🟢 Active", "🟡 Away", "🟢 Active"],
            "Cases": [4, 3, 2, 3],
        }
        df_team = pd.DataFrame(team_members)
        st.dataframe(df_team, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        new_agent = st.text_input("Add Team Member")
        new_role = st.selectbox("Role", ["Lead Analyst", "OSINT Specialist", "Network Expert", "Report Writer"])
        
        if st.button("➕ Add Member"):
            st.success(f"{new_agent} added as {new_role}")

# ============================================================================
# 6. DOCUMENTATION
# ============================================================================
elif nav_option == "📚 Documentation":
    st.title("📚 Documentation & Help")
    
    tab1, tab2, tab3 = st.tabs(["Getting Started", "Guidelines", "Resources"])
    
    with tab1:
        st.subheader("Getting Started with HexStrike")
        
        st.markdown("""
        ### Welcome to HexStrike Operations Center
        
        This dashboard provides centralized control for:
        - **🔍 Investigation Management**: Track OSINT and pentest engagements
        - **🧠 Vault Intelligence**: Access past research and indicators
        - **📈 Report Generation**: Create comprehensive findings reports
        - **⚙️ System Configuration**: Manage containers and team
        
        ### Quick Start
        1. Navigate using the sidebar menu
        2. Create new investigations in the "Investigations" section
        3. Generate reports with legal compliance verification
        4. Search the vault for past findings
        
        ### Architecture
        - **th3-streamlit**: This dashboard (port 8501)
        - **th3-hexstrike**: OSINT/Pentest tools (port 8001)
        - **th3-kali**: Penetration testing toolkit
        - **th3-tor**: Anonymous routing (SOCKS5 on 9050)
        - **vault-sync**: Shared knowledge base (/vault)
        """)
    
    with tab2:
        st.subheader("THIRTY3 Guidelines")
        
        st.markdown("""
        ### Legal Framework Compliance
        
        All operations must comply with THIRTY3 legal standards:
        
        ✅ **Authorized Activities**
        - OSINT on public information
        - Authorized penetration testing
        - Intelligence gathering with client consent
        
        ❌ **Prohibited Activities**
        - Unauthorized system access
        - Data exfiltration
        - Disruption or DoS attacks
        
        ### Investigation Standards
        1. Verify authorization before starting
        2. Document all findings
        3. Maintain audit trail
        4. Generate compliant reports
        """)
    
    with tab3:
        st.subheader("Resources")
        
        st.markdown("""
        ### Documentation Files
        - `/vault` → Shared knowledge base
        - `_TEMPLATES/` → Report and investigation templates
        - `_BRAIN/` → Project architecture and planning
        
        ### Internal Tools
        - HexStrike: http://localhost:8001
        - Kali Tools: VNC on localhost:5901
        - Tor Status: SOCKS5 on localhost:9050
        
        ### External Resources
        - [OSINT Frameworks](https://osintframework.com/)
        - [MITRE ATT&CK](https://attack.mitre.org/)
        - [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
        """)

# ============================================================================
# Footer
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px;">
    HexStrike Operations Center v2.0 | Running under THIRTY3 Legal Framework
</div>
""", unsafe_allow_html=True)