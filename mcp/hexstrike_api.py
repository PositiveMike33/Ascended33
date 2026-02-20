"""
hexstrike_api.py — FastAPI app for th3-hackergpt container

Expose le HexStrikeClient via une API REST.
uvicorn mcp.hexstrike_api:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime

from mcp.hexstrike_client import HexStrikeClient

app = FastAPI(
    title="HackerGPT — HexStrike API",
    description="Claude + HexStrike AI security agent interface",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Client singleton (connects to th3-hexstrike on port 8001)
_client: Optional[HexStrikeClient] = None


def get_client() -> HexStrikeClient:
    global _client
    if _client is None:
        _client = HexStrikeClient(base_url="http://th3-hexstrike:8001")
    return _client


# ── Pydantic Models ──────────────────────────────────────────────────────────

class ToolRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any] = {}


class AgentRequest(BaseModel):
    agent_name: str
    mission: str
    context: Optional[Dict[str, Any]] = None


class ReconRequest(BaseModel):
    target: str
    ports: str = "top-1000"


class WebScanRequest(BaseModel):
    target_url: str


class CVERequest(BaseModel):
    cve_id: str


class CTFRequest(BaseModel):
    challenge_description: str
    files: Optional[List[str]] = None


# ── Health ───────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    client = get_client()
    hexstrike_up = client.is_reachable()
    return {
        "status": "healthy",
        "service": "th3-hackergpt",
        "hexstrike_connected": hexstrike_up,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/status")
async def status():
    client = get_client()
    return {
        "status": "running",
        "hexstrike_url": client.base_url,
        "hexstrike_reachable": client.is_reachable(),
    }


# ── Tool Endpoints ───────────────────────────────────────────────────────────

@app.get("/tools")
async def list_tools():
    """List all available security tools."""
    client = get_client()
    tools = client.list_tools()
    return {"tools": tools}


@app.post("/tools/call")
async def call_tool(request: ToolRequest):
    """Execute a specific security tool."""
    client = get_client()
    try:
        result = client.run_tool(request.tool_name, request.parameters)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Agent Endpoints ──────────────────────────────────────────────────────────

@app.post("/agents/run")
async def run_agent(request: AgentRequest):
    """Invoke a HexStrike AI agent."""
    client = get_client()
    try:
        result = client.run_agent(request.agent_name, request.mission, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Convenience Endpoints ─────────────────────────────────────────────────────

@app.post("/recon/network")
async def network_recon(request: ReconRequest):
    """Run network reconnaissance."""
    client = get_client()
    try:
        return client.network_recon(request.target, request.ports)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/recon/web")
async def web_scan(request: WebScanRequest):
    """Run web application security scan."""
    client = get_client()
    try:
        return client.web_scan(request.target_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cve")
async def cve_lookup(request: CVERequest):
    """Look up CVE details."""
    client = get_client()
    try:
        return client.cve_lookup(request.cve_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ctf/analyze")
async def ctf_analyze(request: CTFRequest):
    """Analyze a CTF challenge."""
    client = get_client()
    try:
        return client.ctf_analyze(request.challenge_description, request.files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
