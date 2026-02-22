# HexStrike Advanced Integration Guide

## Overview

Ascended33 now includes a comprehensive HexStrike integration with:

- **MCP Wrapper**: Professional client for HexStrike with connection pooling, retries, and health checks
- **Async Worker**: Background job queue with priority scheduling and task management
- **Vault Cache**: Automatic caching of results to Obsidian
- **Streamlit Dashboard**: Rich UI for launching tools and monitoring jobs

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────┐
│  Streamlit Dashboard (pages/hexstrike_tools.py)          │
│  ├─ 🚀 Launch Tool                                      │
│  ├─ 📊 Monitor Jobs                                     │
│  ├─ 📈 Results & Analytics                              │
│  └─ ⚙️ Settings                                         │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  Worker Queue (workers/hexstrike_worker.py)             │
│  ├─ Task Priority Scheduling                            │
│  ├─ Async Job Management                                │
│  ├─ Result Callbacks                                    │
│  └─ Retry Logic & Error Handling                        │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  HexStrike MCP Client (mcp/hexstrike_wrapper.py)        │
│  ├─ Connection Pooling                                  │
│  ├─ Health Checks                                       │
│  ├─ Sync & Async Operations                             │
│  └─ Result Caching                                      │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  HexStrike Server (localhost:8888)                      │
│  ├─ nmap, masscan, nuclei, ...                          │
│  ├─ Job Management                                      │
│  └─ Results Processing                                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  Obsidian Vault Cache (cache/hexstrike_cache.py)        │
│  ├─ Job Results (HexStrike/Jobs/)                       │
│  ├─ Tool Summaries (HexStrike/Tools/)                   │
│  └─ Weekly Reports (HexStrike/Summaries/)               │
└─────────────────────────────────────────────────────────┘
```

## Usage

### 1. Access HexStrike Tools in Streamlit

```bash
streamlit run streamlit_app.py
```

Navigate to **HexStrike Tools** tab in the sidebar.

### 2. Using the MCP Wrapper (Python Scripts)

```python
from mcp.hexstrike_wrapper import HexStrikeClient

# Create client
client = HexStrikeClient("http://localhost:8888")

# Check health
if client.is_reachable:
    print("✅ HexStrike is online")

# Get available tools
tools = client.get_tools()
print(f"Available tools: {tools}")

# Run a scan synchronously
result = client.run_scan(
    tool="nmap",
    params={"target": "192.168.1.0/24", "scan_type": "-sV"},
    wait=True,
    timeout=300
)

# Get job status
status = client.get_job_status(job_id)

# Run asynchronously (fire-and-forget)
job_data = await client.run_scan_async(
    tool="nuclei",
    params={"target": "https://example.com", "templates": ["cves"]}
)

print(f"Job ID: {job_data['job_id']}")
```

### 3. Using the Worker Queue

```python
from workers.hexstrike_worker import get_worker, TaskPriority

# Get worker singleton
worker = get_worker()
worker.start()

# Submit a high-priority task
task_id = worker.submit_task(
    tool="masscan",
    params={"target": "10.0.0.0/8", "ports": "1-1000", "rate": 5000},
    priority=TaskPriority.HIGH,
    cache_result=True,
    callback=lambda task_id, result: print(f"Task {task_id} completed!")
)

# Monitor task
status = worker.get_task_status(task_id)
print(f"Task status: {status}")

# Wait for completion
results = worker.wait_all(timeout=600)

worker.stop()
```

### 4. Vault Caching

Results are automatically cached to Obsidian in this structure:

```
HexStrike/
├── Jobs/
│   ├── 2026-02-19/
│   │   ├── job-uuid-1.md
│   │   └── job-uuid-2.md
│   └── 2026-02-20/
├── Tools/
│   ├── nmap.md
│   ├── masscan.md
│   └── nuclei.md
└── Summaries/
    └── weekly-02-19.md
```

Each cached job includes:
- Job metadata (ID, timestamps, duration)
- Tool parameters
- Full results in JSON
- Error information if applicable
- Obsidian tags for searching

## Streamlit Dashboard Features

### 🚀 Launch Tool Tab

- **Tool Selection**: Choose from nmap, masscan, nuclei, or custom tools
- **Parameter Builder**: Context-sensitive forms for each tool
- **Priority Levels**: Normal, High, Urgent
- **Options**: 
  - Auto-cache results to Obsidian
  - Notifications on completion
- **Real-time feedback**: Task ID generation and tracking

### 📊 Monitor Jobs Tab

- **Live Job List**: See all running, pending, and completed jobs
- **Status Indicators**: Color-coded status (running, completed, failed)
- **Action Buttons**: Cancel running jobs
- **Statistics**: Total, completed, running, failed counts
- **Auto-refresh**: Configurable refresh intervals (5s, 10s, 30s)

### 📈 Results Tab

#### Recent Jobs
- View completed job details
- See execution time and status
- Inspect full result JSON
- Time since completion

#### Tool Stats
- Runs per tool
- Success rate per tool
- Performance metrics
- Trend analysis

#### Export
- Download results as JSON
- Save to local file or Obsidian

### ⚙️ Settings Tab

- Server configuration display
- Worker settings
- Cache management
- Connection testing

## Task Priority System

```python
from workers.hexstrike_worker import TaskPriority

TaskPriority.URGENT   # 0 - Highest priority
TaskPriority.HIGH     # 1
TaskPriority.NORMAL   # 2 (default)
TaskPriority.LOW      # 3 - Lowest priority
```

Tasks are processed by priority, then by submission time.

## Error Handling & Retries

The worker automatically retries failed tasks:
- Max retries: 3 (configurable)
- Backoff: 5s * retry_count
- Status tracking: Failed tasks are marked after max retries

```python
# Customize retries
task = Task(
    task_id=task_id,
    tool="nmap",
    params={...},
    max_retries=5,  # Custom retry count
    ...
)
```

## Performance Considerations

### Concurrent Jobs
- Default: 3 worker threads
- Customize with `max_workers` parameter:

```python
worker = HexStrikeWorker(
    hexstrike_url="http://localhost:8888",
    max_workers=5
)
```

### Timeouts
- Default job timeout: 300s (5 minutes)
- Default health check timeout: 5s
- Customize per job:

```python
result = client.run_scan(
    tool="nmap",
    params={...},
    timeout=600  # 10 minutes
)
```

### Caching
- Session-based cache (in-memory)
- Configurable per client:

```python
client = HexStrikeClient(enable_caching=True)
client.clear_cache()  # Manual clear
```

## Integration with Other Components

### With OSINT Tools
```python
from workers.hexstrike_worker import get_worker
from scripts.osint.investigators import OSINTEngine

worker = get_worker()

# Launch nmap then feed results to OSINT
task_id = worker.submit_task(
    tool="nmap",
    params={"target": "example.com"},
    callback=lambda tid, result: 
        OSINTEngine.analyze(result)
)
```

### With Vault Sync
Results are automatically synced to Obsidian via `vault_sync.vault_api.ObsidianVaultClient`.

### With Kali VM
HexStrike instances can run on remote Kali VMs via SSH:

```python
from mcp.kali_ssh_client import KaliSSHClient

with KaliSSHClient.from_config() as kali:
    hexstrike_status = kali.hexstrike_status()
    if not hexstrike_status:
        kali.start_hexstrike()
```

## Troubleshooting

### HexStrike Server Offline

```python
client = HexStrikeClient()

if not client.is_reachable:
    print("❌ HexStrike is offline")
    print("Start HexStrike: docker-compose up hexstrike")
```

### Job Timeout

```python
# Increase timeout for large scans
result = client.run_scan(
    tool="masscan",
    params={"target": "0.0.0.0/0", "rate": 1000},
    timeout=1800  # 30 minutes
)
```

### Missing Dependencies

```bash
# Install requirements
pip install requests aiohttp
```

### Vault Cache Not Working

```python
# Check vault configuration
from vault_sync.vault_api import ObsidianVaultClient

vault = ObsidianVaultClient.from_config()
if not vault.is_reachable:
    print("Obsidian REST API not reachable")
```

## Best Practices

1. **Use appropriate priorities**: Don't overuse URGENT for all tasks
2. **Monitor job queue**: Use the Streamlit dashboard to prevent overload
3. **Cache results**: Enable caching for result persistence
4. **Set reasonable timeouts**: Avoid extremely long timeouts for large scans
5. **Use callbacks**: Notify other systems of completion
6. **Test connections**: Use `test_connection()` before running production jobs
7. **Review logs**: Check worker logs for issues and performance metrics

## Future Enhancements

- [ ] Web API wrapper (FastAPI endpoints)
- [ ] Advanced scheduling (cron-based tasks)
- [ ] Machine learning-based parameter optimization
- [ ] Multi-target scanning with batching
- [ ] Result comparison and Delta analysis
- [ ] Template-based scanning workflows
- [ ] Integration with Shodan/Censys APIs

## Support & Debugging

Enable debug logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("hexstrike")
logger.setLevel(logging.DEBUG)
```

Check worker logs:
```bash
tail -f ascended33.log | grep hexstrike
```

Test the integration:
```bash
python verify_connections.py
```

---

**Generated**: February 19, 2026
**Version**: 2.0 (Advanced Integration)
**Status**: ✅ Stable & Production Ready
