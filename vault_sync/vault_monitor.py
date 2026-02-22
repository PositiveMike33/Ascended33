# ================================================================
# VAULT MONITOR - Real-time Vault Synchronization
# Monitors D:\Vault\Vault for changes and syncs automatically
# ================================================================

import os
import json
import time
import hashlib
import threading
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VaultChangeHandler(FileSystemEventHandler):
    """Handles file system events in the Vault directory"""
    
    def __init__(self, vault_path, sync_callback):
        super().__init__()
        self.vault_path = vault_path
        self.sync_callback = sync_callback
        self.last_event_time = {}
        self.debounce_delay = 2  # Seconds
        
    def on_created(self, event):
        """Handle file/folder creation"""
        if not event.is_directory:
            self._handle_change(event, "created")
    
    def on_modified(self, event):
        """Handle file/folder modification"""
        if not event.is_directory:
            self._handle_change(event, "modified")
    
    def on_deleted(self, event):
        """Handle file/folder deletion"""
        if not event.is_directory:
            self._handle_change(event, "deleted")
    
    def _handle_change(self, event, event_type):
        """Process file changes with debouncing"""
        file_path = event.src_path
        
        # Debounce: ignore duplicate events within 2 seconds
        if file_path in self.last_event_time:
            if time.time() - self.last_event_time[file_path] < self.debounce_delay:
                return
        
        self.last_event_time[file_path] = time.time()
        
        # Skip temporary files and system files
        if self._should_ignore(file_path):
            return
        
        logger.info(f"Vault change detected: {event_type} - {file_path}")
        
        # Trigger sync callback
        self.sync_callback(file_path, event_type)
    
    @staticmethod
    def _should_ignore(file_path):
        """Check if file should be ignored"""
        ignore_patterns = [
            '.obsidian',
            '.git',
            '__pycache__',
            '.pyc',
            '.tmp',
            '.lock',
            'desktop.ini',
            'Thumbs.db'
        ]
        
        path_lower = file_path.lower()
        return any(pattern in path_lower for pattern in ignore_patterns)


class VaultMonitor:
    """Monitors and syncs Vault directory"""
    
    def __init__(self, vault_path="D:\\Vault\\Vault"):
        self.vault_path = Path(vault_path)
        self.sync_index_path = self.vault_path / ".vault_sync.json"
        self.observer = None
        self.sync_thread = None
        self.is_running = False
        self.sync_queue = []
        self.sync_lock = threading.Lock()
        
        # Load or create sync index
        self.sync_index = self._load_sync_index()
    
    def start(self):
        """Start monitoring the Vault"""
        if self.is_running:
            logger.warning("Vault Monitor already running")
            return
        
        logger.info(f"Starting Vault Monitor for: {self.vault_path}")
        
        # Start observer
        event_handler = VaultChangeHandler(str(self.vault_path), self._queue_sync)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.vault_path), recursive=True)
        self.observer.start()
        
        # Start sync thread
        self.is_running = True
        self.sync_thread = threading.Thread(target=self._sync_worker, daemon=True)
        self.sync_thread.start()
        
        logger.info("Vault Monitor started successfully")
    
    def stop(self):
        """Stop monitoring the Vault"""
        logger.info("Stopping Vault Monitor...")
        
        self.is_running = False
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        if self.sync_thread:
            self.sync_thread.join(timeout=5)
        
        logger.info("Vault Monitor stopped")
    
    def _queue_sync(self, file_path, event_type):
        """Queue a file for synchronization"""
        with self.sync_lock:
            self.sync_queue.append({
                'path': file_path,
                'type': event_type,
                'timestamp': datetime.now().isoformat()
            })
    
    def _sync_worker(self):
        """Worker thread that processes sync queue"""
        while self.is_running:
            with self.sync_lock:
                if self.sync_queue:
                    sync_item = self.sync_queue.pop(0)
                else:
                    sync_item = None
            
            if sync_item:
                self._process_sync(sync_item)
            else:
                time.sleep(0.1)
    
    def _process_sync(self, sync_item):
        """Process a sync item"""
        file_path = sync_item['path']
        event_type = sync_item['type']
        
        try:
            # Update sync index
            self._update_sync_index(file_path, event_type)
            
            # Log the sync
            logger.info(f"Synced ({event_type}): {file_path}")
            
        except Exception as e:
            logger.error(f"Sync error for {file_path}: {e}")
    
    def _update_sync_index(self, file_path, event_type):
        """Update the sync index file"""
        rel_path = os.path.relpath(file_path, self.vault_path)
        
        if event_type == "deleted":
            if rel_path in self.sync_index:
                del self.sync_index[rel_path]
        else:
            # Calculate file hash for integrity check
            file_hash = self._calculate_hash(file_path)
            
            self.sync_index[rel_path] = {
                'path': file_path,
                'type': event_type,
                'hash': file_hash,
                'timestamp': datetime.now().isoformat(),
                'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
            }
        
        # Save sync index
        self._save_sync_index()
    
    def _calculate_hash(self, file_path):
        """Calculate SHA256 hash of file"""
        if not os.path.exists(file_path) or os.path.isdir(file_path):
            return None
        
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _load_sync_index(self):
        """Load sync index from file"""
        if self.sync_index_path.exists():
            try:
                with open(self.sync_index_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading sync index: {e}")
                return {}
        return {}
    
    def _save_sync_index(self):
        """Save sync index to file"""
        try:
            with open(self.sync_index_path, 'w', encoding='utf-8') as f:
                json.dump(self.sync_index, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving sync index: {e}")
    
    def get_sync_status(self):
        """Get current sync status"""
        return {
            'running': self.is_running,
            'vault_path': str(self.vault_path),
            'files_tracked': len(self.sync_index),
            'queue_size': len(self.sync_queue),
            'index': self.sync_index
        }
    
    def full_resync(self):
        """Perform a full resync of the entire Vault"""
        logger.info("Starting full Vault resync...")
        
        self.sync_index.clear()
        
        for root, dirs, files in os.walk(self.vault_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not self._should_ignore_dir(d)]
            
            for file in files:
                file_path = os.path.join(root, file)
                if not VaultChangeHandler._should_ignore(file_path):
                    self._update_sync_index(file_path, "created")
        
        logger.info(f"Full resync complete - {len(self.sync_index)} files indexed")
    
    @staticmethod
    def _should_ignore_dir(dir_name):
        """Check if directory should be ignored"""
        ignore_dirs = ['.obsidian', '.git', '__pycache__', '.vault_sync']
        return dir_name in ignore_dirs


class VaultAutoconnect:
    """Auto-connect and verify Vault connection"""
    
    def __init__(self, vault_path="D:\\Vault\\Vault"):
        self.vault_path = Path(vault_path)
        self.status_file = self.vault_path / ".vault_connected"
        self.last_check = None
    
    def check_connection(self):
        """Check if Vault is accessible"""
        return self.vault_path.exists() and self.vault_path.is_dir()
    
    def mark_connected(self):
        """Mark Vault as connected"""
        try:
            with open(self.status_file, 'w') as f:
                json.dump({
                    'connected': True,
                    'timestamp': datetime.now().isoformat(),
                    'vault_path': str(self.vault_path)
                }, f)
            self.last_check = datetime.now()
            logger.info("Vault marked as connected")
            return True
        except Exception as e:
            logger.error(f"Error marking Vault as connected: {e}")
            return False
    
    def is_connected(self):
        """Check if Vault was previously connected"""
        if self.status_file.exists():
            try:
                with open(self.status_file, 'r') as f:
                    data = json.load(f)
                    return data.get('connected', False)
            except:
                return False
        return False
    
    def auto_reconnect(self):
        """Automatically reconnect when Vault becomes available"""
        logger.info("Attempting automatic Vault reconnection...")
        
        if self.check_connection():
            if self.mark_connected():
                logger.info("Vault auto-reconnected successfully")
                return True
        
        logger.warning("Vault auto-reconnection failed - Vault not accessible")
        return False


def monitor_vault_background():
    """Background monitoring function"""
    monitor = VaultMonitor()
    monitor.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutdown signal received")
        monitor.stop()


if __name__ == "__main__":
    # Test the monitor
    monitor = VaultMonitor()
    monitor.start()
    
    try:
        print(f"Monitoring Vault: D:\\Vault\\Vault")
        print("Press Ctrl+C to stop...")
        while True:
            time.sleep(1)
            status = monitor.get_sync_status()
            if status['queue_size'] > 0:
                print(f"Sync queue: {status['queue_size']} items")
    except KeyboardInterrupt:
        monitor.stop()
        print("Monitor stopped")
