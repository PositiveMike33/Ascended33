"""
note_builder.py — Build structured Obsidian notes with YAML frontmatter.

Obsidian notes in Ascended33 use:
  - YAML frontmatter for metadata (date, tags, type, status)
  - Dataview-compatible fields
  - Wikilinks [[note-name]] for cross-references
  - Standard tag taxonomy

Usage:
    from vault_sync.note_builder import NoteBuilder

    note = NoteBuilder.from_template("osint")
    note.set_title("Domain Recon — example.com")
    note.set_tags(["osint", "domain", "2026"])
    note.set_body("## Findings\n...")
    content = note.build()
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class NoteMetadata:
    title: str = ""
    date: str = ""
    type: str = ""              # osint | pentest | threat_intel | ctf | personal | journal
    status: str = "active"      # active | archived | flagged
    target: str = ""
    tags: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)   # wikilinks to related notes
    severity: str = ""          # Critical | High | Medium | Low | Informational
    author: str = "Michael Gauthier Guillet"
    generated_by: str = "Ascended33"
    custom: dict[str, Any] = field(default_factory=dict)


class NoteBuilder:
    """Constructs Obsidian-compatible Markdown notes with YAML frontmatter."""

    def __init__(self):
        self.metadata = NoteMetadata()
        self._body_sections: list[str] = []
        self._backlinks: list[str] = []

    # ── Metadata setters ─────────────────────────────────────────────────────

    def set_title(self, title: str) -> "NoteBuilder":
        self.metadata.title = title
        return self

    def set_type(self, note_type: str) -> "NoteBuilder":
        self.metadata.type = note_type
        return self

    def set_tags(self, tags: list[str]) -> "NoteBuilder":
        self.metadata.tags = tags
        return self

    def add_tag(self, tag: str) -> "NoteBuilder":
        if tag not in self.metadata.tags:
            self.metadata.tags.append(tag)
        return self

    def set_target(self, target: str) -> "NoteBuilder":
        self.metadata.target = target
        return self

    def set_severity(self, severity: str) -> "NoteBuilder":
        self.metadata.severity = severity
        return self

    def set_status(self, status: str) -> "NoteBuilder":
        self.metadata.status = status
        return self

    def add_related(self, note_name: str) -> "NoteBuilder":
        """Add a related note wikilink."""
        self.metadata.related.append(note_name)
        return self

    def set_custom(self, key: str, value: Any) -> "NoteBuilder":
        self.metadata.custom[key] = value
        return self

    # ── Body building ─────────────────────────────────────────────────────────

    def add_section(self, heading: str, content: str, level: int = 2) -> "NoteBuilder":
        prefix = "#" * level
        self._body_sections.append(f"{prefix} {heading}\n\n{content}")
        return self

    def set_body(self, body: str) -> "NoteBuilder":
        """Set the full body directly (replaces all sections)."""
        self._body_sections = [body]
        return self

    def add_backlink(self, note_name: str) -> "NoteBuilder":
        self._backlinks.append(note_name)
        return self

    def add_callout(self, callout_type: str, title: str, content: str) -> "NoteBuilder":
        """
        Add an Obsidian callout block.
        Types: note, tip, warning, danger, info, success, question
        """
        block = f"> [!{callout_type}] {title}\n"
        for line in content.splitlines():
            block += f"> {line}\n"
        self._body_sections.append(block)
        return self

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build_frontmatter(self) -> str:
        m = self.metadata
        now = datetime.now()
        date_str = m.date or now.strftime("%Y-%m-%d")

        lines = ["---"]
        lines.append(f"title: \"{m.title}\"")
        lines.append(f"date: {date_str}")
        lines.append(f"type: {m.type}")
        lines.append(f"status: {m.status}")
        lines.append(f"author: {m.author}")
        lines.append(f"generated_by: {m.generated_by}")

        if m.target:
            lines.append(f"target: \"{m.target}\"")

        if m.severity:
            lines.append(f"severity: {m.severity}")

        if m.tags:
            lines.append("tags:")
            for tag in m.tags:
                lines.append(f"  - {tag}")

        if m.aliases:
            lines.append("aliases:")
            for alias in m.aliases:
                lines.append(f"  - \"{alias}\"")

        if m.related:
            lines.append("related:")
            for rel in m.related:
                lines.append(f"  - \"[[{rel}]]\"")

        for key, value in m.custom.items():
            if isinstance(value, str):
                lines.append(f"{key}: \"{value}\"")
            else:
                lines.append(f"{key}: {value}")

        lines.append("---")
        return "\n".join(lines)

    def build(self) -> str:
        """Build the complete note content."""
        parts = [self._build_frontmatter()]

        if self.metadata.title:
            parts.append(f"\n# {self.metadata.title}\n")

        if self._body_sections:
            parts.append("\n".join(self._body_sections))

        if self._backlinks:
            backlink_list = " | ".join(f"[[{b}]]" for b in self._backlinks)
            parts.append(f"\n---\n**Related**: {backlink_list}")

        return "\n\n".join(parts) + "\n"

    @classmethod
    def security_note(
        cls,
        title: str,
        target: str,
        note_type: str,
        body: str,
        tags: list[str] | None = None,
        severity: str = "",
    ) -> str:
        """Convenience factory for security research notes."""
        builder = cls()
        builder.set_title(title)
        builder.set_type(note_type)
        builder.set_target(target)
        builder.set_body(body)
        builder.set_tags(tags or [note_type])
        if severity:
            builder.set_severity(severity)
        return builder.build()

    @classmethod
    def session_note(cls, session_summary: str, key_insights: list[str]) -> str:
        """Build a Claude-Michael collaborative session note."""
        builder = cls()
        builder.set_title(f"Session — {datetime.now().strftime('%Y-%m-%d')}")
        builder.set_type("session")
        builder.add_tag("claude")
        builder.add_tag("session")
        builder.add_section("Session Summary", session_summary)
        if key_insights:
            insight_list = "\n".join(f"- {i}" for i in key_insights)
            builder.add_section("Key Insights", insight_list)
        builder.add_callout("info", "Collaborative Note", "Generated from Claude + Michael working session.")
        return builder.build()
