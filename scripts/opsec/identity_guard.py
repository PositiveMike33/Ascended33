"""
identity_guard.py — PII detection and scrubbing before any external output.

Scans files or text for personal identifiable information (PII) before
committing, publishing, or transmitting. Protects the operator's identity.

Detects:
  - Real name patterns (configurable via IDENTITY_PATTERNS)
  - Private IP addresses hardcoded in source
  - Windows personal user paths (C:\\Users\\<username>\\)
  - API key / token patterns (common prefixes)
  - Email addresses
  - SSH private key material
  - Loaded from config.yaml: custom client names, personal keywords

Usage:
    # Scan all tracked files
    python3 scripts/opsec/identity_guard.py --all

    # Scan specific files
    python3 scripts/opsec/identity_guard.py --files scripts/osint/domain_recon.py

    # Scan text piped from stdin
    echo "my report" | python3 scripts/opsec/identity_guard.py --stdin

    # Programmatic use
    from scripts.opsec.identity_guard import scan_text, scan_file, GuardResult
    result = scan_text("some output containing Michael Gauthier")
    if result.has_findings:
        print(result.report())
        sys.exit(1)
"""

import logging
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------
# PII PATTERNS
# Each entry: (pattern_name, compiled_regex, severity)
# severity: "critical" | "high" | "medium"
# ----------------------------------------------------------------

# Real-name fragments — add operator's known aliases here
_NAME_FRAGMENTS: list[str] = [
    r"Michael\s+Gauthier(?:\s+Guillet)?",
    r"Gauthier\s+Guillet",
    r"M\.?\s*Gauthier",
]

# Common API key / token prefixes
_API_KEY_PATTERNS: list[str] = [
    r"ghp_[A-Za-z0-9]{36,}",          # GitHub Personal Access Token
    r"github_pat_[A-Za-z0-9_]{80,}",   # GitHub fine-grained PAT
    r"sk-[A-Za-z0-9]{32,}",            # OpenAI / generic sk- key
    r"xoxb-[0-9]+-[A-Za-z0-9-]+",      # Slack Bot Token
    r"xoxp-[0-9]+-[A-Za-z0-9-]+",      # Slack User Token
    r"AKIA[0-9A-Z]{16}",               # AWS Access Key ID
    r"Bearer\s+[A-Za-z0-9\-._~+/]{20,}=*",  # Generic Bearer token
    r"[Aa][Pp][Ii]_?[Kk][Ee][Yy]\s*[=:]\s*['\"][A-Za-z0-9\-._]{16,}['\"]",
]

# Private IP ranges (RFC1918) — 192.168.x.x, 10.x.x.x, 172.16-31.x.x
_PRIVATE_IP_PATTERN = (
    r"\b(?:"
    r"192\.168\.\d{1,3}\.\d{1,3}"
    r"|10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}"
    r")\b"
)

# Windows personal user paths with a non-generic username
# Pattern: drive:\Users\<non-generic-name>\ — excludes Public, Default, TEMP
_WINDOWS_USER_PATH_PATTERN = (
    r"[Cc]:\\[Uu]sers\\(?!(?:Public|Default|All Users|TEMP)[\\/ ])[^\s\\\"']{3,}\\"
)

# Email addresses (simple heuristic)
_EMAIL_PATTERN = r"\b[A-Za-z0-9._%+\-]{2,}@[A-Za-z0-9.\-]{2,}\.[A-Za-z]{2,}\b"

# SSH private key material
_SSH_KEY_PATTERN = r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"

# Compile all patterns into a flat list of (name, regex, severity)
_COMPILED_PATTERNS: list[tuple[str, re.Pattern[str], str]] = []


def _build_patterns(extra_keywords: Optional[list[str]] = None) -> None:
    """Build the compiled pattern list (called once at import + after config load)."""
    global _COMPILED_PATTERNS
    _COMPILED_PATTERNS = []

    for frag in _NAME_FRAGMENTS:
        _COMPILED_PATTERNS.append(
            ("real_name", re.compile(frag, re.IGNORECASE), "critical")
        )

    for pat in _API_KEY_PATTERNS:
        _COMPILED_PATTERNS.append(
            ("api_key", re.compile(pat), "critical")
        )

    _COMPILED_PATTERNS.append(
        ("private_ip", re.compile(_PRIVATE_IP_PATTERN), "high")
    )
    _COMPILED_PATTERNS.append(
        ("windows_user_path", re.compile(_WINDOWS_USER_PATH_PATTERN), "high")
    )
    _COMPILED_PATTERNS.append(
        ("email_address", re.compile(_EMAIL_PATTERN), "medium")
    )
    _COMPILED_PATTERNS.append(
        ("ssh_private_key", re.compile(_SSH_KEY_PATTERN), "critical")
    )

    if extra_keywords:
        for kw in extra_keywords:
            escaped = re.escape(kw)
            _COMPILED_PATTERNS.append(
                ("custom_keyword", re.compile(escaped, re.IGNORECASE), "high")
            )


_build_patterns()


# ----------------------------------------------------------------
# DATA CLASSES
# ----------------------------------------------------------------

@dataclass
class Finding:
    """A single PII finding in a file or text block."""
    pattern_name: str
    severity: str
    line_number: int
    line_content: str
    matched_value: str
    source: str = "<text>"


@dataclass
class GuardResult:
    """Result of a full identity guard scan."""
    findings: list[Finding] = field(default_factory=list)
    files_scanned: int = 0
    lines_scanned: int = 0

    @property
    def has_findings(self) -> bool:
        return len(self.findings) > 0

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "critical")

    @property
    def high_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "high")

    def report(self) -> str:
        """Human-readable summary of all findings."""
        if not self.has_findings:
            return (
                f"[identity_guard] CLEAN — {self.files_scanned} file(s), "
                f"{self.lines_scanned} lines scanned. No PII detected."
            )

        lines = [
            f"[identity_guard] ⚠️  {len(self.findings)} PII finding(s) detected "
            f"({self.critical_count} CRITICAL, {self.high_count} HIGH)",
            f"Files scanned: {self.files_scanned} | Lines scanned: {self.lines_scanned}",
            "",
        ]
        for f in self.findings:
            severity_tag = f.severity.upper().ljust(8)
            lines.append(
                f"  [{severity_tag}] [{f.pattern_name}] "
                f"{f.source}:{f.line_number} — {f.line_content.strip()[:120]}"
            )
        return "\n".join(lines)


# ----------------------------------------------------------------
# CORE SCAN FUNCTIONS
# ----------------------------------------------------------------

# Lines that contain this marker are whitelisted (false positive suppression)
_ALLOWLIST_MARKER = "identity_guard: allowlist"

# File extensions to scan
_SCANNABLE_EXTENSIONS = {
    ".py", ".yaml", ".yml", ".json", ".md", ".txt", ".sh", ".bat", ".ps1",
    ".env", ".cfg", ".ini", ".toml",
}

# Files / dirs to always skip
_SKIP_PATHS = {
    ".secrets.baseline",
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules",
}


def scan_text(text: str, source: str = "<text>") -> GuardResult:
    """
    Scan a block of text for PII patterns.

    Args:
        text: The text content to scan.
        source: Label used in findings (e.g., filename).

    Returns:
        GuardResult with all findings.
    """
    result = GuardResult(files_scanned=1)
    for line_num, line in enumerate(text.splitlines(), start=1):
        result.lines_scanned += 1
        if _ALLOWLIST_MARKER in line:
            continue
        for pattern_name, regex, severity in _COMPILED_PATTERNS:
            match = regex.search(line)
            if match:
                result.findings.append(Finding(
                    pattern_name=pattern_name,
                    severity=severity,
                    line_number=line_num,
                    line_content=line,
                    matched_value=match.group(0),
                    source=source,
                ))
                break  # one finding per line is enough
    return result


def scan_file(path: Path) -> GuardResult:
    """
    Scan a single file for PII patterns.

    Args:
        path: Path to the file to scan.

    Returns:
        GuardResult for this file.
    """
    result = GuardResult()
    if not path.is_file():
        return result
    if path.suffix.lower() not in _SCANNABLE_EXTENSIONS:
        return result
    if any(skip in path.parts for skip in _SKIP_PATHS):
        return result

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        logger.warning("Cannot read %s: %s", path, e)
        return result

    file_result = scan_text(text, source=str(path))
    result.findings.extend(file_result.findings)
    result.files_scanned = 1
    result.lines_scanned = file_result.lines_scanned
    return result


def scan_directory(root: Path, recursive: bool = True) -> GuardResult:
    """
    Scan all scannable files under a directory.

    Args:
        root: Root directory to scan.
        recursive: If True, scan subdirectories.

    Returns:
        Aggregated GuardResult for all files.
    """
    combined = GuardResult()
    pattern = "**/*" if recursive else "*"
    for path in root.glob(pattern):
        if path.is_file() and not any(skip in path.parts for skip in _SKIP_PATHS):
            file_result = scan_file(path)
            combined.findings.extend(file_result.findings)
            combined.files_scanned += file_result.files_scanned
            combined.lines_scanned += file_result.lines_scanned
    return combined


def load_custom_keywords_from_config() -> list[str]:
    """
    Load custom PII keywords from config.yaml (client names, personal keywords).

    Returns:
        List of keyword strings to add to patterns, or empty list if unavailable.
    """
    try:
        import yaml  # type: ignore[import]
        config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
        if not config_path.exists():
            return []
        with config_path.open() as f:
            cfg = yaml.safe_load(f)
        return cfg.get("identity_guard", {}).get("custom_keywords", [])
    except Exception as e:
        logger.debug("Could not load custom keywords from config: %s", e)
        return []


# ----------------------------------------------------------------
# CLI ENTRY POINT
# ----------------------------------------------------------------

def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="identity_guard — PII detector for Ascended33",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/opsec/identity_guard.py --all
  python3 scripts/opsec/identity_guard.py --files report.md notes.txt
  echo "text to check" | python3 scripts/opsec/identity_guard.py --stdin
        """,
    )
    parser.add_argument("--all", action="store_true", help="Scan entire repo")
    parser.add_argument("--files", nargs="+", help="Scan specific file(s)")
    parser.add_argument("--stdin", action="store_true", help="Scan text from stdin")
    parser.add_argument("--no-fail", action="store_true",
                        help="Report findings but exit 0 (useful in CI info mode)")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )

    # Load custom keywords from config (client names, etc.)
    extra_kw = load_custom_keywords_from_config()
    if extra_kw:
        _build_patterns(extra_keywords=extra_kw)
        logger.debug("Loaded %d custom keywords from config.yaml", len(extra_kw))

    result = GuardResult()

    if args.stdin:
        text = sys.stdin.read()
        result = scan_text(text, source="<stdin>")

    elif args.files:
        for f in args.files:
            r = scan_file(Path(f))
            result.findings.extend(r.findings)
            result.files_scanned += r.files_scanned
            result.lines_scanned += r.lines_scanned

    elif args.all:
        repo_root = Path(__file__).parent.parent.parent
        result = scan_directory(repo_root)

    else:
        parser.print_help()
        return 0

    print(result.report())

    if result.has_findings and not args.no_fail:
        print(
            "\n  Fix: remove or redact PII before committing. "
            "Add '# identity_guard: allowlist' to suppress false positives."
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
