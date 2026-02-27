# 05 — Countermeasures & Defensive Report

## How the attack works (red-team perspective)

> Explain the attack vector in plain language so a blue-team engineer
> understands it without needing security expertise. Be specific to
> **th3-gemini** and the findings in 02_vulnerabilities.md.

## Remediation steps

### Finding: `nmap`

**Countermeasure:** Restrict exposed ports via firewall rules (iptables/nftables). Allow only required services.

**Reference:** https://owasp.org/www-project-top-ten/

### Finding: `gobuster`

**Countermeasure:** Remove debug/admin endpoints from production. Return 404 (not 403) for sensitive paths to avoid enumeration.

**Reference:** https://owasp.org/www-project-top-ten/

## Concrete rules to apply

```bash
# Example — replace with specific commands for this finding
# iptables -A INPUT -p tcp --dport <PORT> -j DROP
# systemctl disable <vulnerable-service>
# apt-get install --only-upgrade <package>
```

## Validation plan

1. Apply the rules above on `th3-gemini`.
2. Re-run the same HexStrike scan (same `operation_type` + options).
3. Confirm the finding no longer appears in the output.
4. Document result in `06_validation.md`.
