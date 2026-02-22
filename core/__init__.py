"""
Ascended33 Core Package
OSINT Platform - Core modules for investigation management
"""

__version__ = "3.0.0"
__author__ = "Ascended33 Development Team"

from .obsidian_sync_engine import (
    ObsidianSyncEngine,
    ObsidianVault,
    IOCtoNotes,
    NotestoIOC,
    VaultWatcher,
    VaultMetadata
)

from .obsidian_ioc_linker import (
    ObsidianIOCLinker,
    ThreatActorLinker,
    CampaignLinker,
    InvestigationGraphBuilder
)

__all__ = [
    'ObsidianSyncEngine',
    'ObsidianVault',
    'IOCtoNotes',
    'NotestoIOC',
    'VaultWatcher',
    'VaultMetadata',
    'ObsidianIOCLinker',
    'ThreatActorLinker',
    'CampaignLinker',
    'InvestigationGraphBuilder',
]
