# ============================================================================
# AUDIT TRAIL SYSTEM - Immutable Change Logging & Compliance
# ============================================================================
# Purpose: Track all user actions with cryptographic integrity verification
# Features: Immutable logging, hashing, compliance reporting
#
# Author: Ascended33 Platform
# Version: 1.0.0 (JOUR 2)
# Status: Production Ready
# ============================================================================

import logging
import json
import hashlib
import sqlite3
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuditActionType(Enum):
    """Audit log action types"""
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_CREATE = "user_create"
    USER_DELETE = "user_delete"
    USER_UPDATE = "user_update"
    INVESTIGATION_CREATE = "investigation_create"
    INVESTIGATION_UPDATE = "investigation_update"
    INVESTIGATION_DELETE = "investigation_delete"
    IOC_ADD = "ioc_add"
    IOC_DELETE = "ioc_delete"
    EXPORT_DATA = "export_data"
    IMPORT_DATA = "import_data"
    CONFIG_CHANGE = "config_change"
    PERMISSION_GRANT = "permission_grant"
    PERMISSION_REVOKE = "permission_revoke"
    SYSTEM_ACCESS = "system_access"
    SECURITY_EVENT = "security_event"
    API_CALL = "api_call"


@dataclass
class AuditEntry:
    """Single audit log entry"""
    entry_id: str
    timestamp: str
    user_id: str
    action_type: str
    resource_type: str
    resource_id: str
    details: Dict
    ip_address: str
    user_agent: str
    status: str  # "success" or "failure"
    previous_hash: str
    entry_hash: str


class AuditTrailManager:
    """Manage immutable audit trail with cryptographic integrity"""
    
    def __init__(self, db_path: str):
        """
        Initialize audit trail manager
        
        Args:
            db_path: Path to audit database
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        self.previous_hash = self._get_chain_hash()
        logger.info(f"AuditTrailManager initialized at {db_path}")
    
    def _init_database(self):
        """Initialize audit database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Audit log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                entry_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                user_id TEXT NOT NULL,
                action_type TEXT NOT NULL,
                resource_type TEXT NOT NULL,
                resource_id TEXT,
                details TEXT,
                ip_address TEXT,
                user_agent TEXT,
                status TEXT,
                previous_hash TEXT,
                entry_hash TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Compliance events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS compliance_events (
                event_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                event_type TEXT,
                severity TEXT,
                description TEXT,
                user_id TEXT,
                remediation_required BOOLEAN,
                remediation_details TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Hash chain table for integrity
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hash_chain (
                chain_id TEXT PRIMARY KEY,
                block_number INTEGER,
                timestamp TEXT,
                block_hash TEXT,
                previous_hash TEXT,
                entries_count INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _get_chain_hash(self) -> str:
        """Get the last hash in the chain"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT block_hash FROM hash_chain ORDER BY block_number DESC LIMIT 1"
        )
        row = cursor.fetchone()
        conn.close()
        
        return row[0] if row else hashlib.sha256(b"CHAIN_START").hexdigest()
    
    def _calculate_entry_hash(self, entry_data: Dict, previous_hash: str) -> str:
        """Calculate entry hash with previous hash"""
        data_str = json.dumps(entry_data, sort_keys=True)
        combined = f"{previous_hash}{data_str}"
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def log_action(self, user_id: str, action_type: AuditActionType, 
                  resource_type: str, resource_id: Optional[str] = None,
                  details: Optional[Dict] = None, ip_address: str = "0.0.0.0",
                  user_agent: str = "unknown", status: str = "success") -> str:
        """
        Log user action to audit trail
        
        Args:
            user_id: User ID performing action
            action_type: Type of action
            resource_type: Type of resource affected
            resource_id: ID of resource (optional)
            details: Additional action details
            ip_address: IP address of user
            user_agent: User agent string
            status: Action status (success/failure)
        
        Returns:
            Entry ID
        """
        entry_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        if details is None:
            details = {}
        
        # Create entry data
        entry_data = {
            'entry_id': entry_id,
            'timestamp': timestamp,
            'user_id': user_id,
            'action_type': action_type.value,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'details': details,
            'status': status
        }
        
        # Calculate hash
        entry_hash = self._calculate_entry_hash(entry_data, self.previous_hash)
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO audit_log 
                (entry_id, timestamp, user_id, action_type, resource_type, 
                 resource_id, details, ip_address, user_agent, status, 
                 previous_hash, entry_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry_id, timestamp, user_id, action_type.value,
                resource_type, resource_id, json.dumps(details),
                ip_address, user_agent, status, self.previous_hash, entry_hash
            ))
            
            conn.commit()
            
            # Update chain hash
            self.previous_hash = entry_hash
            logger.info(f"Logged action: {action_type.value} for {resource_type}")
            
            return entry_id
            
        except Exception as e:
            logger.error(f"Error logging action: {e}")
            return ""
        finally:
            conn.close()
    
    def get_audit_log(self, user_id: Optional[str] = None, 
                     action_type: Optional[str] = None,
                     days_back: int = 30, limit: int = 1000) -> List[Dict]:
        """
        Retrieve audit log entries
        
        Args:
            user_id: Filter by user (optional)
            action_type: Filter by action type (optional)
            days_back: Number of days to look back
            limit: Maximum entries to return
        
        Returns:
            List of audit entries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = (datetime.utcnow() - timedelta(days=days_back)).isoformat()
        
        query = "SELECT * FROM audit_log WHERE timestamp >= ? "
        params = [cutoff_date]
        
        if user_id:
            query += "AND user_id = ? "
            params.append(user_id)
        
        if action_type:
            query += "AND action_type = ? "
            params.append(action_type)
        
        query += "ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        entries = []
        for row in rows:
            entries.append({
                'entry_id': row[0],
                'timestamp': row[1],
                'user_id': row[2],
                'action_type': row[3],
                'resource_type': row[4],
                'resource_id': row[5],
                'details': json.loads(row[6]) if row[6] else {},
                'ip_address': row[7],
                'user_agent': row[8],
                'status': row[9]
            })
        
        return entries
    
    def verify_chain_integrity(self) -> Dict:
        """
        Verify integrity of audit trail hash chain
        
        Returns:
            Verification result dictionary
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM audit_log ORDER BY timestamp ASC")
        rows = cursor.fetchall()
        conn.close()
        
        current_hash = hashlib.sha256(b"CHAIN_START").hexdigest()
        integrity_ok = True
        invalid_entries = []
        
        for row in rows:
            entry_id = row[0]
            stored_previous_hash = row[10]
            stored_entry_hash = row[11]
            
            # Verify chain continuity
            if stored_previous_hash != current_hash:
                integrity_ok = False
                invalid_entries.append(entry_id)
            
            # Recalculate hash
            entry_data = {
                'entry_id': row[0],
                'timestamp': row[1],
                'user_id': row[2],
                'action_type': row[3],
                'resource_type': row[4],
                'resource_id': row[5],
                'details': json.loads(row[6]) if row[6] else {},
                'status': row[9]
            }
            
            calculated_hash = self._calculate_entry_hash(entry_data, current_hash)
            
            if calculated_hash != stored_entry_hash:
                integrity_ok = False
                invalid_entries.append(entry_id)
            
            current_hash = stored_entry_hash
        
        return {
            'integrity_valid': integrity_ok,
            'total_entries': len(rows),
            'invalid_entries': invalid_entries,
            'verification_time': datetime.utcnow().isoformat()
        }


class ComplianceReportGenerator:
    """Generate compliance reports from audit trail"""
    
    def __init__(self, audit_manager: AuditTrailManager):
        """
        Initialize compliance report generator
        
        Args:
            audit_manager: AuditTrailManager instance
        """
        self.audit_manager = audit_manager
        logger.info("ComplianceReportGenerator initialized")
    
    def generate_user_activity_report(self, user_id: str, 
                                     start_date: str, 
                                     end_date: str) -> Dict:
        """
        Generate user activity report for compliance
        
        Args:
            user_id: User ID
            start_date: Start date ISO format
            end_date: End date ISO format
        
        Returns:
            Compliance report dictionary
        """
        entries = self.audit_manager.get_audit_log(user_id=user_id)
        
        # Filter by date range
        filtered_entries = [
            e for e in entries 
            if start_date <= e['timestamp'] <= end_date
        ]
        
        # Aggregate statistics
        action_counts = {}
        failed_actions = []
        resource_counts = {}
        
        for entry in filtered_entries:
            # Count actions
            action = entry['action_type']
            action_counts[action] = action_counts.get(action, 0) + 1
            
            # Track failures
            if entry['status'] == 'failure':
                failed_actions.append(entry)
            
            # Count resources
            resource = entry['resource_type']
            resource_counts[resource] = resource_counts.get(resource, 0) + 1
        
        report = {
            'report_id': str(uuid.uuid4()),
            'user_id': user_id,
            'period_start': start_date,
            'period_end': end_date,
            'total_actions': len(filtered_entries),
            'action_breakdown': action_counts,
            'resource_breakdown': resource_counts,
            'failed_actions_count': len(failed_actions),
            'failed_actions': failed_actions[:10],  # Last 10 failures
            'generated_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Generated compliance report for {user_id}")
        return report
    
    def generate_security_events_report(self, days_back: int = 30) -> Dict:
        """
        Generate security events report
        
        Args:
            days_back: Number of days to report on
        
        Returns:
            Security events report
        """
        entries = self.audit_manager.get_audit_log(
            action_type='SECURITY_EVENT',
            days_back=days_back
        )
        
        # Categorize events
        high_severity = [e for e in entries if e.get('details', {}).get('severity') == 'high']
        medium_severity = [e for e in entries if e.get('details', {}).get('severity') == 'medium']
        low_severity = [e for e in entries if e.get('details', {}).get('severity') == 'low']
        
        report = {
            'report_id': str(uuid.uuid4()),
            'period_days': days_back,
            'total_events': len(entries),
            'high_severity_count': len(high_severity),
            'medium_severity_count': len(medium_severity),
            'low_severity_count': len(low_severity),
            'high_severity_events': high_severity[:5],
            'generated_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Generated security events report")
        return report


class AuditSearchEngine:
    """Search and filter audit logs"""
    
    def __init__(self, audit_manager: AuditTrailManager):
        """
        Initialize search engine
        
        Args:
            audit_manager: AuditTrailManager instance
        """
        self.audit_manager = audit_manager
        logger.info("AuditSearchEngine initialized")
    
    def search_by_criteria(self, **kwargs) -> List[Dict]:
        """
        Search audit log by multiple criteria
        
        Args:
            **kwargs: Search criteria
        
        Returns:
            Matching entries
        """
        user_id = kwargs.get('user_id')
        action_type = kwargs.get('action_type')
        days_back = kwargs.get('days_back', 30)
        resource_type = kwargs.get('resource_type')
        status = kwargs.get('status')
        
        entries = self.audit_manager.get_audit_log(
            user_id=user_id,
            action_type=action_type,
            days_back=days_back
        )
        
        # Apply additional filters
        if resource_type:
            entries = [e for e in entries if e['resource_type'] == resource_type]
        
        if status:
            entries = [e for e in entries if e['status'] == status]
        
        logger.info(f"Found {len(entries)} matching audit entries")
        return entries
    
    def get_user_session_activity(self, user_id: str, 
                                 session_start: str) -> List[Dict]:
        """
        Get all activity from a user session
        
        Args:
            user_id: User ID
            session_start: Session start timestamp
        
        Returns:
            Session activities
        """
        entries = self.audit_manager.get_audit_log(user_id=user_id)
        
        # Filter to session period (1 hour after start)
        from datetime import datetime as dt
        start_dt = dt.fromisoformat(session_start)
        end_dt = start_dt + timedelta(hours=1)
        
        session_entries = [
            e for e in entries 
            if start_dt.isoformat() <= e['timestamp'] <= end_dt.isoformat()
        ]
        
        return session_entries
