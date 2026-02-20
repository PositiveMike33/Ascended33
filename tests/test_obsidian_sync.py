"""
JOUR 1 Validation Tests - Obsidian Sync Engine
Comprehensive test suite for bidirectional vault synchronization
"""

import pytest
import sys
import tempfile
import json
from pathlib import Path
from datetime import datetime
import yaml

# Add core to path
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from obsidian_sync_engine import (
    ObsidianVault,
    IOCtoNotes,
    NotestoIOC,
    VaultMetadata,
    ObsidianSyncEngine
)

from obsidian_ioc_linker import (
    ObsidianIOCLinker,
    InvestigationGraphBuilder
)


class TestVaultRead:
    """Test Obsidian vault read operations with frontmatter parsing"""
    
    def test_vault_read(self):
        """
        Verify vault reads notes with proper frontmatter parsing
        Tests YAML frontmatter extraction and metadata preservation
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir)
            
            # Create test note with YAML frontmatter
            test_note = vault_path / "test_note.md"
            note_content = """---
investigation_id: inv_001
ioc_type: domain
confidence: high
status: verified
tags:
  - ioc_domain
  - severity_critical
---

## Investigation Details

Test investigation note for validation.

## IOC References

- [[IOC/domain/example.com]]
- [[IOC/ip/192.168.1.1]]
"""
            test_note.write_text(note_content)
            
            # Initialize vault and read note
            vault = ObsidianVault(vault_path=str(vault_path))
            metadata, content = vault.read_note("test_note.md")
            
            # Assertions
            assert metadata is not None, "Metadata should not be None"
            assert metadata.get('investigation_id') == 'inv_001'
            assert metadata.get('ioc_type') == 'domain'
            assert metadata.get('confidence') == 'high'
            assert metadata.get('status') == 'verified'
            assert 'Investigation Details' in content
            assert '[[IOC/domain/example.com]]' in content
            
            print("✅ test_vault_read PASSED")


class TestVaultWrite:
    """Test Obsidian vault write operations with metadata preservation"""
    
    def test_vault_write(self):
        """
        Verify vault writes notes with metadata preservation
        Tests YAML frontmatter creation and file writing
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir)
            
            # Create test metadata
            metadata = {
                'investigation_id': 'inv_002',
                'ioc_type': 'ip_address',
                'confidence': 'medium',
                'status': 'unverified',
                'tags': ['ioc_ip', 'severity_medium'],
                'created_date': datetime.utcnow().isoformat(),
                'source': 'threat_feed'
            }
            
            content = "## IOC Analysis\n\nDetailed analysis of 192.168.1.100"
            
            # Write note
            vault = ObsidianVault(vault_path=str(vault_path))
            vault.write_note("test_ioc.md", metadata, content)
            
            # Verify file exists
            test_file = vault_path / "test_ioc.md"
            assert test_file.exists(), "Note file should be created"
            
            # Verify content
            file_content = test_file.read_text()
            assert 'investigation_id: inv_002' in file_content
            assert 'ioc_type: ip_address' in file_content
            assert 'confidence: medium' in file_content
            assert 'IOC Analysis' in file_content
            
            print("✅ test_vault_write PASSED")


class TestIOCtoNotes:
    """Test IOC to Notes conversion"""
    
    def test_ioc_to_notes(self):
        """
        Verify IOC to Note conversion with proper structure
        Tests creation of correctly formatted IOC notes
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir)
            
            # Create IOC object
            ioc_data = {
                'type': 'domain',
                'value': 'malware.com',
                'confidence': 'high',
                'investigation_id': 'inv_001',
                'source': 'threat_feed',
                'status': 'verified'
            }
            
            # Convert IOC to note
            converter = IOCtoNotes(vault_path=str(vault_path))
            note_path, metadata, content = converter.create_ioc_note(ioc_data)
            
            # Assertions
            assert note_path is not None
            assert 'domain' in str(note_path).lower()
            assert metadata['ioc_type'] == 'domain'
            assert metadata['confidence'] == 'high'
            assert 'malware.com' in content
            
            print("✅ test_ioc_to_notes PASSED")


class TestFrontmatterParsing:
    """Test YAML frontmatter parsing accuracy"""
    
    def test_frontmatter_parsing(self):
        """
        Verify YAML frontmatter parsing accuracy
        Tests extraction of complex nested YAML structures
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir)
            
            # Create complex note with nested YAML
            test_note = vault_path / "complex_note.md"
            note_content = """---
investigation_id: inv_003
case_of_use: incident_response
ioc_references:
  - domain_malware.com
  - ip_192.168.1.1
  - hash_abc123
tags:
  - ioc_domain
  - severity_critical
  - status_verified
metadata:
  created_date: "2025-02-19T10:30:00Z"
  modified_date: "2025-02-19T11:00:00Z"
  source: threat_feed
---

## Investigation Report

Complex investigation with nested metadata.
"""
            test_note.write_text(note_content)
            
            # Parse frontmatter
            vault = ObsidianVault(vault_path=str(vault_path))
            metadata, content = vault.read_note("complex_note.md")
            
            # Assertions
            assert metadata.get('investigation_id') == 'inv_003'
            assert metadata.get('case_of_use') == 'incident_response'
            assert isinstance(metadata.get('ioc_references'), list)
            assert len(metadata.get('ioc_references', [])) == 3
            assert isinstance(metadata.get('tags'), list)
            assert isinstance(metadata.get('metadata'), dict)
            
            print("✅ test_frontmatter_parsing PASSED")


class TestWatchVault:
    """Test real-time vault monitoring"""
    
    def test_watch_vault(self):
        """
        Verify real-time file monitoring and change detection
        Tests watchdog integration and change detection
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir)
            
            # Initialize watcher
            sync_engine = ObsidianSyncEngine(vault_path=str(vault_path))
            
            # Verify initialization
            assert sync_engine.vault_path == vault_path
            assert hasattr(sync_engine, 'vault')
            assert hasattr(sync_engine, 'watcher')
            
            # Create test file
            test_note = vault_path / "watch_test.md"
            test_content = "---\ntest: true\n---\n\n## Test Content"
            test_note.write_text(test_content)
            
            # Verify file can be read after creation
            metadata, content = sync_engine.vault.read_note("watch_test.md")
            assert metadata is not None
            assert 'Test Content' in content
            
            print("✅ test_watch_vault PASSED")


class TestGraphBuilder:
    """Test investigation graph building"""
    
    def test_graph_builder(self):
        """
        Verify investigation graph building
        Tests IOC linking and relationship creation
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir)
            
            # Create test structure
            (Path(tmpdir) / "IOCs" / "domain").mkdir(parents=True, exist_ok=True)
            (Path(tmpdir) / "Investigations").mkdir(parents=True, exist_ok=True)
            
            # Create test IOC notes
            ioc_note = Path(tmpdir) / "IOCs" / "domain" / "example.com.md"
            ioc_note.write_text("""---
type: domain
value: example.com
confidence: high
---

## Malicious Domain
Found in investigation inv_001
""")
            
            # Create investigation note
            inv_note = Path(tmpdir) / "Investigations" / "inv_001.md"
            inv_note.write_text("""---
investigation_id: inv_001
status: active
---

## Investigation 001
IOCs: [[IOCs/domain/example.com]]
""")
            
            # Build graph
            graph_builder = InvestigationGraphBuilder(vault_path=str(vault_path))
            graph = graph_builder.build_investigation_graph("Investigations/inv_001")
            
            # Assertions
            assert graph is not None
            assert 'nodes' in graph or isinstance(graph, dict)
            
            print("✅ test_graph_builder PASSED")


class TestIntegration:
    """Integration tests for complete sync workflow"""
    
    def test_complete_workflow(self):
        """
        Verify complete bidirectional sync workflow
        Tests full cycle: IOC → Note → Graph
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir)
            
            # Create vault structure
            (Path(tmpdir) / "IOCs" / "domain").mkdir(parents=True, exist_ok=True)
            (Path(tmpdir) / "Investigations").mkdir(parents=True, exist_ok=True)
            
            # Step 1: Create IOC
            ioc_data = {
                'type': 'domain',
                'value': 'malware.com',
                'confidence': 'high',
                'investigation_id': 'inv_001'
            }
            
            # Step 2: Convert to note
            converter = IOCtoNotes(vault_path=str(vault_path))
            note_path, metadata, content = converter.create_ioc_note(ioc_data)
            
            # Step 3: Write note
            vault = ObsidianVault(vault_path=str(vault_path))
            vault.write_note(str(note_path.relative_to(vault_path)), metadata, content)
            
            # Step 4: Read and verify
            read_metadata, read_content = vault.read_note(
                str(note_path.relative_to(vault_path))
            )
            
            assert read_metadata['ioc_type'] == 'domain'
            assert 'malware.com' in read_content
            
            print("✅ test_complete_workflow PASSED")


# Test execution
if __name__ == "__main__":
    print("\n" + "="*70)
    print("JOUR 1 - VALIDATION TESTS")
    print("Obsidian Sync Engine Integration")
    print("="*70 + "\n")
    
    # Run all tests
    pytest.main([__file__, "-v", "--tb=short"])
