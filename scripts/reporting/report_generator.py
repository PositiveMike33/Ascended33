"""
report_generator.py — Core report generation pipeline for Ascended33.

Loads the appropriate template, substitutes values, and writes the report
to the Obsidian Vault (or local filesystem as fallback).

Usage:
    python3 scripts/reporting/report_generator.py \\
        --type osint \\
        --target "example.com" \\
        --output vault

    python3 scripts/reporting/report_generator.py \\
        --type pentest \\
        --engagement "client-2026-02" \\
        --output vault
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"

VAULT_PATHS = {
    "osint": "Security/OSINT",
    "pentest": "Security/Pentests/_Clients",
    "threat_intel": "Security/ThreatIntel",
    "ctf": "Security/CTF",
}


def _load_template(report_type: str) -> str:
    template_map = {
        "osint": "osint_report.md",
        "pentest": "pentest_report.md",
        "threat_intel": "threat_intel_report.md",
        "ctf": "ctf_writeup.md",
    }
    template_file = TEMPLATES_DIR / template_map[report_type]
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")
    return template_file.read_text(encoding="utf-8")


def _apply_base_vars(content: str, extra: dict) -> str:
    now = datetime.now()
    base_vars = {
        "{{date}}": now.strftime("%Y-%m-%d"),
        "{{generated_at}}": now.strftime("%Y-%m-%d %H:%M UTC"),
        "{{year}}": str(now.year),
    }
    base_vars.update(extra)
    for placeholder, value in base_vars.items():
        content = content.replace(placeholder, value)
    return content


def generate_report(
    report_type: str,
    variables: dict,
    output: str = "vault",
    filename: str | None = None,
) -> str:
    """
    Generate a security report from a template.

    Args:
        report_type: "osint" | "pentest" | "threat_intel" | "ctf"
        variables: Dict of {{placeholder}} → value substitutions
        output: "vault" | "local" | "both"
        filename: Override the auto-generated filename

    Returns:
        The generated report content as a string.
    """
    template = _load_template(report_type)
    content = _apply_base_vars(template, variables)

    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = variables.get("{{target}}", variables.get("{{engagement}}", "report"))
    slug = slug.replace(" ", "-").replace(".", "-").lower()
    note_filename = filename or f"{date_str}-{slug}.md"

    if output in ("vault", "both"):
        try:
            from vault_sync.vault_api import ObsidianVaultClient
            vault = ObsidianVaultClient.from_config()
            vault_path = f"{VAULT_PATHS[report_type]}/{note_filename}"
            vault.create_note(vault_path, content)
            logger.info("Report written to Vault: %s", vault_path)
        except Exception as e:
            logger.error("Failed to write to Vault: %s", e)

    if output in ("local", "both"):
        output_dir = Path("./output")
        output_dir.mkdir(exist_ok=True)
        local_path = output_dir / note_filename
        local_path.write_text(content, encoding="utf-8")
        logger.info("Report written locally: %s", local_path)

    return content


def main():
    parser = argparse.ArgumentParser(description="Ascended33 Report Generator")
    parser.add_argument("--type", required=True, choices=["osint", "pentest", "threat_intel", "ctf"])
    parser.add_argument("--target", help="Target for OSINT/recon reports")
    parser.add_argument("--engagement", help="Engagement name for pentest reports")
    parser.add_argument("--output", default="vault", choices=["vault", "local", "both"])
    args = parser.parse_args()

    variables = {}
    if args.target:
        variables["{{target}}"] = args.target
    if args.engagement:
        variables["{{engagement}}"] = args.engagement
        variables["{{client_name}}"] = args.engagement

    content = generate_report(args.type, variables, output=args.output)
    print(f"Report generated ({len(content)} chars). Output: {args.output}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
