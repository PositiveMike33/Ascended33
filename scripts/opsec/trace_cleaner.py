"""
trace_cleaner.py — Post-operation artifact cleanup.

Removes temporary files, logs, scan outputs, and other artifacts
generated during security operations. Run after every operation
to minimize the local forensic footprint.

Scopes:
  local  — cleans only repo-local artifacts (output/, *.log, caches)
  full   — local + system-level (DNS cache flush, shell history artifacts)

Usage:
    python3 scripts/opsec/trace_cleaner.py --scope local
    python3 scripts/opsec/trace_cleaner.py --scope full --dry-run
    python3 scripts/opsec/trace_cleaner.py --scope full --verbose

Programmatic:
    from scripts.opsec.trace_cleaner import TraceCleaner, CleanScope
    cleaner = TraceCleaner(repo_root=Path("."))
    result = cleaner.clean(scope=CleanScope.LOCAL)
    print(result.summary())
"""

import logging
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class CleanScope(Enum):
    LOCAL = "local"
    FULL = "full"


@dataclass
class CleanResult:
    """Result of a trace-cleaning operation."""
    files_removed: list[Path] = field(default_factory=list)
    dirs_removed: list[Path] = field(default_factory=list)
    system_actions: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    dry_run: bool = False

    @property
    def total_removed(self) -> int:
        return len(self.files_removed) + len(self.dirs_removed)

    def summary(self) -> str:
        prefix = "[DRY RUN] " if self.dry_run else ""
        lines = [
            f"{prefix}[trace_cleaner] Cleanup complete.",
            f"  Files removed   : {len(self.files_removed)}",
            f"  Dirs removed    : {len(self.dirs_removed)}",
            f"  System actions  : {len(self.system_actions)}",
        ]
        if self.system_actions:
            for action in self.system_actions:
                lines.append(f"  [sys] {action}")
        if self.errors:
            lines.append(f"  Errors ({len(self.errors)}):")
            for err in self.errors:
                lines.append(f"  [ERR] {err}")
        return "\n".join(lines)


class TraceCleaner:
    """
    Cleans up post-operation artifacts from security operations.

    Args:
        repo_root: Root of the Ascended33 repository.
        dry_run: If True, report what would be deleted without deleting.
        verbose: If True, log every file touched.
    """

    # Directories to remove entirely (relative to repo root)
    _LOCAL_DIRS: list[str] = [
        "output",
        "scan_results",
        "nmap_output",
        ".osint_cache",
        "vault_sync/cache",
        "loot",
    ]

    # Glob patterns for files to remove (relative to repo root)
    _LOCAL_FILE_GLOBS: list[str] = [
        "*.log",
        "**/*.log",
        "*.pcap",
        "**/*.pcap",
        "*.cap",
        "**/*.cap",
        "*.xml",        # Nmap XML output (common artifact)
        "*.gnmap",      # Nmap grepable output
        "*.nmap",       # Nmap text output
        ".osint_*",
        "tmp_*",
        "*.tmp",
    ]

    # Files/dirs to NEVER delete
    _PROTECTED_PATHS: set[str] = {
        ".git",
        ".gitignore",
        ".pre-commit-config.yaml",
        ".secrets.baseline",
        "requirements.txt",
        "CLAUDE.md",
        "README.md",
        "LICENSE",
    }

    def __init__(
        self,
        repo_root: Path,
        dry_run: bool = False,
        verbose: bool = False,
    ) -> None:
        self.repo_root = repo_root.resolve()
        self.dry_run = dry_run
        self.verbose = verbose

    def clean(self, scope: CleanScope = CleanScope.LOCAL) -> CleanResult:
        """
        Run the cleanup for the given scope.

        Args:
            scope: CleanScope.LOCAL or CleanScope.FULL

        Returns:
            CleanResult with details of what was cleaned.
        """
        result = CleanResult(dry_run=self.dry_run)

        self._clean_local_dirs(result)
        self._clean_local_files(result)

        if scope == CleanScope.FULL:
            self._flush_dns_cache(result)
            self._clean_pip_cache(result)

        return result

    # ----------------------------------------------------------------
    # LOCAL SCOPE
    # ----------------------------------------------------------------

    def _clean_local_dirs(self, result: CleanResult) -> None:
        for rel_dir in self._LOCAL_DIRS:
            target = self.repo_root / rel_dir
            if not target.exists():
                continue
            if target.name in self._PROTECTED_PATHS:
                continue
            if self.verbose:
                logger.info("Removing directory: %s", target)
            if not self.dry_run:
                try:
                    shutil.rmtree(target)
                    result.dirs_removed.append(target)
                except OSError as e:
                    result.errors.append(f"rmdir {target}: {e}")
            else:
                result.dirs_removed.append(target)

    def _clean_local_files(self, result: CleanResult) -> None:
        for glob_pattern in self._LOCAL_FILE_GLOBS:
            for path in self.repo_root.glob(glob_pattern):
                if not path.is_file():
                    continue
                if self._is_protected(path):
                    continue
                if self.verbose:
                    logger.info("Removing file: %s", path)
                if not self.dry_run:
                    try:
                        path.unlink()
                        result.files_removed.append(path)
                    except OSError as e:
                        result.errors.append(f"unlink {path}: {e}")
                else:
                    result.files_removed.append(path)

    def _is_protected(self, path: Path) -> bool:
        """Return True if the path should never be deleted."""
        rel = path.relative_to(self.repo_root)
        parts = set(rel.parts)
        if parts & self._PROTECTED_PATHS:
            return True
        if path.name in self._PROTECTED_PATHS:
            return True
        # Never touch .git internals
        if ".git" in str(rel):
            return True
        return False

    # ----------------------------------------------------------------
    # FULL SCOPE — system-level actions
    # ----------------------------------------------------------------

    def _flush_dns_cache(self, result: CleanResult) -> None:
        system = platform.system().lower()

        if system == "windows":
            cmd = ["ipconfig", "/flushdns"]
            description = "DNS cache flushed (ipconfig /flushdns)"
        elif system == "darwin":
            cmd = ["sudo", "dscacheutil", "-flushcache"]
            description = "DNS cache flushed (dscacheutil)"
        elif system == "linux":
            # Try systemd-resolved first, fall back to nscd
            if shutil.which("resolvectl"):
                cmd = ["resolvectl", "flush-caches"]
                description = "DNS cache flushed (resolvectl)"
            elif shutil.which("nscd"):
                cmd = ["nscd", "-i", "hosts"]
                description = "DNS cache flushed (nscd)"
            else:
                result.system_actions.append(
                    "DNS flush: no supported tool found (resolvectl / nscd)"
                )
                return
        else:
            result.system_actions.append(f"DNS flush: unsupported OS ({system})")
            return

        if self.dry_run:
            result.system_actions.append(f"[would run] {' '.join(cmd)}")
            return

        try:
            subprocess.run(cmd, capture_output=True, timeout=10, check=False)
            result.system_actions.append(description)
            logger.info(description)
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
            result.errors.append(f"DNS flush failed: {e}")

    def _clean_pip_cache(self, result: CleanResult) -> None:
        """Clear pip's HTTP cache to avoid leaving traces of downloaded packages."""
        if self.dry_run:
            result.system_actions.append("[would run] pip cache purge")
            return
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "cache", "purge"],
                capture_output=True,
                timeout=30,
                check=False,
            )
            result.system_actions.append("pip cache purged")
        except Exception as e:
            result.errors.append(f"pip cache purge failed: {e}")


# ----------------------------------------------------------------
# CLI ENTRY POINT
# ----------------------------------------------------------------

def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="trace_cleaner — Post-operation artifact cleanup for Ascended33",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Scopes:
  local  Clean repo artifacts only (output/, *.log, scan results, caches)
  full   Local + system DNS cache flush + pip cache purge

Examples:
  python3 scripts/opsec/trace_cleaner.py --scope local
  python3 scripts/opsec/trace_cleaner.py --scope full --dry-run
  python3 scripts/opsec/trace_cleaner.py --scope full --verbose
        """,
    )
    parser.add_argument(
        "--scope",
        choices=["local", "full"],
        default="local",
        help="Cleanup scope (default: local)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be deleted without deleting",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Log every file touched",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Override repo root directory (default: auto-detect)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    repo_root = (
        Path(args.repo_root) if args.repo_root
        else Path(__file__).parent.parent.parent
    )

    cleaner = TraceCleaner(
        repo_root=repo_root,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )

    scope = CleanScope.FULL if args.scope == "full" else CleanScope.LOCAL

    if args.dry_run:
        print(f"[trace_cleaner] DRY RUN — scope={scope.value}, repo={repo_root}")
    else:
        print(f"[trace_cleaner] Cleaning scope={scope.value}, repo={repo_root}")

    result = cleaner.clean(scope=scope)
    print(result.summary())

    return 1 if result.errors else 0


if __name__ == "__main__":
    sys.exit(main())
