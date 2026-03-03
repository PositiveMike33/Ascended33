"""
╔══════════════════════════════════════════════════════╗
║         HEXSTRIKE OPERATIONS CENTER v2.0             ║
║         Streamlit Dashboard — th3-streamlit          ║
╚══════════════════════════════════════════════════════╝
"""

import streamlit as st
import datetime
import random

# ─── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="HexStrike OpCenter",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ───────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&display=swap');
  :root {
    --hex-green:#00ff88; --hex-cyan:#00e5ff; --hex-red:#ff3355;
    --hex-yellow:#ffcc00; --hex-orange:#ff7700;
    --bg-deep:#050a0f; --bg-card:#0a1520; --bg-border:#0d2030;
    --text-dim:#3a6b8a; --text-mid:#6aa9cc; --text-main:#b8d8eb;
  }
  html,body,[data-testid="stAppViewContainer"]{background:var(--bg-deep)!important;color:var(--text-main)!important;font-family:'Rajdhani',sans-serif!important;}
  [data-testid="stSidebar"]{background:#020810!important;border-right:1px solid var(--bg-border)!important;}
  h1,h2,h3{font-family:'Share Tech Mono',monospace!important;}
  h1{color:var(--hex-green)!important;letter-spacing:2px;}
  h2{color:var(--hex-cyan)!important;letter-spacing:1px;}
  [data-testid="stMetric"]{background:var(--bg-card)!important;border:1px solid var(--bg-border)!important;border-left:3px solid var(--hex-green)!important;border-radius:4px!important;padding:12px!important;}
  [data-testid="stMetricLabel"]{color:var(--text-dim)!important;font-family:'Share Tech Mono',monospace!important;font-size:11px!important;}
  [data-testid="stMetricValue"]{color:var(--hex-green)!important;font-family:'Share Tech Mono',monospace!important;}
  .stButton>button{background:transparent!important;border:1px solid var(--hex-green)!important;color:var(--hex-green)!important;font-family:'Share Tech Mono',monospace!important;letter-spacing:1px!important;border-radius:2px!important;transition:all 0.2s!important;}
  .stButton>button:hover{background:var(--hex-green)!important;color:var(--bg-deep)!important;box-shadow:0 0 12px var(--hex-green)!important;}
  .stSelectbox>div>div,.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:var(--bg-card)!important;border:1px solid var(--bg-border)!important;color:var(--text-main)!important;font-family:'Share Tech Mono',monospace!important;}
  .stTabs [data-baseweb="tab-list"]{background:var(--bg-card)!important;border-bottom:1px solid var(--bg-border)!important;gap:0!important;}
  .stTabs [data-baseweb="tab"]{color:var(--text-dim)!important;font-family:'Share Tech Mono',monospace!important;font-size:12px!important;letter-spacing:1px!important;padding:8px 20px!important;border:none!important;border-right:1px solid var(--bg-border)!important;}
  .stTabs [aria-selected="true"]{color:var(--hex-green)!important;background:var(--bg-deep)!important;border-bottom:2px solid var(--hex-green)!important;}
  hr{border-color:var(--bg-border)!important;}
  .streamlit-expanderHeader{background:var(--bg-card)!important;color:var(--hex-cyan)!important;font-family:'Share Tech Mono',monospace!important;border:1px solid var(--bg-border)!important;}
  .streamlit-expanderContent{background:var(--bg-card)!important;border:1px solid var(--bg-border)!important;border-top:none!important;}
  .badge{display:inline-block;padding:2px 8px;border-radius:2px;font-family:'Share Tech Mono',monospace;font-size:11px;font-weight:600;letter-spacing:1px;}
  .badge-green{background:rgba(0,255,136,.15);color:var(--hex-green);border:1px solid var(--hex-green);}
  .badge-red{background:rgba(255,51,85,.15);color:var(--hex-red);border:1px solid var(--hex-red);}
  .badge-yellow{background:rgba(255,204,0,.15);color:var(--hex-yellow);border:1px solid var(--hex-yellow);}
  .badge-cyan{background:rgba(0,229,255,.15);color:var(--hex-cyan);border:1px solid var(--hex-cyan);}
  .badge-orange{background:rgba(255,119,0,.15);color:var(--hex-orange);border:1px solid var(--hex-orange);}
  .op-card{background:var(--bg-card);border:1px solid var(--bg-border);border-radius:4px;padding:16px;margin-bottom:12px;position:relative;}
  .op-card::before{content:'';position:absolute;top:0;left:0;width:3px;height:100%;background:var(--hex-green);border-radius:4px 0 0 4px;}
  .op-card.red::before{background:var(--hex-red);}
  .op-card.cyan::before{background:var(--hex-cyan);}
  .op-card.yellow::before{background:var(--hex-yellow);}
  .terminal{background:#000a0f;border:1px solid var(--bg-border);border-radius:4px;padding:16px;font-family:'Share Tech Mono',monospace;font-size:12px;color:var(--hex-green);line-height:1.6;white-space:pre-wrap;word-break:break-all;}
  .stProgress>div>div{background:var(--hex-green)!important;}
  .stAlert{background:var(--bg-card)!important;border:1px solid var(--bg-border)!important;}
  .stCheckbox label{color:var(--text-main)!important;font-family:'Rajdhani'!important;}
  ::-webkit-scrollbar{width:6px;background:var(--bg-deep);}
  ::-webkit-scrollbar-thumb{background:var(--bg-border);border-radius:3px;}
  ::-webkit-scrollbar-thumb:hover{background:var(--hex-green);}
  #MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)


# ─── STATE INIT ───────────────────────────────────────
def _init():
    defaults = {
        "page": "OPERATIONS",
        "investigations": [
            {"id":"INV-001","target":"target-domain.com","type":"OSINT","status":"ACTIVE","priority":"HIGH","created":"2025-02-10","progress":65},
            {"id":"INV-002","target":"192.168.1.0/24","type":"NETWORK","status":"COMPLETE","priority":"MEDIUM","created":"2025-01-28","progress":100},
            {"id":"INV-003","target":"john.doe@corp.com","type":"EMAIL","status":"ACTIVE","priority":"HIGH","created":"2025-02-14","progress":30},
            {"id":"INV-004","target":"@th3_target_handle","type":"SOCIAL","status":"PENDING","priority":"LOW","created":"2025-02-18","progress":0},
            {"id":"INV-005","target":"0x1A2B3C4D...","type":"CRYPTO","status":"ACTIVE","priority":"MEDIUM","created":"2025-02-20","progress":45},
        ],
        "tor_status":"CONNECTED",
        "active_circuit":"FR → DE → NL",
        "tor_exit_ip":"185.220.101.47",
        "reports":[],
        "vault_notes":[
            {"title":"OSINT Email Recon Playbook","tags":["OSINT","EMAIL"],"modified":"2025-02-21"},
            {"title":"Domain Reconnaissance Guide","tags":["OSINT","DOMAIN"],"modified":"2025-02-19"},
            {"title":"Tor OPSEC Checklist","tags":["OPSEC","TOR"],"modified":"2025-02-18"},
            {"title":"Legal Authorization Template","tags":["LEGAL"],"modified":"2025-02-15"},
            {"title":"Crypto Tracing Methodology","tags":["CRYPTO","CHAIN"],"modified":"2025-02-10"},
        ],
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k]=v
_init()


# ─── HELPERS ──────────────────────────────────────────
def badge(label,kind="green"):
    return f'<span class="badge badge-{kind}">{label}</span>'

def status_badge(s):
    m={"ACTIVE":"green","COMPLETE":"cyan","PENDING":"yellow","PAUSED":"orange","FAILED":"red"}
    return badge(s,m.get(s,"cyan"))

def priority_badge(p):
    m={"HIGH":"red","MEDIUM":"yellow","LOW":"cyan","CRITICAL":"orange"}
    return badge(p,m.get(p,"cyan"))

def terminal_block(c):
    return f'<div class="terminal">{c}</div>'

def now_ts():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ─── SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 0 10px 0;'>
      <div style='font-family:"Share Tech Mono",monospace;font-size:28px;color:#00ff88;letter-spacing:3px;'>⬡ HEXSTRIKE</div>
      <div style='font-family:"Share Tech Mono",monospace;font-size:10px;color:#3a6b8a;letter-spacing:4px;margin-top:4px;'>OPERATIONS CENTER v2.0</div>
    </div>
    <hr style='border-color:#0d2030;margin:8px 0 16px 0;'/>
    """, unsafe_allow_html=True)

    tor_color="#00ff88" if st.session_state.tor_status=="CONNECTED" else "#ff3355"
    st.markdown(f"""
    <div class='op-card' style='margin-bottom:16px;padding:10px 14px;'>
      <div style='font-family:"Share Tech Mono",monospace;font-size:10px;color:#3a6b8a;letter-spacing:2px;'>TOR STATUS</div>
      <div style='display:flex;align-items:center;gap:8px;margin-top:4px;'>
        <div style='width:8px;height:8px;border-radius:50%;background:{tor_color};box-shadow:0 0 8px {tor_color};'></div>
        <span style='font-family:"Share Tech Mono",monospace;font-size:13px;color:{tor_color};'>{st.session_state.tor_status}</span>
      </div>
      <div style='font-family:"Share Tech Mono",monospace;font-size:10px;color:#6aa9cc;margin-top:4px;'>CIRCUIT: {st.session_state.active_circuit}</div>
      <div style='font-family:"Share Tech Mono",monospace;font-size:10px;color:#3a6b8a;margin-top:2px;'>EXIT: {st.session_state.tor_exit_ip}</div>
    </div>
    """, unsafe_allow_html=True)

    pages=[("OPERATIONS","⬡"),("INVESTIGATIONS","◈"),("TOR OPSEC","⊛"),("REPORT GEN","▣"),("VAULT SEARCH","⊡"),("TELEGRAM","⊹"),("CONFIGURATION","⊕")]
    for pname,icon in pages:
        if st.button(f"{icon}  {pname}",key=f"nav_{pname}",use_container_width=True):
            st.session_state.page=pname; st.rerun()

    st.markdown("<hr style='border-color:#0d2030;margin:16px 0;'/>", unsafe_allow_html=True)
    active_c=sum(1 for i in st.session_state.investigations if i["status"]=="ACTIVE")
    pending_c=sum(1 for i in st.session_state.investigations if i["status"]=="PENDING")
    st.markdown(f"""
    <div style='font-family:"Share Tech Mono",monospace;font-size:10px;color:#3a6b8a;letter-spacing:2px;padding:0 4px;'>QUICK STATS</div>
    <div style='padding:8px 4px;font-family:"Share Tech Mono",monospace;font-size:11px;'>
      <div style='display:flex;justify-content:space-between;margin:4px 0;'><span style='color:#6aa9cc;'>Active</span><span style='color:#00ff88;'>{active_c}</span></div>
      <div style='display:flex;justify-content:space-between;margin:4px 0;'><span style='color:#6aa9cc;'>Pending</span><span style='color:#ffcc00;'>{pending_c}</span></div>
      <div style='display:flex;justify-content:space-between;margin:4px 0;'><span style='color:#6aa9cc;'>Vault notes</span><span style='color:#00e5ff;'>{len(st.session_state.vault_notes)}</span></div>
    </div>
    """, unsafe_allow_html=True)


# ─── PAGE: OPERATIONS ─────────────────────────────────
def page_operations():
    st.markdown("## ⬡ OPERATIONS CENTER")
    st.markdown(f"<div style='font-family:\"Share Tech Mono\",monospace;font-size:11px;color:#3a6b8a;'>SYSTEM TIME: {now_ts()} UTC &nbsp;|&nbsp; OPERATOR: TH3_THIRTY3 &nbsp;|&nbsp; CLEARANCE: ALPHA</div>",unsafe_allow_html=True)
    st.markdown("<hr/>",unsafe_allow_html=True)
    c1,c2,c3,c4,c5=st.columns(5, gap="small")
    total=len(st.session_state.investigations)
    active=sum(1 for i in st.session_state.investigations if i["status"]=="ACTIVE")
    done=sum(1 for i in st.session_state.investigations if i["status"]=="COMPLETE")
    high=sum(1 for i in st.session_state.investigations if i["priority"]=="HIGH")
    c1.metric("TOTAL CASES",total); c2.metric("ACTIVE",active); c3.metric("COMPLETED",done); c4.metric("HIGH PRIORITY",high); c5.metric("TOR CIRCUITS","1")
    st.markdown("<br/>",unsafe_allow_html=True)
    col_l,col_r=st.columns([3,2], gap="small")
    with col_l:
        st.markdown("### ◈ ACTIVE INVESTIGATIONS")
        for inv in [i for i in st.session_state.investigations if i["status"] in ("ACTIVE","PENDING")]:
            with st.expander(f"{inv['id']} — {inv['target']}",expanded=False):
                c1,c2,c3=st.columns(3, gap="small")
                c1.markdown(f"**TYPE:** {inv['type']}")
                c2.markdown(status_badge(inv["status"])+" "+priority_badge(inv["priority"]),unsafe_allow_html=True)
                c3.markdown(f"**CREATED:** {inv['created']}")
                st.progress(inv["progress"]/100)
                st.markdown(f"<div style='font-family:\"Share Tech Mono\",monospace;font-size:11px;color:#6aa9cc;'>PROGRESS: {inv['progress']}%</div>",unsafe_allow_html=True)
    with col_r:
        st.markdown("### ⊛ TOR CIRCUIT")
        nodes=[("YOU","Montreal, CA","#00ff88"),("ENTRY GUARD","Paris, FR","#00e5ff"),("MIDDLE RELAY","Berlin, DE","#00e5ff"),("EXIT NODE","Amsterdam, NL","#ff7700"),("TARGET","Unknown","#ff3355")]
        for i,(role,loc,color) in enumerate(nodes):
            st.markdown(f"""<div style='display:flex;align-items:center;gap:12px;margin:4px 0;'>
              <div style='width:10px;height:10px;border-radius:50%;background:{color};box-shadow:0 0 6px {color};flex-shrink:0;'></div>
              <div style='font-family:"Share Tech Mono",monospace;font-size:11px;'><span style='color:{color};'>{role}</span><span style='color:#3a6b8a;margin-left:8px;'>{loc}</span></div>
            </div>{"<div style='margin-left:4px;color:#0d2030;font-size:11px;font-family:Share Tech Mono,monospace;'>│</div>" if i<len(nodes)-1 else ""}""",unsafe_allow_html=True)
        st.markdown("<br/>",unsafe_allow_html=True)
        st.markdown("### ▣ ACTIVITY LOG")
        logs=[("02:14:55","INV-003","Email header extracted","green"),("01:47:22","INV-001","Subdomain enum: +47 hosts","green"),("01:12:08","TOR","Circuit renewed","cyan"),("00:33:14","INV-005","Wallet cluster found","yellow"),("00:01:59","SYSTEM","Vault sync completed","cyan")]
        log_html="".join(f"<div style='margin:3px 0;'><span style='color:#3a6b8a;'>[{ts}]</span> <span style='color:var(--hex-{c});'>{src}</span> <span style='color:#6aa9cc;'>→</span> <span style='color:#b8d8eb;'>{msg}</span></div>" for ts,src,msg,c in logs)
        st.markdown(f'<div class="terminal">{log_html}</div>',unsafe_allow_html=True)


# ─── PAGE: INVESTIGATIONS ─────────────────────────────
def page_investigations():
    st.markdown("## ◈ INVESTIGATION TRACKER")
    st.markdown("<hr/>",unsafe_allow_html=True)
    tab1,tab2=st.tabs(["  ALL CASES  ","  + NEW CASE  "])
    with tab1:
        fc1,fc2,fc3=st.columns(3, gap="small")
        fs=fc1.selectbox("STATUS",["ALL","ACTIVE","PENDING","COMPLETE","PAUSED"])
        ft=fc2.selectbox("TYPE",["ALL","OSINT","NETWORK","EMAIL","SOCIAL","CRYPTO"])
        fp=fc3.selectbox("PRIORITY",["ALL","HIGH","MEDIUM","LOW","CRITICAL"])
        filtered=st.session_state.investigations
        if fs!="ALL": filtered=[i for i in filtered if i["status"]==fs]
        if ft!="ALL": filtered=[i for i in filtered if i["type"]==ft]
        if fp!="ALL": filtered=[i for i in filtered if i["priority"]==fp]
        st.markdown(f"<div style='font-family:\"Share Tech Mono\",monospace;font-size:11px;color:#3a6b8a;margin:8px 0;'>SHOWING {len(filtered)}/{len(st.session_state.investigations)} CASES</div>",unsafe_allow_html=True)
        for inv in filtered:
            with st.expander(f"  {inv['id']}  ▸  {inv['target']}  ▸  {inv['type']}",expanded=False):
                r1,r2,r3,r4=st.columns(4, gap="small")
                r1.markdown(f"**ID:** `{inv['id']}`")
                r2.markdown(status_badge(inv["status"]),unsafe_allow_html=True)
                r3.markdown(priority_badge(inv["priority"]),unsafe_allow_html=True)
                r4.markdown(f"**CREATED:** {inv['created']}")
                st.progress(inv["progress"]/100)
                st.markdown(f"<div style='font-family:\"Share Tech Mono\",monospace;font-size:11px;color:#6aa9cc;'>PROGRESS: {inv['progress']}%</div>",unsafe_allow_html=True)
                b1,b2,b3=st.columns(3, gap="small")
                if b1.button("▶ RESUME",key=f"res_{inv['id']}"): inv["status"]="ACTIVE"; st.rerun()
                if b2.button("⏸ PAUSE",key=f"pau_{inv['id']}"): inv["status"]="PAUSED"; st.rerun()
                if b3.button("✓ COMPLETE",key=f"cmp_{inv['id']}"): inv["status"]="COMPLETE"; inv["progress"]=100; st.rerun()
    with tab2:
        st.markdown("### NEW INVESTIGATION")
        nc1,nc2=st.columns(2, gap="small")
        target=nc1.text_input("TARGET",placeholder="domain.com / IP / email / @handle")
        inv_type=nc2.selectbox("TYPE",["OSINT","NETWORK","EMAIL","SOCIAL","CRYPTO","WEB"])
        nc3,nc4=st.columns(2, gap="small")
        priority=nc3.selectbox("PRIORITY",["HIGH","MEDIUM","LOW","CRITICAL"])
        auth=nc4.text_input("AUTHORIZATION REF",placeholder="AUTH-2025-XXX")
        notes=st.text_area("INITIAL NOTES / SCOPE",height=120,placeholder="Scope, objectives, legal authorization details...")
        legal_ok=st.checkbox("✓ Legal authorization has been obtained for this investigation")
        if st.button("◈ CREATE INVESTIGATION",use_container_width=True):
            if not target: st.error("TARGET required.")
            elif not legal_ok: st.error("Legal authorization confirmation required.")
            else:
                new_id=f"INV-{len(st.session_state.investigations)+1:03d}"
                st.session_state.investigations.append({"id":new_id,"target":target,"type":inv_type,"status":"PENDING","priority":priority,"created":datetime.date.today().isoformat(),"progress":0})
                st.success(f"✓ {new_id} created — {target}"); st.rerun()


# ─── PAGE: TOR OPSEC ──────────────────────────────────
def page_tor():
    st.markdown("## ⊛ TOR OPSEC PANEL")
    st.markdown("<hr/>",unsafe_allow_html=True)
    col1,col2=st.columns([2,3], gap="small")
    with col1:
        st.markdown("### CONNECTION STATUS")
        color="#00ff88" if st.session_state.tor_status=="CONNECTED" else "#ff3355"
        st.markdown(f"""<div class='op-card' style='text-align:center;padding:24px;'>
          <div style='font-size:40px;margin-bottom:8px;'>⊛</div>
          <div style='font-family:"Share Tech Mono",monospace;font-size:20px;color:{color};text-shadow:0 0 12px {color};'>{st.session_state.tor_status}</div>
          <div style='font-family:"Share Tech Mono",monospace;font-size:11px;color:#6aa9cc;margin-top:8px;'>CIRCUIT: {st.session_state.active_circuit}</div>
          <div style='font-family:"Share Tech Mono",monospace;font-size:10px;color:#3a6b8a;margin-top:4px;'>EXIT IP: {st.session_state.tor_exit_ip}</div>
          <div style='font-family:"Share Tech Mono",monospace;font-size:10px;color:#3a6b8a;margin-top:4px;'>SOCKS PORT: 9050</div>
        </div>""",unsafe_allow_html=True)
        if st.button("⟳ RENEW CIRCUIT",use_container_width=True):
            circuits=["FR → DE → NL","SE → CH → RO","NO → AT → CZ","FI → ES → PL"]
            exits=["185.220.101.47","91.108.56.139","176.10.99.200","109.70.100.28"]
            st.session_state.active_circuit=random.choice(circuits)
            st.session_state.tor_exit_ip=random.choice(exits)
            st.success("✓ Circuit renewed"); st.rerun()
        st.markdown("<br/>",unsafe_allow_html=True)
        st.markdown("### OPSEC THREAT LEVEL")
        for threat,level,color in [("IP LEAK","LOW","#00ff88"),("DNS LEAK","NONE","#00ff88"),("JS FINGERPRINT","MEDIUM","#ffcc00"),("TIMING ATTACK","LOW","#00ff88"),("EXIT NODE TRUST","MEDIUM","#ffcc00")]:
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #0d2030;'><span style='font-family:\"Share Tech Mono\",monospace;font-size:11px;color:#6aa9cc;'>{threat}</span><span style='font-family:\"Share Tech Mono\",monospace;font-size:11px;color:{color};'>{level}</span></div>",unsafe_allow_html=True)
    with col2:
        st.markdown("### OPSEC CHECKLIST")
        for section,items in [
            ("PRE-OPERATION",["Legal authorization obtained","VPN active before Tor","Real identity email/accounts not used","Browser history cleared","JavaScript disabled on target"]),
            ("DURING OPERATION",["No login to personal accounts","No file downloads without sandboxing","Circuit renewed every 10 minutes","No screenshots with identifying info","Timestamped notes for all findings"]),
            ("POST-OPERATION",["Circuit renewed before closing","All findings saved to Vault","Report generated and archived","Evidence chain of custody documented","Legal review completed"]),
        ]:
            st.markdown(f"**{section}**")
            for item in items:
                st.checkbox(item,key=f"opsec_{item}")
        st.markdown("<br/>",unsafe_allow_html=True)
        st.markdown("### PROXYCHAINS CONFIG")
        st.markdown(terminal_block("# /etc/proxychains4.conf\n[ProxyList]\nsocks5  127.0.0.1 9050\n\n# Usage:\nproxychains4 nmap -sT -p 80,443 target.com\nproxychains4 curl -s http://check.torproject.org\nproxychains4 python3 recon_script.py"),unsafe_allow_html=True)


# ─── PAGE: REPORT GENERATOR ───────────────────────────
def page_report():
    st.markdown("## ▣ REPORT GENERATOR")
    st.markdown("<hr/>",unsafe_allow_html=True)
    col1,col2=st.columns([2,3], gap="small")
    with col1:
        st.markdown("### REPORT PARAMETERS")
        rpt_inv=st.selectbox("INVESTIGATION",[i["id"]+" — "+i["target"] for i in st.session_state.investigations])
        rpt_type=st.selectbox("REPORT TYPE",["Executive Summary","Technical Report","OSINT Report","Pentest Report","Incident Report"])
        rpt_class=st.selectbox("CLASSIFICATION",["CONFIDENTIAL","RESTRICTED","INTERNAL","PUBLIC"])
        rpt_author=st.text_input("AUTHOR",value="TH3_THIRTY3")
        rpt_client=st.text_input("CLIENT/ORG",placeholder="Client organization name")
        if st.button("◈ GENERATE REPORT",use_container_width=True):
            inv_id=rpt_inv.split(" — ")[0]
            inv=next((i for i in st.session_state.investigations if i["id"]==inv_id),None)
            report={"id":f"RPT-{len(st.session_state.reports)+1:03d}","inv_id":inv_id,"target":inv["target"] if inv else "UNKNOWN","type":rpt_type,"class":rpt_class,"author":rpt_author,"client":rpt_client,"generated":now_ts()}
            st.session_state.reports.append(report)
            st.success(f"✓ Report {report['id']} generated"); st.rerun()
    with col2:
        st.markdown("### REPORT PREVIEW")
        if st.session_state.reports:
            r=st.session_state.reports[-1]
            st.markdown(terminal_block(f"╔══════════════════════════════════════════╗\n║  HEXSTRIKE INVESTIGATION REPORT         ║\n╚══════════════════════════════════════════╝\n\nREPORT ID     : {r['id']}\nINVESTIGATION : {r['inv_id']}\nTARGET        : {r['target']}\nTYPE          : {r['type'].upper()}\nCLASSIFICATION: {r['class']}\nAUTHOR        : {r['author']}\nCLIENT        : {r['client'] or 'INTERNAL'}\nGENERATED     : {r['generated']}\n\n─────────────────────────────────────────\n[1] EXECUTIVE SUMMARY\n─────────────────────────────────────────\nInvestigation {r['inv_id']} conducted against\ntarget {r['target']}. All activities performed\nunder legal authorization.\n\n[2] METHODOLOGY\n─────────────────────────────────────────\nPassive reconnaissance via Tor anonymization.\nTools: HexStrike, OSINT framework, scripts.\n\n[3] FINDINGS — [PENDING]\n[4] RISK ASSESSMENT — [PENDING]\n[5] RECOMMENDATIONS — [PENDING]\n\n═══════════════════════════════════════════\nEND OF REPORT — {r['id']} — {r['class']}\n═══════════════════════════════════════════"),unsafe_allow_html=True)
            st.markdown(f"<br/><div style='font-family:\"Share Tech Mono\",monospace;font-size:11px;color:#3a6b8a;'>ARCHIVED: {len(st.session_state.reports)} report(s)</div>",unsafe_allow_html=True)
        else:
            st.markdown(terminal_block("No reports generated yet.\nConfigure parameters on the left\nand click GENERATE REPORT."),unsafe_allow_html=True)


# ─── PAGE: VAULT SEARCH ───────────────────────────────
def page_vault():
    st.markdown("## ⊡ VAULT KNOWLEDGE BASE")
    st.markdown("<hr/>",unsafe_allow_html=True)
    col1,col2=st.columns([3,2], gap="small")
    with col1:
        search_q=st.text_input("⊡ SEARCH VAULT",placeholder="OSINT / recon / opsec / playbook ...")
        tag_filter=st.multiselect("FILTER BY TAG",["OSINT","EMAIL","DOMAIN","OPSEC","TOR","LEGAL","CRYPTO","CHAIN","NETWORK","SOCIAL"])
        filtered_notes=st.session_state.vault_notes
        if search_q: filtered_notes=[n for n in filtered_notes if search_q.lower() in n["title"].lower()]
        if tag_filter: filtered_notes=[n for n in filtered_notes if any(t in n["tags"] for t in tag_filter)]
        st.markdown(f"<div style='font-family:\"Share Tech Mono\",monospace;font-size:11px;color:#3a6b8a;margin:8px 0;'>{len(filtered_notes)} NOTES FOUND</div>",unsafe_allow_html=True)
        for note in filtered_notes:
            tags_html=" ".join([badge(t,"cyan") for t in note["tags"]])
            st.markdown(f"<div class='op-card cyan'><div style='font-family:\"Share Tech Mono\",monospace;font-size:14px;color:#b8d8eb;'>{note['title']}</div><div style='margin-top:8px;'>{tags_html}</div><div style='font-family:\"Share Tech Mono\",monospace;font-size:10px;color:#3a6b8a;margin-top:8px;'>MODIFIED: {note['modified']} | PATH: _BRAIN/</div></div>",unsafe_allow_html=True)
        st.markdown("<br/>",unsafe_allow_html=True)
        st.markdown("### + ADD NOTE")
        nn1,nn2=st.columns(2, gap="small")
        new_title=nn1.text_input("TITLE",placeholder="Note title")
        new_tags=nn2.text_input("TAGS",placeholder="OSINT,DOMAIN")
        if st.button("+ ADD TO VAULT"):
            if new_title:
                tags=[t.strip().upper() for t in new_tags.split(",") if t.strip()]
                st.session_state.vault_notes.append({"title":new_title,"tags":tags,"modified":datetime.date.today().isoformat()})
                st.success(f"✓ '{new_title}' added"); st.rerun()
    with col2:
        st.markdown("### PLAYBOOK LIBRARY")
        for pb_id,pb_name,pb_tag in [("OSINT_EMAIL_RECON","Email Reconnaissance","EMAIL"),("DOMAIN_RECON","Domain Reconnaissance","DOMAIN"),("IP_INVESTIGATION","IP Tracking & Geoloc","NETWORK"),("CRYPTO_TRACING","Cryptocurrency Tracking","CRYPTO"),("SOCIAL_MEDIA_ANALYSIS","Social Media OSINT","SOCIAL"),("TOR_OPSEC_PROTOCOL","Tor OPSEC Protocol","TOR"),("LEGAL_AUTHORIZATION","Legal Authorization","LEGAL")]:
            st.markdown(f"<div class='op-card' style='padding:10px 14px;'><div style='display:flex;justify-content:space-between;align-items:center;'><div><div style='font-family:\"Share Tech Mono\",monospace;font-size:12px;color:#b8d8eb;'>{pb_name}</div><div style='font-family:\"Share Tech Mono\",monospace;font-size:9px;color:#3a6b8a;margin-top:2px;'>{pb_id}.md</div></div>{badge(pb_tag,'cyan')}</div></div>",unsafe_allow_html=True)
        st.markdown("<br/>",unsafe_allow_html=True)
        st.markdown(terminal_block(f"VAULT SYNC STATUS\n─────────────────\nLast sync  : {datetime.date.today().isoformat()}\nTotal notes: {len(st.session_state.vault_notes)}\nPlaybooks  : 7\nTemplates  : 4\n\nSTRUCTURE\n─────────\n_BRAIN/HEXSTRIKE_PLAYBOOKS/\n_BRAIN/INDICATORS_LIBRARY/\n_BRAIN/LEGAL_FRAMEWORK/\n_BRAIN/CASE_STUDIES/\n_TEMPLATES/"),unsafe_allow_html=True)


# ─── PAGE: CONFIGURATION ──────────────────────────────
def page_config():
    st.markdown("## ⊕ CONFIGURATION")
    st.markdown("<hr/>",unsafe_allow_html=True)
    tab1,tab2,tab3=st.tabs(["  SERVICES  ","  NETWORK  ","  OPERATOR  "])
    with tab1:
        st.markdown("### SERVICE ENDPOINTS")
        for svc,port,desc,status in [("th3-hexstrike",":8001","HexStrike Core","RUNNING"),("th3-hackergpt",":8000","HackerGPT AI","RUNNING"),("th3-kali",":22","Kali Toolkit SSH","RUNNING"),("th3-tor",":9050","Tor SOCKS Proxy","RUNNING"),("th3-security",":3000","Security Dashboard","RUNNING"),("th3-streamlit",":8501","This Dashboard","RUNNING")]:
            color="#00ff88" if status=="RUNNING" else "#ff3355"
            st.markdown(f"<div class='op-card' style='padding:10px 14px;'><div style='display:flex;justify-content:space-between;align-items:center;'><div><div style='font-family:\"Share Tech Mono\",monospace;font-size:13px;color:#b8d8eb;'>{svc}</div><div style='font-family:\"Share Tech Mono\",monospace;font-size:10px;color:#3a6b8a;'>{desc} — PORT {port}</div></div><div style='display:flex;align-items:center;gap:6px;'><div style='width:7px;height:7px;border-radius:50%;background:{color};box-shadow:0 0 6px {color};'></div><span style='font-family:\"Share Tech Mono\",monospace;font-size:11px;color:{color};'>{status}</span></div></div></div>",unsafe_allow_html=True)
    with tab2:
        st.markdown("### NETWORK CONFIGURATION")
        cc1,cc2=st.columns(2, gap="small")
        cc1.text_input("TOR PROXY HOST",value="127.0.0.1"); cc2.text_input("TOR SOCKS PORT",value="9050")
        cc1.text_input("HEXSTRIKE HOST",value="th3-hexstrike"); cc2.text_input("HEXSTRIKE PORT",value="8001")
        cc1.text_input("HACKERGPT HOST",value="th3-hackergpt"); cc2.text_input("HACKERGPT PORT",value="8000")
        st.text_input("VAULT PATH",value="/vault")
        if st.button("SAVE NETWORK CONFIG"): st.success("✓ Configuration saved")
    with tab3:
        st.markdown("### OPERATOR PROFILE")
        p1,p2=st.columns(2, gap="small")
        p1.text_input("OPERATOR ID",value="TH3_THIRTY3"); p2.text_input("CLEARANCE LEVEL",value="ALPHA")
        p1.text_input("ORGANIZATION",value="HEXSTRIKE OPS"); p2.selectbox("TIMEZONE",["UTC","America/Montreal","Europe/Paris"])
        st.markdown("### PREFERENCES")
        st.checkbox("Auto-renew Tor circuit every 10 min",value=True)
        st.checkbox("Save investigations to Vault on close",value=True)
        st.checkbox("Require legal auth confirmation",value=True)
        st.checkbox("Enable activity logging",value=True)
        st.slider("LOG RETENTION (days)",7,90,30)
        if st.button("SAVE OPERATOR PROFILE"): st.success("✓ Operator profile saved")


# ─── ROUTER ───────────────────────────────────────────

# ─── PAGE: TELEGRAM MONITORING ────────────────────────────────────────────────
def page_telegram():
    st.markdown("## ⊹ TELEGRAM INTEL MONITOR")
    st.markdown("<hr/>", unsafe_allow_html=True)

    channels = [
        {"name":"@hexstrike_ops_bot",   "type":"OWN BOT",   "status":"ACTIVE", "members":1,    "last_msg":"02:14","unread":0,  "tags":["OPS"]},
        {"name":"@darkweb_intel",       "type":"MONITORED", "status":"ACTIVE", "members":4820, "last_msg":"01:47","unread":14, "tags":["OSINT","THREAT"]},
        {"name":"@cybersec_fr",         "type":"MONITORED", "status":"ACTIVE", "members":9310, "last_msg":"00:55","unread":7,  "tags":["FR","NEWS"]},
        {"name":"@leaks_monitor",       "type":"MONITORED", "status":"ACTIVE", "members":2140, "last_msg":"00:33","unread":3,  "tags":["LEAKS"]},
        {"name":"@th3_thirty3_alerts",  "type":"OWN BOT",   "status":"ACTIVE", "members":1,    "last_msg":"23:58","unread":0,  "tags":["ALERTS"]},
        {"name":"@osint_stream",        "type":"MONITORED", "status":"PAUSED", "members":6700, "last_msg":"18:22","unread":0,  "tags":["OSINT"]},
    ]
    alerts = [
        {"ts":"02:14","chan":"@darkweb_intel","kw":"hexstrike",     "msg":"New OSINT tool spotted: hexstrike framework listed on channel...","sev":"HIGH"},
        {"ts":"01:47","chan":"@leaks_monitor","kw":"data breach",   "msg":"Alleged database leak from Quebec-based financial firm...","sev":"MEDIUM"},
        {"ts":"01:12","chan":"@cybersec_fr",  "kw":"ransomware",    "msg":"LockBit 3.0 campaign targeting French-Canadian SMEs detected...","sev":"HIGH"},
        {"ts":"00:33","chan":"@darkweb_intel","kw":"credential",    "msg":"Fresh combo list: ~50k entries, CA region...","sev":"MEDIUM"},
        {"ts":"23:55","chan":"@osint_stream", "kw":"recon",         "msg":"New passive recon tool released: passive DNS enumeration...","sev":"LOW"},
    ]

    tab1, tab2, tab3 = st.tabs(["  CHANNELS  ", "  KEYWORD ALERTS  ", "  BOT MANAGER  "])

    with tab1:
        st.markdown("### MONITORED CHANNELS")
        for section_label, type_filter in [("OWN BOTS", "OWN BOT"), ("MONITORED CHANNELS", "MONITORED")]:
            section_list = [c for c in channels if c["type"] == type_filter]
            st.markdown(f"<div style='font-family:\"Share Tech Mono\",monospace;font-size:10px;color:#3a6b8a;letter-spacing:2px;margin:12px 0 8px 0;'>{section_label} ({len(section_list)})</div>", unsafe_allow_html=True)
            for c in section_list:
                tags_html = " ".join([badge(t,"cyan") for t in c["tags"]])
                unread_str = f" ● {c['unread']}" if c["unread"] > 0 else ""
                unread_html = f'<span style="color:#ffcc00;font-family:monospace;font-size:11px;">{unread_str}</span>'
                dot_color = "#00ff88" if c["status"] == "ACTIVE" else "#ff7700"
                st.markdown(f"""
                <div class='op-card' style='padding:10px 14px;'>
                  <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div>
                      <div style='display:flex;align-items:center;gap:8px;'>
                        <div style='width:7px;height:7px;border-radius:50%;background:{dot_color};box-shadow:0 0 5px {dot_color};'></div>
                        <span style='font-family:"Share Tech Mono",monospace;font-size:13px;color:#b8d8eb;'>{c["name"]}</span>
                        {unread_html}
                      </div>
                      <div style='font-family:"Share Tech Mono",monospace;font-size:10px;color:#3a6b8a;margin-top:4px;'>
                        LAST: {c["last_msg"]} | MEMBERS: {c["members"]:,}
                      </div>
                    </div>
                    <div>{tags_html}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("### + ADD CHANNEL")
        ac1, ac2 = st.columns(2, gap="small")
        new_chan  = ac1.text_input("CHANNEL USERNAME", placeholder="@channel_name")
        chan_tags = ac2.text_input("TAGS", placeholder="OSINT,THREAT")
        if st.button("+ ADD CHANNEL TO MONITOR"):
            if new_chan:
                st.success(f"Added: {new_chan}")

    with tab2:
        st.markdown("### KEYWORD ALERTS")
        ka1, ka2 = st.columns([2, 1], gap="small")
        current_kw = ["hexstrike","th3_thirty3","THIRTY3","data breach","credential","ransomware","recon","osint"]
        with ka1:
            kw_html = " ".join([badge(kw,"green") for kw in current_kw])
            st.markdown(f"<div style='font-family:\"Share Tech Mono\",monospace;font-size:10px;color:#3a6b8a;margin-bottom:8px;'>ACTIVE KEYWORDS: {len(current_kw)}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='padding:12px;background:#0a1520;border:1px solid #0d2030;border-radius:4px;line-height:2.2;'>{kw_html}</div>", unsafe_allow_html=True)
            st.markdown("<br/>", unsafe_allow_html=True)
            new_kw = st.text_input("ADD KEYWORD", placeholder="domain.com / brand / handle")
            if st.button("+ ADD KEYWORD"):
                if new_kw: st.success(f"Keyword added: {new_kw}")
        with ka2:
            st.metric("TOTAL ALERTS",    len(alerts))
            st.metric("HIGH SEVERITY",   sum(1 for a in alerts if a["sev"] == "HIGH"))
            st.metric("ACTIVE CHANNELS", sum(1 for c in channels if c["status"] == "ACTIVE"))

        st.markdown("### RECENT ALERTS")
        for a in alerts:
            sev_map = {"HIGH":"red","MEDIUM":"yellow","LOW":"cyan"}
            sc = sev_map.get(a["sev"],"cyan")
            st.markdown(f"""
            <div class='op-card {sc}' style='padding:10px 14px;'>
              <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                <div style='flex:1;'>
                  <div style='font-family:"Share Tech Mono",monospace;font-size:10px;color:#3a6b8a;margin-bottom:4px;'>
                    [{a["ts"]}] {a["chan"]} — KW: <span style='color:#00ff88;'>{a["kw"]}</span>
                  </div>
                  <div style='font-family:"Rajdhani",sans-serif;font-size:13px;color:#b8d8eb;'>{a["msg"]}</div>
                </div>
                <div style='margin-left:12px;'>{badge(a["sev"],sc)}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    with tab3:
        st.markdown("### BOT ARCHITECTURE")
        col1, col2 = st.columns([3, 2], gap="small")
        with col1:
            st.markdown(terminal_block(
"# HEXSTRIKE TELEGRAM BOT\n"
"# ─────────────────────────────────────\n"
"# Token: export BOT_TOKEN=xxxx\n"
"# ─────────────────────────────────────\n\n"
"COMMANDS:\n"
"  /status        → System status (Tor, services)\n"
"  /alert <msg>   → Push to @th3_thirty3_alerts\n"
"  /inv list      → List active investigations\n"
"  /inv new <tgt> → Create investigation (PENDING)\n"
"  /vault <query> → Search vault notes\n"
"  /report <id>   → Quick report summary\n"
"  /circuit renew → Rotate Tor circuit\n\n"
"WEBHOOK:\n"
"  curl -X POST \\\n"
"    api.telegram.org/bot$BOT_TOKEN/setWebhook \\\n"
"    -d url=https://yourdomain.com/webhook\n\n"
"# Start (inside th3-hexstrike container):\n"
"  python3 /app/telegram_bot.py"
            ), unsafe_allow_html=True)
        with col2:
            st.markdown("### BOT STATUS")
            for bot_name, bot_status, bot_color in [("@hexstrike_ops_bot","RUNNING","#00ff88"),("@th3_thirty3_alerts","RUNNING","#00ff88")]:
                st.markdown(f"""<div class='op-card' style='padding:10px 14px;'>
                  <div style='display:flex;align-items:center;gap:8px;'>
                    <div style='width:7px;height:7px;border-radius:50%;background:{bot_color};box-shadow:0 0 6px {bot_color};'></div>
                    <div>
                      <div style='font-family:"Share Tech Mono",monospace;font-size:12px;color:#b8d8eb;'>{bot_name}</div>
                      <div style='font-family:"Share Tech Mono",monospace;font-size:10px;color:{bot_color};'>{bot_status}</div>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)
            st.markdown("<br/>", unsafe_allow_html=True)
            if st.button("⊹ PING BOTS",          use_container_width=True): st.info("All bots responding")
            if st.button("⊹ PUSH STATUS ALERT",   use_container_width=True): st.success("Alert sent to @th3_thirty3_alerts")
            if st.button("⊹ CLEAR ALERT QUEUE",   use_container_width=True): st.success("Alert queue cleared")



{
    "OPERATIONS":    page_operations,
    "INVESTIGATIONS":page_investigations,
    "TOR OPSEC":     page_tor,
    "REPORT GEN":    page_report,
    "VAULT SEARCH":  page_vault,
    "CONFIGURATION": page_config,
    "TELEGRAM":      page_telegram,
}.get(st.session_state.page, page_operations)()
