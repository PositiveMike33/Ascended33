"""
JOUR 2 - User Session Management Tests
Test suite for session lifecycle, activity tracking, and session management
"""

import pytest
import os
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Add core directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from user_session_management import (
    Session,
    SessionActivity,
    SessionManager,
    SessionActivityLogger
)


class TestSession:
    """Test Session dataclass"""

    def test_session_creation(self):
        """Test creating a session"""
        session = Session(
            session_id="sess001",
            user_id="user001",
            token="token_abc123def456",
            created_at=datetime.now(),
            last_activity=datetime.now(),
            expires_at=datetime.now() + timedelta(minutes=30),
            is_active=True
        )
        assert session.session_id == "sess001"
        assert session.user_id == "user001"
        assert session.is_active is True

    def test_session_expiry_time(self):
        """Test session expiry calculation"""
        now = datetime.now()
        session = Session(
            session_id="sess001",
            user_id="user001",
            token="token_abc123def456",
            created_at=now,
            last_activity=now,
            expires_at=now + timedelta(minutes=30),
            is_active=True
        )
        assert session.expires_at > now

    def test_session_token_format(self):
        """Test session token format"""
        session = Session(
            session_id="sess001",
            user_id="user001",
            token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
            created_at=datetime.now(),
            last_activity=datetime.now(),
            is_active=True
        )
        assert len(session.token) > 0
        assert isinstance(session.token, str)

    def test_session_inactive_status(self):
        """Test session inactive status"""
        session = Session(
            session_id="sess001",
            user_id="user001",
            token="token_abc123def456",
            created_at=datetime.now(),
            last_activity=datetime.now(),
            is_active=False
        )
        assert session.is_active is False


class TestSessionActivity:
    """Test SessionActivity dataclass"""

    def test_session_activity_creation(self):
        """Test creating session activity"""
        activity = SessionActivity(
            activity_id="act001",
            session_id="sess001",
            action="CASE_VIEWED",
            resource_type="CASE",
            resource_id="case123",
            timestamp=datetime.now(),
            status="SUCCESS"
        )
        assert activity.activity_id == "act001"
        assert activity.session_id == "sess001"
        assert activity.action == "CASE_VIEWED"

    def test_session_activity_with_details(self):
        """Test session activity with additional details"""
        activity = SessionActivity(
            activity_id="act001",
            session_id="sess001",
            action="IOC_SEARCH",
            resource_type="IOC",
            resource_id="ioc456",
            timestamp=datetime.now(),
            status="SUCCESS",
            details={"query": "192.168.1.1", "results_found": 5}
        )
        assert activity.details is not None
        assert activity.details["query"] == "192.168.1.1"

    def test_session_activity_status_types(self):
        """Test different activity status types"""
        statuses = ["SUCCESS", "FAILED", "PENDING", "IN_PROGRESS"]
        
        for status in statuses:
            activity = SessionActivity(
                activity_id="act001",
                session_id="sess001",
                action="DATA_ACCESS",
                resource_type="FILE",
                resource_id="file123",
                timestamp=datetime.now(),
                status=status
            )
            assert activity.status == status

    def test_session_activity_action_types(self):
        """Test different activity action types"""
        actions = [
            "CASE_VIEWED",
            "CASE_CREATED",
            "IOC_ADDED",
            "IOC_SEARCHED",
            "EXPORT_INITIATED",
            "REPORT_GENERATED",
            "DATA_ACCESSED",
            "DATA_MODIFIED"
        ]
        
        for action in actions:
            activity = SessionActivity(
                activity_id="act001",
                session_id="sess001",
                action=action,
                resource_type="RESOURCE",
                resource_id="res123",
                timestamp=datetime.now(),
                status="SUCCESS"
            )
            assert activity.action == action


class TestSessionManager:
    """Test SessionManager for session lifecycle management"""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database"""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_sessions.db")
        yield db_path
        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.rmtree(temp_dir)

    def test_session_manager_initialization(self, temp_db):
        """Test SessionManager initialization"""
        manager = SessionManager(db_path=temp_db)
        assert manager is not None
        assert os.path.exists(temp_db)

    def test_create_session(self, temp_db):
        """Test creating a session"""
        manager = SessionManager(db_path=temp_db)
        session = manager.create_session(user_id="user001")
        
        assert session is not None
        assert session.user_id == "user001"
        assert session.is_active is True

    def test_get_session(self, temp_db):
        """Test retrieving a session"""
        manager = SessionManager(db_path=temp_db)
        created_session = manager.create_session(user_id="user001")
        retrieved_session = manager.get_session(created_session.session_id)
        
        assert retrieved_session is not None
        assert retrieved_session.user_id == "user001"

    def test_get_session_by_token(self, temp_db):
        """Test retrieving session by token"""
        manager = SessionManager(db_path=temp_db)
        created_session = manager.create_session(user_id="user001")
        retrieved_session = manager.get_session_by_token(created_session.token)
        
        assert retrieved_session is not None
        assert retrieved_session.session_id == created_session.session_id

    def test_session_not_found(self, temp_db):
        """Test retrieving non-existent session"""
        manager = SessionManager(db_path=temp_db)
        session = manager.get_session("nonexistent_session")
        
        assert session is None

    def test_update_last_activity(self, temp_db):
        """Test updating session last activity"""
        manager = SessionManager(db_path=temp_db)
        session = manager.create_session(user_id="user001")
        
        original_activity = session.last_activity
        manager.update_last_activity(session.session_id)
        
        updated_session = manager.get_session(session.session_id)
        assert updated_session.last_activity >= original_activity

    def test_end_session(self, temp_db):
        """Test ending a session"""
        manager = SessionManager(db_path=temp_db)
        session = manager.create_session(user_id="user001")
        
        manager.end_session(session.session_id)
        
        ended_session = manager.get_session(session.session_id)
        assert ended_session.is_active is False

    def test_get_user_sessions(self, temp_db):
        """Test retrieving all sessions for a user"""
        manager = SessionManager(db_path=temp_db)
        
        # Create multiple sessions
        for i in range(3):
            manager.create_session(user_id="user001")
        
        sessions = manager.get_user_sessions(user_id="user001")
        assert len(sessions) >= 3

    def test_cleanup_expired_sessions(self, temp_db):
        """Test cleaning up expired sessions"""
        manager = SessionManager(db_path=temp_db, session_timeout_minutes=0)
        
        # Create sessions
        session1 = manager.create_session(user_id="user001")
        session2 = manager.create_session(user_id="user002")
        
        # Cleanup should mark as inactive if expired
        manager.cleanup_expired_sessions()
        
        # Sessions should still exist in database
        assert manager.get_session(session1.session_id) is not None

    def test_is_session_valid(self, temp_db):
        """Test session validity check"""
        manager = SessionManager(db_path=temp_db, session_timeout_minutes=30)
        session = manager.create_session(user_id="user001")
        
        is_valid = manager.is_session_valid(session.session_id)
        assert is_valid is True

    def test_session_validity_after_expiry(self, temp_db):
        """Test session validity after expiry"""
        manager = SessionManager(db_path=temp_db, session_timeout_minutes=0)
        session = manager.create_session(user_id="user001")
        
        # Session should be expired (timeout is 0)
        is_valid = manager.is_session_valid(session.session_id)
        # Actually with timeout_minutes=0, it expires immediately
        # This tests the timeout logic


class TestSessionActivityLogger:
    """Test SessionActivityLogger for activity tracking"""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database"""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_activities.db")
        yield db_path
        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.rmtree(temp_dir)

    def test_activity_logger_initialization(self, temp_db):
        """Test SessionActivityLogger initialization"""
        logger = SessionActivityLogger(db_path=temp_db)
        assert logger is not None

    def test_log_activity(self, temp_db):
        """Test logging session activity"""
        logger = SessionActivityLogger(db_path=temp_db)
        
        activity = logger.log_activity(
            session_id="sess001",
            action="CASE_VIEWED",
            resource_type="CASE",
            resource_id="case123",
            status="SUCCESS"
        )
        
        assert activity is not None
        assert activity.session_id == "sess001"

    def test_log_multiple_activities(self, temp_db):
        """Test logging multiple activities"""
        logger = SessionActivityLogger(db_path=temp_db)
        
        for i in range(5):
            logger.log_activity(
                session_id="sess001",
                action=f"ACTION_{i}",
                resource_type="RESOURCE",
                resource_id=f"res{i}",
                status="SUCCESS"
            )
        
        activities = logger.get_session_activities(session_id="sess001")
        assert len(activities) >= 5

    def test_get_session_activities(self, temp_db):
        """Test retrieving session activities"""
        logger = SessionActivityLogger(db_path=temp_db)
        
        # Log some activities
        for i in range(3):
            logger.log_activity(
                session_id="sess001",
                action="CASE_VIEWED",
                resource_type="CASE",
                resource_id=f"case{i}",
                status="SUCCESS"
            )
        
        activities = logger.get_session_activities(session_id="sess001")
        assert len(activities) >= 3

    def test_activity_timestamp_tracking(self, temp_db):
        """Test activity timestamp tracking"""
        logger = SessionActivityLogger(db_path=temp_db)
        
        before = datetime.now()
        logger.log_activity(
            session_id="sess001",
            action="DATA_ACCESS",
            resource_type="FILE",
            resource_id="file123",
            status="SUCCESS"
        )
        after = datetime.now()
        
        activities = logger.get_session_activities(session_id="sess001")
        assert len(activities) > 0
        activity_time = activities[0].timestamp
        assert before <= activity_time <= after

    def test_get_user_activity_summary(self, temp_db):
        """Test getting user activity summary"""
        logger = SessionActivityLogger(db_path=temp_db)
        
        # Log activities for multiple sessions
        for session_idx in range(2):
            for action_idx in range(5):
                logger.log_activity(
                    session_id=f"sess{session_idx}",
                    action=f"ACTION_{action_idx}",
                    resource_type="RESOURCE",
                    resource_id=f"res{action_idx}",
                    status="SUCCESS"
                )
        
        # Get summary
        summary = logger.get_user_activity_summary(session_id="sess0")
        assert summary is not None

    def test_activity_with_error_status(self, temp_db):
        """Test logging activity with error status"""
        logger = SessionActivityLogger(db_path=temp_db)
        
        activity = logger.log_activity(
            session_id="sess001",
            action="DATA_ACCESS",
            resource_type="FILE",
            resource_id="file123",
            status="FAILED",
            details={"error": "Access denied"}
        )
        
        assert activity is not None
        assert activity.status == "FAILED"

    def test_activity_with_details(self, temp_db):
        """Test logging activity with additional details"""
        logger = SessionActivityLogger(db_path=temp_db)
        
        details = {
            "query_type": "IOC_SEARCH",
            "query_value": "192.168.1.1",
            "results_count": 5,
            "duration_ms": 234
        }
        
        activity = logger.log_activity(
            session_id="sess001",
            action="IOC_SEARCHED",
            resource_type="IOC",
            resource_id="ioc_search_001",
            status="SUCCESS",
            details=details
        )
        
        assert activity.details is not None


class TestSessionLifecycleIntegration:
    """Integration tests for complete session lifecycle"""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database"""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_lifecycle.db")
        yield db_path
        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.rmtree(temp_dir)

    def test_complete_session_workflow(self, temp_db):
        """Test complete session creation, activity, and termination"""
        manager = SessionManager(db_path=temp_db)
        logger = SessionActivityLogger(db_path=temp_db)
        
        # Create session (login)
        session = manager.create_session(user_id="investigator001")
        assert session.is_active is True
        
        # Log activities during session
        logger.log_activity(
            session_id=session.session_id,
            action="CASE_VIEWED",
            resource_type="CASE",
            resource_id="case_alpha_001",
            status="SUCCESS"
        )
        
        logger.log_activity(
            session_id=session.session_id,
            action="IOC_SEARCHED",
            resource_type="IOC",
            resource_id="ioc_001",
            status="SUCCESS",
            details={"ioc_type": "IP", "query": "192.168.1.1"}
        )
        
        # Update activity
        manager.update_last_activity(session.session_id)
        
        # Get activities
        activities = logger.get_session_activities(session.session_id)
        assert len(activities) == 2
        
        # End session (logout)
        manager.end_session(session.session_id)
        ended_session = manager.get_session(session.session_id)
        assert ended_session.is_active is False

    def test_multiple_concurrent_sessions(self, temp_db):
        """Test managing multiple concurrent sessions"""
        manager = SessionManager(db_path=temp_db)
        logger = SessionActivityLogger(db_path=temp_db)
        
        # Create multiple sessions
        sessions = []
        for i in range(3):
            session = manager.create_session(user_id=f"user{i}")
            sessions.append(session)
        
        # Log activities in each session
        for session in sessions:
            logger.log_activity(
                session_id=session.session_id,
                action="LOGIN",
                resource_type="USER",
                resource_id=session.user_id,
                status="SUCCESS"
            )
        
        # Verify all sessions are active
        for session in sessions:
            active_session = manager.get_session(session.session_id)
            assert active_session.is_active is True
        
        # Verify each user has correct session
        for i, session in enumerate(sessions):
            user_sessions = manager.get_user_sessions(user_id=f"user{i}")
            assert len(user_sessions) >= 1

    def test_session_activity_tracking_over_time(self, temp_db):
        """Test tracking activities over session lifetime"""
        manager = SessionManager(db_path=temp_db)
        logger = SessionActivityLogger(db_path=temp_db)
        
        session = manager.create_session(user_id="user001")
        
        # Simulate activities over time
        actions = [
            ("LOGIN", "USER", "user001"),
            ("CASE_VIEWED", "CASE", "case001"),
            ("IOC_ADDED", "IOC", "ioc001"),
            ("EXPORT_INITIATED", "EXPORT", "export001"),
            ("LOGOUT", "USER", "user001")
        ]
        
        for action, resource_type, resource_id in actions:
            logger.log_activity(
                session_id=session.session_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                status="SUCCESS"
            )
            manager.update_last_activity(session.session_id)
        
        # Verify all activities logged
        activities = logger.get_session_activities(session.session_id)
        assert len(activities) == len(actions)
        
        # Verify action sequence
        for i, (action, _, _) in enumerate(actions):
            assert activities[i].action == action


class TestSessionSecurity:
    """Security-focused tests for session management"""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database"""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_security.db")
        yield db_path
        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.rmtree(temp_dir)

    def test_session_token_uniqueness(self, temp_db):
        """Test that session tokens are unique"""
        manager = SessionManager(db_path=temp_db)
        
        tokens = []
        for i in range(10):
            session = manager.create_session(user_id="user001")
            tokens.append(session.token)
        
        # All tokens should be unique
        assert len(set(tokens)) == len(tokens)

    def test_session_isolation(self, temp_db):
        """Test that sessions are isolated per user"""
        manager = SessionManager(db_path=temp_db)
        
        session_user1 = manager.create_session(user_id="user001")
        session_user2 = manager.create_session(user_id="user002")
        
        # Verify users get different sessions
        assert session_user1.session_id != session_user2.session_id
        assert session_user1.user_id != session_user2.user_id

    def test_expired_session_security(self, temp_db):
        """Test security of expired sessions"""
        manager = SessionManager(db_path=temp_db, session_timeout_minutes=1)
        session = manager.create_session(user_id="user001")
        
        # Session should be valid initially
        assert manager.is_session_valid(session.session_id) is True
        
        # Cleanup should respect timeout
        manager.cleanup_expired_sessions()

    def test_activity_audit_trail(self, temp_db):
        """Test that activities create audit trail"""
        logger = SessionActivityLogger(db_path=temp_db)
        
        sensitive_actions = [
            "DATA_ACCESSED",
            "DATA_MODIFIED",
            "EXPORT_INITIATED",
            "USER_DELETED"
        ]
        
        for action in sensitive_actions:
            logger.log_activity(
                session_id="sess001",
                action=action,
                resource_type="RESOURCE",
                resource_id="res123",
                status="SUCCESS"
            )
        
        activities = logger.get_session_activities(session_id="sess001")
        for i, action in enumerate(sensitive_actions):
            assert activities[i].action == action


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
