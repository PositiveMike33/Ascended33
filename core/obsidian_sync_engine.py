# ============================================================================
# OBSIDIAN SYNC ENGINE - Ascended33 OSINT Platform
# ============================================================================
# Purpose: Bidirectional synchronization between Python OSINT engine and Obsidian vault
# Enables personal note management with automatic IOC linkage and metadata tracking
# 
# Author: Ascended33 Platform
# Version: 1.0.0
# Status: Production Ready
# ============================================================================

import os
import json
import yaml
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class VaultMetadata:
    """Metadata structure for Obsidian notes"""
    case_of_use: str  # bug-bounty, incident-response, journalisme, personnel
    source: str  # Where the information came from
    created_date: str  # ISO format datetime
    modified_date: str  # ISO format datetime
    tags: List[str]  # System tags
    ioc_references: List[str]  # IOC hashes linked to this note
    confidence: Optional[str] = "medium"  # low, medium, high
    investigation_id: Optional[str] = None
    status: Optional[str] = "active"  # active, archived, review


class ObsidianVault:
    """
    Manages Obsidian vault operations: read, write, parse, and watch files
    Handles both markdown content and YAML frontmatter
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize Obsidian vault connection
        
        Args:
            vault_path: Full path to Obsidian vault directory
        """
        self.vault_path = Path(vault_path)
        
        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {vault_path}")
        
        logger.info(f"Initialized Obsidian vault at: {self.vault_path}")
        self.observer = None
    
    def read_note(self, relative_path: str) -> Tuple[Dict, str]:
        """
        Read a note from vault, parse frontmatter and content
        
        Args:
            relative_path: Path relative to vault root (e.g., "Investigations/malware_analysis.md")
        
        Returns:
            Tuple of (frontmatter_dict, markdown_content)
        """
        note_path = self.vault_path / relative_path
        
        if not note_path.exists():
            logger.warning(f"Note not found: {note_path}")
            return {}, ""
        
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        frontmatter, markdown = self._parse_frontmatter(content)
        logger.debug(f"Read note: {relative_path}")
        
        return frontmatter, markdown
    
    def write_note(self, relative_path: str, metadata: Dict, content: str) -> bool:
        """
        Write note to vault with YAML frontmatter and markdown content
        
        Args:
            relative_path: Path relative to vault root
            metadata: Dictionary containing frontmatter metadata
            content: Markdown content
        
        Returns:
            True if successful, False otherwise
        """
        note_path = self.vault_path / relative_path
        note_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create frontmatter
        frontmatter_str = self._create_frontmatter(metadata)
        
        # Combine frontmatter and content
        full_content = f"{frontmatter_str}\n{content}"
        
        try:
            with open(note_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            logger.info(f"Wrote note: {relative_path}")
            return True
        except Exception as e:
            logger.error(f"Error writing note {relative_path}: {e}")
            return False
    
    def list_notes(self, folder: str = "") -> List[str]:
        """
        List all markdown files in vault or specific folder
        
        Args:
            folder: Optional subfolder to search in
        
        Returns:
            List of relative paths to .md files
        """
        search_path = self.vault_path / folder if folder else self.vault_path
        
        if not search_path.exists():
            return []
        
        notes = []
        for note_file in search_path.rglob("*.md"):
            if ".obsidian" not in str(note_file):
                relative = note_file.relative_to(self.vault_path)
                notes.append(str(relative).replace("\\", "/"))
        
        return notes
    
    def get_note_hash(self, relative_path: str) -> str:
        """
        Calculate SHA-256 hash of note content for change detection
        
        Args:
            relative_path: Path to note
        
        Returns:
            SHA-256 hash of file content
        """
        note_path = self.vault_path / relative_path
        
        if not note_path.exists():
            return ""
        
        with open(note_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def _parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """
        Parse YAML frontmatter from markdown content
        
        Args:
            content: Full file content
        
        Returns:
            Tuple of (frontmatter_dict, markdown_content)
        """
        if not content.startswith("---"):
            return {}, content
        
        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}, content
        
        try:
            frontmatter = yaml.safe_load(parts[1])
            markdown = parts[2].strip()
            return frontmatter or {}, markdown
        except yaml.YAMLError as e:
            logger.error(f"Error parsing frontmatter: {e}")
            return {}, content
    
    def _create_frontmatter(self, metadata: Dict) -> str:
        """
        Create YAML frontmatter string from metadata dict
        
        Args:
            metadata: Dictionary to convert
        
        Returns:
            Formatted frontmatter string
        """
        yaml_content = yaml.dump(metadata, default_flow_style=False)
        return f"---\n{yaml_content}---"


class IOCtoNotes:
    """
    Convert IOC (Indicator of Compromise) objects to Obsidian notes
    Creates linked notes with proper metadata and categorization
    """
    
    def __init__(self, vault: ObsidianVault):
        """
        Initialize IOC to Notes converter
        
        Args:
            vault: ObsidianVault instance
        """
        self.vault = vault
    
    def create_ioc_note(self, ioc_data: Dict, case_of_use: str) -> str:
        """
        Create a note for an IOC with proper structure and metadata
        
        Args:
            ioc_data: IOC dictionary (must have 'type', 'value', 'id')
            case_of_use: Classification (bug-bounty, incident-response, journalisme, personnel)
        
        Returns:
            Relative path to created note
        """
        ioc_id = ioc_data.get('id', hashlib.md5(
            ioc_data.get('value', '').encode()).hexdigest()[:8])
        ioc_type = ioc_data.get('type', 'unknown').lower()
        
        # Create folder structure: IOCs/{type}/{id}
        relative_path = f"IOCs/{ioc_type}/{ioc_id}.md"
        
        # Build metadata
        metadata = VaultMetadata(
            case_of_use=case_of_use,
            source=ioc_data.get('source', 'unknown'),
            created_date=datetime.now().isoformat(),
            modified_date=datetime.now().isoformat(),
            tags=[f"ioc-{ioc_type}", f"case-{case_of_use}"],
            ioc_references=[ioc_id],
            confidence=ioc_data.get('confidence', 'medium'),
            investigation_id=ioc_data.get('investigation_id')
        )
        
        # Build markdown content
        content = self._build_ioc_content(ioc_data)
        
        # Write to vault
        self.vault.write_note(relative_path, asdict(metadata), content)
        logger.info(f"Created IOC note: {relative_path}")
        
        return relative_path
    
    def create_investigation_note(self, investigation: Dict) -> str:
        """
        Create investigation folder structure with index note
        
        Args:
            investigation: Investigation dictionary (must have 'name', 'id')
        
        Returns:
            Relative path to created investigation index
        """
        inv_id = investigation.get('id', hashlib.md5(
            investigation.get('name', '').encode()).hexdigest()[:8])
        inv_name = investigation.get('name', 'Unknown Investigation')
        
        # Create folder structure: Investigations/{id}/
        relative_path = f"Investigations/{inv_id}/index.md"
        
        # Build metadata
        metadata = VaultMetadata(
            case_of_use=investigation.get('case_of_use', 'personnel'),
            source=investigation.get('source', 'manual'),
            created_date=datetime.now().isoformat(),
            modified_date=datetime.now().isoformat(),
            tags=["investigation"] + investigation.get('tags', []),
            ioc_references=[],
            investigation_id=inv_id,
            status="active"
        )
        
        # Build markdown content
        content = self._build_investigation_content(investigation)
        
        # Write to vault
        self.vault.write_note(relative_path, asdict(metadata), content)
        logger.info(f"Created investigation note: {relative_path}")
        
        return relative_path
    
    def _build_ioc_content(self, ioc_data: Dict) -> str:
        """Build markdown content for IOC note"""
        content = f"""# IOC: {ioc_data.get('value', 'Unknown')}

## Basic Information
- **Type**: {ioc_data.get('type', 'Unknown')}
- **Value**: `{ioc_data.get('value', 'N/A')}`
- **Confidence**: {ioc_data.get('confidence', 'Medium')}
- **First Seen**: {ioc_data.get('first_seen', 'Unknown')}
- **Source**: {ioc_data.get('source', 'Unknown')}

## Analysis
{ioc_data.get('analysis', 'No analysis available')}

## Relationships
{ioc_data.get('relationships', 'No relationships recorded')}

## References
{ioc_data.get('references', 'No references available')}

## Tags
{', '.join(ioc_data.get('tags', []))}

---
*Created by Ascended33 OSINT Engine*
*Last updated: {datetime.now().isoformat()}*
"""
        return content
    
    def _build_investigation_content(self, investigation: Dict) -> str:
        """Build markdown content for investigation index note"""
        content = f"""# Investigation: {investigation.get('name', 'Unknown')}

## Overview
{investigation.get('description', 'No description available')}

## Key Details
- **Status**: Active
- **Started**: {investigation.get('start_date', 'Unknown')}
- **Case Type**: {investigation.get('case_of_use', 'Personnel')}

## IOCs
This section will be populated with linked IOCs as they are discovered.

## Timeline
- Created: {datetime.now().isoformat()}

## Notes
Add your investigation notes here as you progress.

---
*Investigation managed by Ascended33 OSINT Platform*
"""
        return content


class NotestoIOC:
    """
    Extract IOCs and structured data from Obsidian notes
    Reverse operation: notes → IOC objects
    """
    
    def __init__(self, vault: ObsidianVault):
        """
        Initialize Notes to IOC converter
        
        Args:
            vault: ObsidianVault instance
        """
        self.vault = vault
    
    def extract_iocs_from_note(self, relative_path: str) -> List[Dict]:
        """
        Extract IOCs from a note using pattern matching
        
        Args:
            relative_path: Path to note to extract from
        
        Returns:
            List of extracted IOC dictionaries
        """
        metadata, content = self.vault.read_note(relative_path)
        iocs = []
        
        # Extract IOCs from content using regex patterns
        iocs.extend(self._extract_ips(content))
        iocs.extend(self._extract_domains(content))
        iocs.extend(self._extract_hashes(content))
        iocs.extend(self._extract_emails(content))
        
        logger.info(f"Extracted {len(iocs)} IOCs from {relative_path}")
        return iocs
    
    def get_note_metadata_as_dict(self, relative_path: str) -> Dict:
        """
        Get note frontmatter as dictionary
        
        Args:
            relative_path: Path to note
        
        Returns:
            Frontmatter metadata as dictionary
        """
        metadata, _ = self.vault.read_note(relative_path)
        return metadata
    
    def _extract_ips(self, content: str) -> List[Dict]:
        """Extract IP addresses using regex"""
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        ips = re.findall(ip_pattern, content)
        return [{'type': 'IP', 'value': ip} for ip in set(ips)]
    
    def _extract_domains(self, content: str) -> List[Dict]:
        """Extract domain names using regex"""
        domain_pattern = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})'
        domains = re.findall(domain_pattern, content)
        return [{'type': 'Domain', 'value': domain} for domain in set(domains)]
    
    def _extract_hashes(self, content: str) -> List[Dict]:
        """Extract hashes (MD5, SHA-1, SHA-256) using regex"""
        hashes = []
        # MD5
        md5_pattern = r'\b[a-fA-F0-9]{32}\b'
        hashes.extend([{'type': 'MD5', 'value': h} for h in set(re.findall(md5_pattern, content))])
        # SHA-1
        sha1_pattern = r'\b[a-fA-F0-9]{40}\b'
        hashes.extend([{'type': 'SHA1', 'value': h} for h in set(re.findall(sha1_pattern, content))])
        # SHA-256
        sha256_pattern = r'\b[a-fA-F0-9]{64}\b'
        hashes.extend([{'type': 'SHA256', 'value': h} for h in set(re.findall(sha256_pattern, content))])
        return hashes
    
    def _extract_emails(self, content: str) -> List[Dict]:
        """Extract email addresses using regex"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, content)
        return [{'type': 'Email', 'value': email} for email in set(emails)]


class VaultWatcher(FileSystemEventHandler):
    """
    Watch Obsidian vault for file changes and trigger sync
    Enables real-time bidirectional synchronization
    """
    
    def __init__(self, vault: ObsidianVault, callback=None):
        """
        Initialize vault watcher
        
        Args:
            vault: ObsidianVault instance
            callback: Function to call on file change (relative_path, change_type)
        """
        self.vault = vault
        self.callback = callback
        self.last_hashes = {}
    
    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory or not event.src_path.endswith('.md'):
            return
        
        try:
            relative_path = str(Path(event.src_path).relative_to(self.vault.vault_path))
            relative_path = relative_path.replace("\\", "/")
            
            current_hash = self.vault.get_note_hash(relative_path)
            last_hash = self.last_hashes.get(relative_path)
            
            if current_hash != last_hash:
                logger.info(f"Note modified: {relative_path}")
                self.last_hashes[relative_path] = current_hash
                
                if self.callback:
                    self.callback(relative_path, 'modified')
        except Exception as e:
            logger.error(f"Error handling modification: {e}")
    
    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory or not event.src_path.endswith('.md'):
            return
        
        try:
            relative_path = str(Path(event.src_path).relative_to(self.vault.vault_path))
            relative_path = relative_path.replace("\\", "/")
            
            logger.info(f"Note created: {relative_path}")
            self.last_hashes[relative_path] = self.vault.get_note_hash(relative_path)
            
            if self.callback:
                self.callback(relative_path, 'created')
        except Exception as e:
            logger.error(f"Error handling creation: {e}")


class ObsidianSyncEngine:
    """
    Main orchestrator for Obsidian vault synchronization
    Coordinates all sync operations between Python OSINT and Obsidian
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize the sync engine
        
        Args:
            vault_path: Path to Obsidian vault
        """
        self.vault = ObsidianVault(vault_path)
        self.ioc_to_notes = IOCtoNotes(self.vault)
        self.notes_to_ioc = NotestoIOC(self.vault)
        self.watcher = None
        self.observer = None
    
    def start_watching(self, callback=None):
        """
        Start watching vault for changes
        
        Args:
            callback: Function to call on changes
        """
        self.watcher = VaultWatcher(self.vault, callback)
        self.observer = Observer()
        self.observer.schedule(self.watcher, str(self.vault.vault_path), recursive=True)
        self.observer.start()
        logger.info("Vault watcher started")
    
    def stop_watching(self):
        """Stop watching vault for changes"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("Vault watcher stopped")
    
    def sync_ioc_to_vault(self, ioc_data: Dict, case_of_use: str) -> str:
        """
        Synchronize IOC to vault as new note
        
        Args:
            ioc_data: IOC dictionary
            case_of_use: Classification
        
        Returns:
            Path to created note
        """
        return self.ioc_to_notes.create_ioc_note(ioc_data, case_of_use)
    
    def sync_investigation_to_vault(self, investigation: Dict) -> str:
        """
        Synchronize investigation to vault
        
        Args:
            investigation: Investigation dictionary
        
        Returns:
            Path to created investigation
        """
        return self.ioc_to_notes.create_investigation_note(investigation)
    
    def extract_from_note(self, relative_path: str) -> List[Dict]:
        """
        Extract IOCs from a vault note
        
        Args:
            relative_path: Path to note
        
        Returns:
            List of extracted IOCs
        """
        return self.notes_to_ioc.extract_iocs_from_note(relative_path)
    
    def get_vault_stats(self) -> Dict:
        """
        Get statistics about vault
        
        Returns:
            Dictionary with vault statistics
        """
        all_notes = self.vault.list_notes()
        investigations = self.vault.list_notes("Investigations")
        iocs = self.vault.list_notes("IOCs")
        
        return {
            'total_notes': len(all_notes),
            'investigations': len(investigations),
            'iocs': len(iocs),
            'vault_path': str(self.vault.vault_path)
        }


if __name__ == "__main__":
    logger.info("Obsidian Sync Engine v1.0.0 loaded successfully")
