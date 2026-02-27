# 00 — Operation Metadata

| Field | Value |
|-------|-------|
| **Hat color** | `WHITE` (WHITE-HAT) |
| **Operation type** | `hardening_report` |
| **Target** | `th3-kali` |
| **Timestamp (UTC)** | `2026-02-27T13:14:08.932991Z` |
| **Job ID** | `cli-test-001` |
| **Traffic routing** | Docker-internal (direct) |
| **Internal target** | Yes |
| **Authorization** | Whitelist confirmed or external authorized scope |

## Tools invoked

- `recon`
- `vulnerabilities`
- `countermeasures`
- `summary`

## Scope notes

- Internal containers in scope: ['th3-gemini', 'th3-kali', 'th3-streamlit']
- Protected containers (never targeted): ['nexus-mongo', 'th3-gpu-trainer', 'th3-redis', 'th3-tor', 'vault-brain']
