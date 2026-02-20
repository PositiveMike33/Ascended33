"""
hexstrike_worker_api.py — FastAPI app for th3-hexstrike container

Expose le HexStrikeWorker via une API REST.
uvicorn workers.hexstrike_worker_api:app --host 0.0.0.0 --port 8001
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, Optional
from datetime import datetime

from workers.hexstrike_worker import HexStrikeWorker, TaskPriority, get_worker, shutdown_worker

app = FastAPI(
    title="HexStrike Worker API",
    description="Async job queue for HexStrike security tools",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Pydantic Models ──────────────────────────────────────────────────────────

class TaskRequest(BaseModel):
    tool: str
    params: Dict[str, Any] = {}
    priority: str = "NORMAL"
    cache_result: bool = True


class TaskResponse(BaseModel):
    task_id: str
    tool: str
    status: str
    message: str


# ── Lifespan ─────────────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    get_worker(hexstrike_url="http://th3-hexstrike:8001")


@app.on_event("shutdown")
async def shutdown():
    shutdown_worker()


# ── Health & Status ──────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "th3-hexstrike-worker",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/status")
async def status():
    worker = get_worker()
    tasks = worker.get_all_tasks()
    return {
        "status": "running",
        "tasks_total": len(tasks),
        "tasks_pending": sum(1 for t in tasks.values() if t and t.get("status") == "pending"),
        "tasks_completed": sum(1 for t in tasks.values() if t and t.get("status") == "completed"),
        "tasks_failed": sum(1 for t in tasks.values() if t and t.get("status") == "failed"),
    }


# ── Task Endpoints ───────────────────────────────────────────────────────────

@app.post("/job/submit", response_model=TaskResponse)
async def submit_job(request: TaskRequest):
    """Submit a new security tool job."""
    try:
        priority = TaskPriority[request.priority.upper()]
    except KeyError:
        priority = TaskPriority.NORMAL

    worker = get_worker()
    task_id = worker.submit_task(
        tool=request.tool,
        params=request.params,
        priority=priority,
        cache_result=request.cache_result,
    )

    return TaskResponse(
        task_id=task_id,
        tool=request.tool,
        status="pending",
        message=f"Task {task_id} submitted successfully",
    )


@app.get("/job/{task_id}")
async def get_job(task_id: str):
    """Get job status and result."""
    worker = get_worker()
    task_status = worker.get_task_status(task_id)

    if not task_status:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return task_status


@app.get("/jobs")
async def list_jobs():
    """List all jobs."""
    worker = get_worker()
    return {"jobs": worker.get_all_tasks()}


@app.post("/job/{task_id}/cancel")
async def cancel_job(task_id: str):
    """Cancel a pending job."""
    worker = get_worker()
    cancelled = worker.cancel_task(task_id)

    if not cancelled:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found or already completed")

    return {"task_id": task_id, "status": "cancelled"}


# ── Tools Info ───────────────────────────────────────────────────────────────

@app.get("/tools")
async def list_tools():
    """List available security tools."""
    return {
        "tools": [
            "nmap", "masscan", "nuclei", "amass", "subfinder",
            "httpx", "feroxbuster", "gobuster", "sqlmap", "nikto",
            "wfuzz", "ffuf", "hydra", "john", "hashcat",
            "metasploit", "burpsuite", "zaproxy", "xsstrike",
        ]
    }
