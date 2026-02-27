# 05 — Countermeasures & Defensive Report

## How the attack works (red-team perspective)

> Explain the attack vector in plain language so a blue-team engineer
> understands it without needing security expertise. Be specific to
> **th3-kali** and the findings in 02_vulnerabilities.md.

## Remediation steps

### Finding: `vuln`

**Countermeasure:** Patch identified vulnerabilities. Re-run Nuclei post-patch to confirm remediation.

**Reference:** https://owasp.org/www-project-top-ten/

## Concrete rules to apply

```bash
# Example — replace with specific commands for this finding
# iptables -A INPUT -p tcp --dport <PORT> -j DROP
# systemctl disable <vulnerable-service>
# apt-get install --only-upgrade <package>
```

## Validation plan

1. Apply the rules above on `th3-kali`.
2. Re-run the same HexStrike scan (same `operation_type` + options).
3. Confirm the finding no longer appears in the output.
4. Document result in `06_validation.md`.
