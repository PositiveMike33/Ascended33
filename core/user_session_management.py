# ============================================================================
# USER SESSION MANAGEMENT - Session Lifecycle & Activity Tracking
# ============================================================================
# Purpose: Manage user sessions, authentication, and activity tracking
# Features: Session creation, token management, timeout handling
#
# Author: Ascended33 Platform
# Version: 1.0.0 (JOUR 2)
# Status: Production Ready
# ============================================================================

import logging
import json
import secrets
import sqlite3
from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Session:
    """User session object"""
    session_id: str
    user_id: str
    username: str
    created_at: str
    last_activity: str
    expires_at: str
    ip_address: str
    user_agent: str
    token: str
    is_active: bool = True
    activity_count: int = 0


@dataclass
class SessionActivity:
    """Session activity log entry"""
    activity_id: str
    session_id: str
    user_id: str
    action: str
    timestamp: str
    resource: str
    status: str


class SessionManager:
    """Manage user sessions and activity"""
    
    def __init__(self, db_path: str, session_timeout_minutes: int = 30):
        """
        Initialize session manager
        
        Args:
            db_path: Path to session database
            session_timeout_minutes: Session timeout in minutes
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
        self._init_database()
        logger.info(f"SessionManager initialized (timeout: {session_timeout_minutes}min)")
    
    def _init_database(self):
        """Initialize session database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                username TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_activity TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                token TEXT UNIQUE NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                activity_count INTEGER DEFAULT 0,
                created_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Session activity table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS session_activity (
                activity_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                resource TEXT,
                status TEXT,
                created_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_session(self, user_id: str, username: str, 
                      ip_address: str, user_agent: str) -> Session:
        """
        Create new user session
        
        Args:
            user_id: User ID
            username: Username
            ip_address: Client IP address
            user_agent: Browser user agent
        
        Returns:
            Session object
        """
        session_id = str(uuid.uuid4())
        token = secrets.token_urlsafe(32)
        now = datetime.utcnow().isoformat()
        expires_at = (datetime.utcnow() + self.session_timeout).isoformat()
        
        session = Session(
            session_id=session_id,
            user_id=user_id,
            username=username,
            created_at=now,
            last_activity=now,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
            token=token,
            is_active=True,
            activity_count=0
        )
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO sessions 
                (session_id, user_id, username, created_at, last_activity, 
                 expires_at, ip_address, user_agent, token, is_active, activity_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id, session.user_id, session.username,
                session.created_at, session.last_activity, session.expires_at,
                session.ip_address, session.user_agent, session.token,
                session.is_active, session.activity_count
            ))
            
            conn.commit()
            logger.info(f"Created session {session_id} for user {username}")
            
        except Exception as e:
            logger.error(f"Error creating session: {e}")
        finally:
            conn.close()
        
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Get session by ID
        
        Args:
            session_id: Session ID
        
        Returns:
            Session object or None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return Session(
            session_id=row[0],
            user_id=row[1],
            username=row[2],
            created_at=row[3],
            last_activity=row[4],
            expires_at=row[5],
            ip_address=row[6],
            user_agent=row[7],
            token=row[8],
            is_active=bool(row[9]),
            activity_count=row[10]
        )
    
    def get_session_by_token(self, token: str) -> Optional[Session]:
        """
        Get session by token
        
        Args:
            token: Session token
        
        Returns:
            Session object or None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM sessions WHERE token = ?", (token,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return Session(
            session_id=row[0],
            user_id=row[1],
            username=row[2],
            created_at=row[3],
            last_activity=row[4],
            expires_at=row[5],
            ip_address=row[6],
            user_agent=row[7],
            token=row[8],
            is_active=bool(row[9]),
            activity_count=row[10]
        )
    
    def update_last_activity(self, session_id: str) -> bool:
        """
        Update session last activity timestamp
        
        Args:
            session_id: Session ID
        
        Returns:
            Success status
        """
        now = datetime.utcnow().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE sessions 
            SET last_activity = ?, activity_count = activity_count + 1
            WHERE session_id = ?
        """, (now, session_id))
        
        conn.commit()
        conn.close()
        
        return True
    
    def end_session(self, session_id: str) -> bool:
        """
        End user session
        
        Args:
            session_id: Session ID
        
        Returns:
            Success status
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE sessions SET is_active = 0 WHERE session_id = ?",
            (session_id,)
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Ended session {session_id}")
        return True
    
    def get_user_sessions(self, user_id: str, 
                         active_only: bool = True) -> List[Session]:
        """
        Get all sessions for a user
        
        Args:
            user_id: User ID
            active_only: Only return active sessions
        
        Returns:
            List of Session objects
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM sessions WHERE user_id = ?"
        params = [user_id]
        
        if active_only:
            query += " AND is_active = 1"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        sessions = []
        for row in rows:
            sessions.append(Session(
                session_id=row[0],
                user_id=row[1],
                username=row[2],
                created_at=row[3],
                last_activity=row[4],
                expires_at=row[5],
                ip_address=row[6],
                user_agent=row[7],
                token=row[8],
                is_active=bool(row[9]),
                activity_count=row[10]
            ))
        
        return sessions
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions
        
        Returns:
            Number of sessions cleaned
        """
        now = datetime.utcnow().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE sessions SET is_active = 0 WHERE expires_at < ?",
            (now,)
        )
        
        cleaned = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"Cleaned up {cleaned} expired sessions")
        return cleaned
    
    def is_session_valid(self, session_id: str) -> bool:
        """
        Check if session is valid and active
        
        Args:
            session_id: Session ID
        
        Returns:
            Validity status
        """
        session = self.get_session(session_id)
        
        if not session:
            return False
        
        if not session.is_active:
            return False
        
        now = datetime.utcnow()
        expires = datetime.fromisoformat(session.expires_at)
        
        if now > expires:
            self.end_session(session_id)
            return False
        
        return True


class SessionActivityLogger:
    """Log and track session activities"""
    
    def __init__(self, session_manager: SessionManager):
        """
        Initialize activity logger
        
        Args:
            session_manager: SessionManager instance
        """
        self.session_manager = session_manager
        logger.info("SessionActivityLogger initialized")
    
    def log_activity(self, session_id: str, user_id: str, action: str,
                    resource: str = "", status: str = "success") -> str:
        """
        Log session activity
        
        Args:
            session_id: Session ID
            user_id: User ID
            action: Action performed
            resource: Resource affected
            status: Action status
        
        Returns:
            Activity ID
        """
        activity_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        conn = sqlite3.connect(self.session_manager.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO session_activity 
                (activity_id, session_id, user_id, action, timestamp, resource, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (activity_id, session_id, user_id, action, timestamp, resource, status))
            
            conn.commit()
            logger.info(f"Logged activity: {action} for session {session_id}")
            
            # Update session last activity
            self.session_manager.update_last_activity(session_id)
            
            return activity_id
            
        except Exception as e:
            logger.error(f"Error logging activity: {e}")
            return ""
        finally:
            conn.close()
    
    def get_session_activities(self, session_id: str, 
                              limit: int = 100) -> List[SessionActivity]:
        """
        Get session activities
        
        Args:
            session_id: Session ID
            limit: Maximum entries
        
        Returns:
            List of activities
        """
        conn = sqlite3.connect(self.session_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM session_activity 
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (session_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        activities = []
        for row in rows:
            activities.append(SessionActivity(
                activity_id=row[0],
                session_id=row[1],
                user_id=row[2],
                action=row[3],
                timestamp=row[4],
                resource=row[5],
                status=row[6]
            ))
        
        return activities
    
    def get_user_activity_summary(self, user_id: str, 
                                 hours_back: int = 24) -> Dict:
        """
        Get summary of user activities
        
        Args:
            user_id: User ID
            hours_back: Hours to look back
        
        Returns:
            Activity summary dictionary
        """
        conn = sqlite3.connect(self.session_manager.db_path)
        cursor = conn.cursor()
        
        cutoff_time = (datetime.utcnow() - timedelta(hours=hours_back)).isoformat()
        
        cursor.execute("""
            SELECT action, COUNT(*) as count, status 
            FROM session_activity 
            WHERE user_id = ? AND timestamp >= ?
            GROUP BY action, status
        """, (user_id, cutoff_time))
        
        rows = cursor.fetchall()
        conn.close()
        
        summary = {
            'user_id': user_id,
            'period_hours': hours_back,
            'total_activities': sum(row[1] for row in rows),
            'action_breakdown': {},
            'generated_at': datetime.utcnow().isoformat()
        }
        
        for row in rows:
            action = row[0]
            count = row[1]
            status = row[2]
            
            if action not in summary['action_breakdown']:
                summary['action_breakdown'][action] = {'success': 0, 'failure': 0}
            
            summary['action_breakdown'][action][status] = count
        
        return summary
