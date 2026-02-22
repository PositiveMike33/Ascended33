"""
operation_logger.py — Log security operations to Obsidian Vault

Every operation (OSINT, pentest, dark web scan, etc.) is timestamped and logged
to the Vault for audit trail, knowledge retention, and operational security.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class OperationLogger:
    """Logs security operations to Obsidian Vault"""

    def __init__(self, vault_client=None):
        self.vault = vault_client
        self.operation_id = None
        self.start_time = None
        self.operation_path = None

    def start_operation(
        self,
        operation_name: str,
        operation_type: str,
        target: str,
        opsec_status: dict,
        mission_description: str = "",
    ) -> str:
        """
        Log the start of an operation to Vault

        Args:
            operation_name: Name of operation (e.g., "OSINT - target.com")
            operation_type: Type (osint, pentest, threat_intel, ctf, dark_web)
            target: Target description
            opsec_status: OPSEC verification dict
            mission_description: Detailed mission description

        Returns:
            operation_id (timestamp-based)
        """
        if not self.vault:
            logger.warning("Vault client not initialized — skipping operation logging")
            return None

        self.start_time = datetime.now()
        self.operation_id = self.start_time.strftime("%Y%m%d_%H%M%S")

        tags = [
            "operation",
            operation_type.lower(),
            "self-test",
        ]

        opsec_section = f"""
## OPSEC Verification
| Field | Value |
|-------|-------|
| VPN Active | {opsec_status.get('vpn_active', False)} |
| VPN Provider | {opsec_status.get('vpn_provider', 'N/A')} |
| Tor Active | {opsec_status.get('tor_active', False)} |
| Current IP | `{opsec_status.get('current_ip', 'unknown')}` |
| Safe | {opsec_status.get('safe', False)} |
"""

        content = f"""# {operation_name}

**Operation ID**: `{self.operation_id}`
**Type**: {operation_type}
**Target**: {target}
**Self-Testing**: Yes (cible: moi-même)
**Started**: {self.start_time.isoformat()}

## Mission
{mission_description or '[No description]'}

{opsec_section}

## Findings
[To be populated during operation]

## Timeline
- **{self.start_time.strftime('%H:%M:%S')}** — Operation started

## Status
🔄 **In Progress**

---
*Auto-logged by Ascended33 OPSEC system*
"""

        self.operation_path = f"Security/Operations/{self.start_time.strftime('%Y-%m-%d')}/{self.operation_id}-{operation_name.replace(' ', '-')}.md"

        try:
            self.vault.create_note(self.operation_path, content, tags=tags)
            logger.info(f"✓ Operation logged: {self.operation_path}")
            return self.operation_id
        except Exception as e:
            logger.error(f"Failed to log operation: {e}")
            return None

    def log_finding(
        self,
        finding_type: str,
        title: str,
        description: str,
        severity: str = "medium",
        evidence: Optional[dict] = None,
    ) -> bool:
        """
        Log a finding within an operation

        Args:
            finding_type: Type of finding (vulnerability, info, credential, etc.)
            title: Finding title
            description: Detailed description
            severity: Risk level (critical, high, medium, low, info)
            evidence: Optional dict with evidence/proof

        Returns:
            True if logged successfully
        """
        if not self.vault or not self.operation_path:
            logger.warning("Cannot log finding — no active operation")
            return False

        try:
            # Read current note
            current_content = self.vault.read_note(self.operation_path)

            # Build finding entry
            finding_section = f"""
### [{severity.upper()}] {title}
**Type**: {finding_type}
**Logged**: {datetime.now().isoformat()}

{description}
"""

            if evidence:
                finding_section += f"\n**Evidence**:\n```json\n{json.dumps(evidence, indent=2)}\n```\n"

            # Insert before Status section
            updated_content = current_content.replace(
                "## Status",
                f"## Findings\n{finding_section}\n\n## Status"
            )

            # Update note
            self.vault.update_note(self.operation_path, updated_content)
            logger.info(f"✓ Finding logged: {title}")
            return True

        except Exception as e:
            logger.error(f"Failed to log finding: {e}")
            return False

    def end_operation(
        self,
        status: str = "completed",
        summary: str = "",
        total_findings: int = 0,
    ) -> bool:
        """
        Close operation log with final status

        Args:
            status: final status (completed, failed, aborted)
            summary: Operation summary
            total_findings: Number of findings discovered

        Returns:
            True if updated successfully
        """
        if not self.vault or not self.operation_path:
            logger.warning("Cannot end operation — no active operation")
            return False

        try:
            current_content = self.vault.read_note(self.operation_path)
            end_time = datetime.now()

            status_icon = {
                "completed": "✅",
                "failed": "❌",
                "aborted": "⛔",
            }.get(status, "❓")

            duration = end_time - self.start_time
            duration_str = str(duration).split('.')[0]  # Remove microseconds

            # Update timeline and status
            updated_content = current_content.replace(
                "## Status\n🔄 **In Progress**",
                f"""## Summary
- **Total Findings**: {total_findings}
- **Duration**: {duration_str}
- **Summary**: {summary or '[See findings above]'}

## Status
{status_icon} **{status.upper()}** at {end_time.isoformat()}""",
            )

            self.vault.update_note(self.operation_path, updated_content)
            logger.info(f"✓ Operation closed: {status}")
            return True

        except Exception as e:
            logger.error(f"Failed to end operation: {e}")
            return False


def get_operation_logger(config_path: str = "config/config.yaml"):
    """Factory function to create operation logger with Vault client"""
    try:
        from vault_sync.vault_api import ObsidianVaultClient

        vault = ObsidianVaultClient.from_config(config_path)
        return OperationLogger(vault)
    except Exception as e:
        logger.warning(f"Failed to initialize OperationLogger: {e}")
        return OperationLogger(None)
