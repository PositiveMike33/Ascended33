# ================================================================
# AUTO SYNC CONFIGURATION
# Automatic Vault synchronization and reconnection manager
# ================================================================

import os
import json
import time
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VaultAutoSyncConfig:
    """Manages automatic synchronization configuration"""
    
    def __init__(self, vault_path="D:\\Vault\\Vault", repo_path="D:\\Vault\\Vault\\Ascended33"):
        self.vault_path = Path(vault_path)
        self.repo_path = Path(repo_path)
        self.config_file = self.repo_path / "config" / "auto_sync.json"
        self.state_file = self.vault_path / ".auto_sync_state.json"
        self.reconnect_log = self.vault_path / ".reconnect_log.json"
        
        # Ensure config directory exists
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load or create config
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load auto-sync configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading config: {e}")
        
        # Create default config
        return self._create_default_config()
    
    def _create_default_config(self) -> Dict:
        """Create default auto-sync configuration"""
        config = {
            "version": "1.0",
            "enabled": True,
            "vault": {
                "path": str(self.vault_path),
                "auto_mount": True,
                "auto_reconnect": True,
                "reconnect_interval": 5,  # seconds
                "reconnect_max_attempts": 0  # 0 = infinite
            },
            "sync": {
                "enabled": True,
                "bidirectional": True,
                "monitor_folders": [
                    "HACKERGPT/HEXSTRIKE",
                    "HACKERGPT/OSINT_Profilage",
                    "HACKERGPT/Pentest",
                    "ENQUETES_OSINT",
                    "Claude-Michael/Sessions",
                    "_BRAIN",
                    "REPORT"
                ],
                "auto_backup": True,
                "backup_interval": 3600  # 1 hour
            },
            "output": {
                "destination": str(self.vault_path),
                "auto_organize": True,
                "create_folders": True,
                "overwrite_existing": False
            },
            "monitoring": {
                "enabled": True,
                "watch_interval": 1,  # seconds
                "debounce_delay": 2,  # seconds
                "max_queue_size": 1000
            },
            "logging": {
                "enabled": True,
                "log_file": str(self.vault_path / ".ascended33_sync.log"),
                "log_level": "INFO",
                "max_log_size": 10485760  # 10MB
            },
            "shortcuts": {
                "auto_create": True,
                "target_path": str(Path.home() / "OneDrive" / "Desktop"),
                "shortcuts": [
                    {
                        "name": "Ascended33",
                        "target": str(self.repo_path / "ASCENDED33_LAUNCH.ps1"),
                        "description": "Launch Ascended33 Mission Control"
                    },
                    {
                        "name": "Vault Sync",
                        "target": str(self.repo_path / "vault_sync" / "vault_monitor.py"),
                        "description": "Monitor and sync Vault"
                    },
                    {
                        "name": "Vault Status",
                        "target": str(self.repo_path / "verify_connections.py"),
                        "description": "Check Vault connection status"
                    }
                ]
            }
        }
        
        # Save default config
        self._save_config(config)
        return config
    
    def _save_config(self, config: Dict) -> bool:
        """Save configuration to file"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            logger.info(f"Config saved to {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False
    
    def verify_vault_connection(self) -> bool:
        """Verify Vault is accessible"""
        if not self.vault_path.exists():
            logger.error(f"Vault not found: {self.vault_path}")
            return False
        
        if not self.vault_path.is_dir():
            logger.error(f"Vault path is not a directory: {self.vault_path}")
            return False
        
        # Check write permissions
        test_file = self.vault_path / ".ascended33_test"
        try:
            test_file.write_text("test")
            test_file.unlink()
            logger.info("Vault connection verified successfully")
            return True
        except Exception as e:
            logger.error(f"Vault write test failed: {e}")
            return False
    
    def ensure_vault_folders(self) -> bool:
        """Create all required Vault folders"""
        monitor_folders = self.config.get("sync", {}).get("monitor_folders", [])
        
        created_count = 0
        for folder in monitor_folders:
            folder_path = self.vault_path / folder
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
                created_count += 1
                logger.info(f"Ensured folder: {folder}")
            except Exception as e:
                logger.error(f"Error creating folder {folder}: {e}")
        
        logger.info(f"Ensured {created_count}/{len(monitor_folders)} folders")
        return created_count == len(monitor_folders)
    
    def mark_vault_connected(self) -> bool:
        """Mark Vault as connected and ready"""
        try:
            state = {
                "connected": True,
                "timestamp": datetime.now().isoformat(),
                "vault_path": str(self.vault_path),
                "repo_path": str(self.repo_path),
                "version": self.config.get("version", "1.0")
            }
            
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
            
            logger.info("Vault marked as connected")
            return True
        except Exception as e:
            logger.error(f"Error marking Vault as connected: {e}")
            return False
    
    def check_vault_status(self) -> Dict:
        """Check Vault status"""
        status = {
            "vault_path": str(self.vault_path),
            "repo_path": str(self.repo_path),
            "vault_exists": self.vault_path.exists(),
            "vault_accessible": self.verify_vault_connection(),
            "state_file_exists": self.state_file.exists(),
            "config_valid": self._is_config_valid(),
            "timestamp": datetime.now().isoformat()
        }
        
        return status
    
    def _is_config_valid(self) -> bool:
        """Validate configuration"""
        required_keys = ["vault", "sync", "output", "monitoring"]
        return all(key in self.config for key in required_keys)
    
    def add_reconnect_log(self, success: bool, reason: str = ""):
        """Add entry to reconnection log"""
        try:
            logs = []
            if self.reconnect_log.exists():
                with open(self.reconnect_log, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            
            logs.append({
                "timestamp": datetime.now().isoformat(),
                "success": success,
                "reason": reason
            })
            
            # Keep only last 100 logs
            logs = logs[-100:]
            
            with open(self.reconnect_log, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            logger.error(f"Error adding reconnect log: {e}")
    
    def get_output_paths(self) -> Dict[str, Path]:
        """Get all output paths for different content types"""
        base = self.vault_path
        
        paths = {
            "reports": base / "REPORT",
            "osint": base / "HACKERGPT" / "OSINT_Profilage",
            "hexstrike": base / "HACKERGPT" / "HEXSTRIKE",
            "pentest": base / "HACKERGPT" / "Pentest",
            "investigations": base / "ENQUETES_OSINT",
            "sessions": base / "Claude-Michael" / "Sessions",
            "brain": base / "_BRAIN",
            "default": base
        }
        
        return paths
    
    def get_sync_folders(self) -> List[Path]:
        """Get all folders that should be monitored"""
        folders = self.config.get("sync", {}).get("monitor_folders", [])
        return [self.vault_path / folder for folder in folders]


class VaultReconnectManager:
    """Manages automatic Vault reconnection"""
    
    def __init__(self, config_manager: VaultAutoSyncConfig):
        self.config_mgr = config_manager
        self.reconnect_attempts = 0
        self.last_check = None
        self.connected = False
    
    def check_and_reconnect(self) -> bool:
        """Check Vault connection and reconnect if needed"""
        logger.info("Checking Vault connection...")
        
        # Check if Vault is accessible
        if self.config_mgr.verify_vault_connection():
            if not self.connected:
                logger.info("Vault reconnected!")
                self.connected = True
                self.reconnect_attempts = 0
                self.config_mgr.mark_vault_connected()
                self.config_mgr.add_reconnect_log(True, "Vault reconnected")
            
            return True
        else:
            logger.warning("Vault not accessible")
            self.connected = False
            self.reconnect_attempts += 1
            self.config_mgr.add_reconnect_log(False, "Vault disconnected")
            
            # Check reconnection limits
            max_attempts = self.config_mgr.config.get("vault", {}).get("reconnect_max_attempts", 0)
            if max_attempts > 0 and self.reconnect_attempts >= max_attempts:
                logger.error(f"Max reconnection attempts ({max_attempts}) reached")
                return False
            
            return False
    
    def start_continuous_monitoring(self):
        """Start continuous Vault monitoring"""
        import threading
        
        def monitor_loop():
            while True:
                try:
                    self.check_and_reconnect()
                    interval = self.config_mgr.config.get("vault", {}).get("reconnect_interval", 5)
                    time.sleep(interval)
                except Exception as e:
                    logger.error(f"Error in monitor loop: {e}")
                    time.sleep(5)
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
        logger.info("Continuous Vault monitoring started")


def setup_auto_sync():
    """Setup and initialize auto-sync system"""
    logger.info("Initializing Auto-Sync System...")
    
    # Create config manager
    config_mgr = VaultAutoSyncConfig()
    
    # Verify Vault connection
    if not config_mgr.verify_vault_connection():
        logger.error("Cannot connect to Vault!")
        return None
    
    # Ensure all folders exist
    config_mgr.ensure_vault_folders()
    
    # Mark as connected
    config_mgr.mark_vault_connected()
    
    # Create reconnect manager
    reconnect_mgr = VaultReconnectManager(config_mgr)
    reconnect_mgr.start_continuous_monitoring()
    
    logger.info("Auto-Sync System initialized successfully")
    
    return {
        "config": config_mgr,
        "reconnect": reconnect_mgr,
        "status": config_mgr.check_vault_status()
    }


if __name__ == "__main__":
    # Initialize and test
    result = setup_auto_sync()
    if result:
        print("\n✓ Auto-Sync System Ready")
        print(f"Status: {json.dumps(result['status'], indent=2)}")
