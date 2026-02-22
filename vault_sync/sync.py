"""
sync.py — Bidirectional sync pipeline between Ascended33 and Obsidian Vault.

Capabilities:
  1. PULL: Read templates and existing notes from Vault into local cache
  2. PUSH: Write generated reports/notes to correct Vault paths
  3. INDEX: Scan the Vault structure and build a local index of note paths
  4. LINK: Automatically update the Vault Index.md with new entries
  5. SEARCH: Find notes in the Vault by type, tag, or text

Usage:
    from vault_sync.sync import VaultSync

    sync = VaultSync()
    sync.pull_templates()
    sync.push_report("Security/OSINT/2026-02-19-target.md", content)
    index = sync.build_index()
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Default Vault folder structure (mirrors CLAUDE.md §5)
VAULT_FOLDERS = {
    "osint":        "Security/OSINT",
    "osint_active": "Security/OSINT/_Active",
    "osint_archive":"Security/OSINT/_Archive",
    "pentest":      "Security/Pentests/_Clients",
    "pentest_labs": "Security/Pentests/_Labs",
    "threat_intel": "Security/ThreatIntel",
    "darkweb":      "Security/ThreatIntel/DarkWeb",
    "cves":         "Security/ThreatIntel/CVEs",
    "ctf":          "Security/CTF",
    "tools":        "Security/Tools",
    "personal":     "Personal",
    "journal":      "Personal/Journal",
    "sessions":     "Claude-Michael/Sessions",
    "insights":     "Claude-Michael/Insights",
    "templates":    "Templates",
}


@dataclass
class NoteIndex:
    path: str
    title: str
    note_type: str
    tags: list[str]
    date: str
    target: str = ""
    status: str = ""


@dataclass
class SyncResult:
    pushed: list[str] = field(default_factory=list)
    pulled: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    indexed: int = 0

    @property
    def success(self) -> bool:
        return len(self.errors) == 0


class VaultSync:
    """Orchestrates all sync operations between Ascended33 and the Obsidian Vault."""

    def __init__(self):
        from vault_sync.vault_api import ObsidianVaultClient
        self.vault = ObsidianVaultClient.from_config()
        self._template_cache: dict[str, str] = {}

    # ── Connectivity ──────────────────────────────────────────────────────────

    def check_connection(self) -> bool:
        """Verify Vault is reachable."""
        if not self.vault.is_reachable():
            logger.error(
                "Vault is not reachable. Check:\n"
                "  1. Obsidian is running\n"
                "  2. Local REST API plugin is enabled\n"
                "  3. API key in config/config.yaml is correct"
            )
            return False
        logger.info("Vault connection OK")
        return True

    # ── Pull (Vault → local) ─────────────────────────────────────────────────

    def pull_templates(self) -> dict[str, str]:
        """Pull report templates from the Vault Templates/ folder."""
        template_names = [
            "osint_report.md",
            "pentest_report.md",
            "threat_intel_report.md",
            "ctf_writeup.md",
            "incident_note.md",
        ]
        for name in template_names:
            vault_path = f"{VAULT_FOLDERS['templates']}/{name}"
            content = self.vault.read_note(vault_path)
            if content:
                self._template_cache[name] = content
                logger.info("Pulled template: %s", name)
            else:
                logger.debug("Template not in Vault yet: %s", name)
        return self._template_cache

    def get_template(self, template_name: str) -> str | None:
        """
        Get a template — tries Vault first, falls back to local templates/ dir.
        """
        # Try cache
        if template_name in self._template_cache:
            return self._template_cache[template_name]

        # Try Vault
        content = self.vault.read_note(f"{VAULT_FOLDERS['templates']}/{template_name}")
        if content:
            self._template_cache[template_name] = content
            return content

        # Fall back to local templates/
        local_path = Path("templates") / template_name
        if local_path.exists():
            return local_path.read_text(encoding="utf-8")

        return None

    # ── Push (local → Vault) ─────────────────────────────────────────────────

    def push_report(
        self,
        note_type: str,
        content: str,
        filename: str | None = None,
        target: str = "",
        status: str = "active",
    ) -> str:
        """
        Push a report/note to the correct Vault folder.

        Returns: The vault path where the note was written.
        """
        folder = VAULT_FOLDERS.get(note_type, f"Security/{note_type.title()}")
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = (target or note_type).replace(" ", "-").replace(".", "-").lower()
        note_filename = filename or f"{date_str}-{slug}.md"
        vault_path = f"{folder}/{note_filename}"

        self.vault.create_note(vault_path, content)
        logger.info("Pushed to Vault: %s", vault_path)

        # Update the index
        self._update_index(vault_path, note_type, target)
        return vault_path

    def push_session_note(self, summary: str, insights: list[str]) -> str:
        """Push a Claude-Michael session note to Claude-Michael/Sessions/."""
        from vault_sync.note_builder import NoteBuilder
        content = NoteBuilder.session_note(summary, insights)
        date_str = datetime.now().strftime("%Y-%m-%d")
        vault_path = f"{VAULT_FOLDERS['sessions']}/{date_str}-session.md"
        self.vault.create_note(vault_path, content)
        logger.info("Session note pushed: %s", vault_path)
        return vault_path

    # ── Index management ──────────────────────────────────────────────────────

    def _update_index(self, note_path: str, note_type: str, target: str = "") -> None:
        """Add a new entry to the Vault's master Index.md."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        note_name = Path(note_path).stem
        entry = f"- {date_str} | [[{note_name}]] | {note_type} | {target or '—'}\n"
        self.vault.append_to_note("Index.md", entry)

    def build_index(self) -> list[NoteIndex]:
        """
        Build a local index of all security notes in the Vault.
        Parses YAML frontmatter to extract metadata.
        """
        index = []
        security_folders = [
            VAULT_FOLDERS["osint"],
            VAULT_FOLDERS["osint_active"],
            VAULT_FOLDERS["osint_archive"],
            VAULT_FOLDERS["pentest"],
            VAULT_FOLDERS["pentest_labs"],
            VAULT_FOLDERS["threat_intel"],
            VAULT_FOLDERS["darkweb"],
            VAULT_FOLDERS["ctf"],
        ]

        for folder in security_folders:
            # Try to list notes — only works in filesystem mode
            if self.vault.mode == "filesystem":
                folder_path = self.vault.vault_path / folder
                if folder_path.exists():
                    for note_file in folder_path.glob("*.md"):
                        entry = self._parse_note_metadata(
                            str(note_file.relative_to(self.vault.vault_path)),
                            note_file.read_text(encoding="utf-8"),
                        )
                        if entry:
                            index.append(entry)

        logger.info("Index built: %d notes", len(index))
        return index

    def _parse_note_metadata(self, path: str, content: str) -> NoteIndex | None:
        """Extract YAML frontmatter metadata from a note."""
        if not content.startswith("---"):
            return None
        try:
            end = content.index("---", 3)
            frontmatter = content[3:end]
            meta = {}
            for line in frontmatter.splitlines():
                if ": " in line:
                    key, _, value = line.partition(": ")
                    meta[key.strip()] = value.strip().strip('"')

            return NoteIndex(
                path=path,
                title=meta.get("title", Path(path).stem),
                note_type=meta.get("type", "unknown"),
                tags=re.findall(r"- (\w+)", meta.get("tags", "")),
                date=meta.get("date", ""),
                target=meta.get("target", ""),
                status=meta.get("status", ""),
            )
        except (ValueError, KeyError):
            return None

    # ── Search ────────────────────────────────────────────────────────────────

    def search_notes(self, query: str, note_type: str | None = None) -> list[NoteIndex]:
        """Search the local index for notes matching a query."""
        index = self.build_index()
        query_lower = query.lower()
        results = []
        for note in index:
            if note_type and note.note_type != note_type:
                continue
            if (query_lower in note.title.lower()
                    or query_lower in note.target.lower()
                    or any(query_lower in t for t in note.tags)):
                results.append(note)
        return results

    # ── Full sync ─────────────────────────────────────────────────────────────

    def full_sync(self) -> SyncResult:
        """Run a full pull → index cycle."""
        result = SyncResult()
        if not self.check_connection():
            result.errors.append("Vault unreachable")
            return result

        pulled = self.pull_templates()
        result.pulled = list(pulled.keys())
        index = self.build_index()
        result.indexed = len(index)
        logger.info("Full sync complete: %d templates pulled, %d notes indexed",
                    len(result.pulled), result.indexed)
        return result
