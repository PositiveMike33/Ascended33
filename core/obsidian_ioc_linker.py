# ============================================================================
# OBSIDIAN IOC LINKER - Link IOCs to Obsidian Notes
# ============================================================================
# Purpose: Create and maintain relationships between IOCs and investigation notes
# Enables graph-based analysis within Obsidian vault
#
# Author: Ascended33 Platform
# Version: 1.0.0
# Status: Production Ready
# ============================================================================

import json
import logging
from typing import Dict, List, Set, Tuple
from pathlib import Path
from dataclasses import dataclass
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class IOCLink:
    """Represents a link between IOC and notes"""
    ioc_id: str
    ioc_value: str
    ioc_type: str
    note_path: str
    relationship_type: str  # "mentioned_in", "discovered_in", "related_to"
    confidence: str  # low, medium, high
    created_date: str


class ObsidianIOCLinker:
    """
    Create and maintain IOC relationships within Obsidian vault
    Generates backlinks and graph connections
    """
    
    def __init__(self, vault_path: str):
        """Initialize IOC linker"""
        self.vault_path = Path(vault_path)
        self.ioc_links: Dict[str, List[IOCLink]] = {}
    
    def create_backlink(self, ioc_id: str, note_path: str) -> str:
        """
        Create backlink from IOC note to investigation note
        Returns markdown backlink syntax for Obsidian
        
        Args:
            ioc_id: IOC identifier
            note_path: Relative path to investigation note
        
        Returns:
            Markdown backlink string
        """
        # Convert path to Obsidian link format
        link_path = note_path.replace(".md", "").replace("\\", "/")
        backlink = f"[[{link_path}]]"
        logger.info(f"Created backlink: {ioc_id} -> {backlink}")
        return backlink
    
    def create_graph_connection(self, source_ioc: Dict, target_ioc: Dict, 
                               relationship: str) -> Dict:
        """
        Create graph connection between two IOCs
        
        Args:
            source_ioc: Source IOC dictionary
            target_ioc: Target IOC dictionary
            relationship: Type of relationship
        
        Returns:
            Connection dictionary for graph
        """
        connection = {
            'source': source_ioc['id'],
            'target': target_ioc['id'],
            'relationship': relationship,
            'source_type': source_ioc['type'],
            'target_type': target_ioc['type'],
            'bidirectional': True
        }
        logger.info(f"Created connection: {source_ioc['id']} --[{relationship}]--> {target_ioc['id']}")
        return connection
    
    def generate_graph_json(self, links: List[IOCLink]) -> Dict:
        """
        Generate JSON for Obsidian graph visualization
        
        Args:
            links: List of IOC links
        
        Returns:
            Graph JSON structure
        """
        nodes = []
        edges = []
        node_ids = set()
        
        for link in links:
            # Add nodes if not exists
            if link.ioc_id not in node_ids:
                nodes.append({
                    'id': link.ioc_id,
                    'label': link.ioc_value,
                    'type': link.ioc_type,
                    'confidence': link.confidence
                })
                node_ids.add(link.ioc_id)
            
            # Add edge
            edges.append({
                'source': link.ioc_id,
                'target': link.note_path,
                'relationship': link.relationship_type
            })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'directed': True
        }


class ThreatActorLinker:
    """
    Link IOCs to threat actor profiles
    Create threat actor relationship graphs
    """
    
    def __init__(self, vault_path: str):
        """Initialize threat actor linker"""
        self.vault_path = Path(vault_path)
        self.actor_iocs: Dict[str, List[str]] = {}  # actor_id -> [ioc_ids]
    
    def link_ioc_to_actor(self, ioc_id: str, actor_id: str) -> bool:
        """
        Link IOC to threat actor
        
        Args:
            ioc_id: IOC identifier
            actor_id: Threat actor identifier
        
        Returns:
            True if successful
        """
        if actor_id not in self.actor_iocs:
            self.actor_iocs[actor_id] = []
        
        if ioc_id not in self.actor_iocs[actor_id]:
            self.actor_iocs[actor_id].append(ioc_id)
            logger.info(f"Linked IOC {ioc_id} to actor {actor_id}")
            return True
        return False
    
    def get_actor_iocs(self, actor_id: str) -> List[str]:
        """Get all IOCs linked to actor"""
        return self.actor_iocs.get(actor_id, [])
    
    def create_actor_profile_link(self, actor_id: str, profile_note_path: str) -> Dict:
        """
        Create link between threat actor and profile note
        
        Args:
            actor_id: Threat actor identifier
            profile_note_path: Path to actor profile note
        
        Returns:
            Link structure
        """
        ioc_list = self.get_actor_iocs(actor_id)
        
        return {
            'actor_id': actor_id,
            'profile_note': profile_note_path,
            'linked_iocs': ioc_list,
            'ioc_count': len(ioc_list)
        }


class CampaignLinker:
    """
    Link IOCs to campaigns
    Create campaign timeline and relationships
    """
    
    def __init__(self, vault_path: str):
        """Initialize campaign linker"""
        self.vault_path = Path(vault_path)
        self.campaign_iocs: Dict[str, Dict] = {}  # campaign_id -> {iocs, timeline}
    
    def create_campaign(self, campaign_id: str, campaign_name: str, 
                       start_date: str, end_date: str = None) -> bool:
        """
        Create new campaign with structure
        
        Args:
            campaign_id: Campaign identifier
            campaign_name: Human-readable campaign name
            start_date: Campaign start date (ISO format)
            end_date: Campaign end date (optional, ISO format)
        
        Returns:
            True if successful
        """
        if campaign_id in self.campaign_iocs:
            logger.warning(f"Campaign {campaign_id} already exists")
            return False
        
        self.campaign_iocs[campaign_id] = {
            'name': campaign_name,
            'start_date': start_date,
            'end_date': end_date,
            'iocs': [],
            'actors': [],
            'timeline': []
        }
        logger.info(f"Created campaign: {campaign_name}")
        return True
    
    def add_ioc_to_campaign(self, campaign_id: str, ioc_id: str, 
                           ioc_data: Dict) -> bool:
        """
        Add IOC to campaign
        
        Args:
            campaign_id: Campaign identifier
            ioc_id: IOC identifier
            ioc_data: IOC data dictionary
        
        Returns:
            True if successful
        """
        if campaign_id not in self.campaign_iocs:
            logger.warning(f"Campaign {campaign_id} not found")
            return False
        
        if ioc_id not in self.campaign_iocs[campaign_id]['iocs']:
            self.campaign_iocs[campaign_id]['iocs'].append(ioc_id)
            
            # Add to timeline
            timeline_entry = {
                'ioc_id': ioc_id,
                'ioc_value': ioc_data.get('value', 'unknown'),
                'ioc_type': ioc_data.get('type', 'unknown'),
                'date': ioc_data.get('first_seen', 'unknown'),
                'event': f"IOC discovered: {ioc_data.get('value', 'unknown')}"
            }
            self.campaign_iocs[campaign_id]['timeline'].append(timeline_entry)
            logger.info(f"Added IOC {ioc_id} to campaign {campaign_id}")
            return True
        return False
    
    def get_campaign_timeline(self, campaign_id: str) -> List[Dict]:
        """Get sorted campaign timeline"""
        if campaign_id not in self.campaign_iocs:
            return []
        
        timeline = self.campaign_iocs[campaign_id]['timeline']
        # Sort by date (simple string sort for ISO format)
        return sorted(timeline, key=lambda x: x['date'])


class InvestigationGraphBuilder:
    """
    Build complete investigation graphs
    Connect investigations, IOCs, actors, and campaigns
    """
    
    def __init__(self, vault_path: str):
        """Initialize graph builder"""
        self.vault_path = Path(vault_path)
        self.graph = {
            'investigations': {},
            'iocs': {},
            'actors': {},
            'campaigns': {},
            'relationships': []
        }
    
    def add_investigation_node(self, investigation_id: str, 
                              investigation_data: Dict) -> bool:
        """
        Add investigation to graph
        
        Args:
            investigation_id: Investigation identifier
            investigation_data: Investigation data
        
        Returns:
            True if successful
        """
        self.graph['investigations'][investigation_id] = investigation_data
        logger.info(f"Added investigation node: {investigation_id}")
        return True
    
    def add_ioc_node(self, ioc_id: str, ioc_data: Dict) -> bool:
        """Add IOC to graph"""
        self.graph['iocs'][ioc_id] = ioc_data
        logger.info(f"Added IOC node: {ioc_id}")
        return True
    
    def add_actor_node(self, actor_id: str, actor_data: Dict) -> bool:
        """Add threat actor to graph"""
        self.graph['actors'][actor_id] = actor_data
        logger.info(f"Added actor node: {actor_id}")
        return True
    
    def add_campaign_node(self, campaign_id: str, campaign_data: Dict) -> bool:
        """Add campaign to graph"""
        self.graph['campaigns'][campaign_id] = campaign_data
        logger.info(f"Added campaign node: {campaign_id}")
        return True
    
    def add_relationship(self, source_id: str, target_id: str, 
                         relationship_type: str) -> bool:
        """
        Add relationship between nodes
        
        Args:
            source_id: Source node identifier
            target_id: Target node identifier
            relationship_type: Type of relationship
        
        Returns:
            True if successful
        """
        relationship = {
            'source': source_id,
            'target': target_id,
            'type': relationship_type
        }
        self.graph['relationships'].append(relationship)
        logger.info(f"Added relationship: {source_id} --[{relationship_type}]--> {target_id}")
        return True
    
    def export_graph_json(self, output_path: str) -> bool:
        """
        Export complete graph to JSON
        
        Args:
            output_path: Path to save JSON file
        
        Returns:
            True if successful
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.graph, f, indent=2, default=str)
            logger.info(f"Exported graph to: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting graph: {e}")
            return False
    
    def get_graph_stats(self) -> Dict:
        """Get graph statistics"""
        return {
            'investigations': len(self.graph['investigations']),
            'iocs': len(self.graph['iocs']),
            'actors': len(self.graph['actors']),
            'campaigns': len(self.graph['campaigns']),
            'relationships': len(self.graph['relationships'])
        }


if __name__ == "__main__":
    logger.info("IOC Linker v1.0.0 loaded successfully")
    
    # Example usage
    linker = ObsidianIOCLinker("./vault")
    actor_linker = ThreatActorLinker("./vault")
    campaign_linker = CampaignLinker("./vault")
    graph_builder = InvestigationGraphBuilder("./vault")
    
    logger.info("All linker components initialized")
