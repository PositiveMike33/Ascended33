# 00 — Operation Metadata

| Field | Value |
|-------|-------|
| **Hat color** | `BLACK` (BLACK-HAT) |
| **Operation type** | `ttp_simulation` |
| **Target** | `th3-gemini` |
| **Timestamp (UTC)** | `2026-02-27T13:09:05.710563Z` |
| **Job ID** | `test-003` |
| **Traffic routing** | Docker-internal (direct) |
| **Internal target** | Yes |
| **Authorization** | Whitelist confirmed or external authorized scope |

## Tools invoked

- `nmap`
- `masscan`
- `gobuster`

## Scope notes

- Internal containers in scope: ['th3-gemini', 'th3-kali', 'th3-streamlit']
- Protected containers (never targeted): ['nexus-mongo', 'th3-gpu-trainer', 'th3-redis', 'th3-tor', 'vault-brain']
