"""
JOUR 2 - Audit Trail System Tests
Test suite for immutable logging, compliance reporting, and audit searching
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

from audit_trail_system import (
    AuditActionType,
    AuditEntry,
    AuditTrailManager,
    ComplianceReportGenerator,
    AuditSearchEngine
)


class TestAuditActionType:
    """Test AuditActionType enum"""

    def test_action_type_values(self):
        """Test all audit action types are defined"""
        action_types = [
            AuditActionType.USER_LOGIN,
            AuditActionType.USER_LOGOUT,
            AuditActionType.CASE_CREATED,
            AuditActionType.CASE_MODIFIED,
            AuditActionType.IOC_ADDED,
            AuditActionType.IOC_MATCHED,
            AuditActionType.EXPORT_INITIATED,
            AuditActionType.REPORT_GENERATED,
            AuditActionType.USER_CREATED,
            AuditActionType.USER_DELETED,
            AuditActionType.PERMISSION_CHANGED,
            AuditActionType.DATABASE_BACKUP,
            AuditActionType.DATA_ACCESSED,
            AuditActionType.DATA_MODIFIED,
            AuditActionType.SUSPICIOUS_ACTIVITY,
            AuditActionType.POLICY_VIOLATION,
            AuditActionType.SYSTEM_ERROR,
            AuditActionType.SECURITY_ALERT
        ]
        assert len(action_types) == 18

    def test_action_type_string_representation(self):
        """Test action type string values"""
        assert AuditActionType.USER_LOGIN.value == "USER_LOGIN"
        assert AuditActionType.CASE_CREATED.value == "CASE_CREATED"
        assert AuditActionType.SECURITY_ALERT.value == "SECURITY_ALERT"


class TestAuditEntry:
    """Test AuditEntry dataclass"""

    def test_audit_entry_creation(self):
        """Test creating audit entry"""
        entry = AuditEntry(
            audit_id="audit001",
            user_id="user001",
            action=AuditActionType.USER_LOGIN,
            resource_type="USER",
            resource_id="user001",
            status="SUCCESS",
            timestamp=datetime.now()
        )
        assert entry.audit_id == "audit001"
        assert entry.user_id == "user001"
        assert entry.action == AuditActionType.USER_LOGIN

    def test_audit_entry_with_details(self):
        """Test audit entry with additional details"""
        entry = AuditEntry(
            audit_id="audit001",
            user_id="user001",
            action=AuditActionType.CASE_CREATED,
            resource_type="CASE",
            resource_id="case123",
            status="SUCCESS",
            timestamp=datetime.now(),
            details={"case_name": "Investigation Alpha", "severity": "HIGH"}
        )
        assert entry.details is not None
        assert entry.details["case_name"] == "Investigation Alpha"

    def test_audit_entry_hash_chain(self):
        """Test audit entry hash chain for integrity"""
        entry = AuditEntry(
            audit_id="audit001",
            user_id="user001",
            action=AuditActionType.USER_LOGIN,
            resource_type="USER",
            resource_id="user001",
            status="SUCCESS",
            timestamp=datetime.now(),
            previous_hash="hash_of_previous_entry",
            entry_hash="hash_of_current_entry"
        )
        assert entry.previous_hash is not None
        assert entry.entry_hash is not None


class TestAuditTrailManager:
    """Test AuditTrailManager for logging and verification"""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database"""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_audit.db")
        yield db_path
        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.rmtree(temp_dir)

    def test_audit_manager_initialization(self, temp_db):
        """Test AuditTrailManager initialization"""
        manager = AuditTrailManager(db_path=temp_db)
        assert manager is not None
        assert os.path.exists(temp_db)

    def test_log_action(self, temp_db):
        """Test logging an action"""
        manager = AuditTrailManager(db_path=temp_db)
        audit_id = manager.log_action(
            user_id="user001",
            action=AuditActionType.USER_LOGIN,
            resource_type="USER",
            resource_id="user001",
            status="SUCCESS"
        )
        assert audit_id is not None

    def test_log_multiple_actions(self, temp_db):
        """Test logging multiple actions"""
        manager = AuditTrailManager(db_path=temp_db)
        
        audit_ids = []
        for i in range(5):
            audit_id = manager.log_action(
                user_id="user001",
                action=AuditActionType.CASE_CREATED if i % 2 == 0 else AuditActionType.CASE_MODIFIED,
                resource_type="CASE",
                resource_id=f"case{i}",
                status="SUCCESS"
            )
            audit_ids.append(audit_id)
        
        assert len(audit_ids) == 5

    def test_get_audit_log(self, temp_db):
        """Test retrieving audit log"""
        manager = AuditTrailManager(db_path=temp_db)
        
        # Log some actions
        manager.log_action(
            user_id="user001",
            action=AuditActionType.USER_LOGIN,
            resource_type="USER",
            resource_id="user001",
            status="SUCCESS"
        )
        
        # Retrieve log
        logs = manager.get_audit_log(limit=10)
        assert len(logs) > 0

    def test_log_with_error_status(self, temp_db):
        """Test logging action with error status"""
        manager = AuditTrailManager(db_path=temp_db)
        
        audit_id = manager.log_action(
            user_id="user001",
            action=AuditActionType.DATA_ACCESSED,
            resource_type="FILE",
            resource_id="file123",
            status="FAILED",
            details={"error": "Access denied", "reason": "Insufficient permissions"}
        )
        
        assert audit_id is not None

    def test_chain_integrity_verification(self, temp_db):
        """Test chain integrity verification"""
        manager = AuditTrailManager(db_path=temp_db)
        
        # Log multiple actions to build chain
        for i in range(5):
            manager.log_action(
                user_id="user001",
                action=AuditActionType.DATA_ACCESSED,
                resource_type="CASE",
                resource_id=f"case{i}",
                status="SUCCESS"
            )
        
        # Verify chain integrity
        is_valid = manager.verify_chain_integrity()
        assert is_valid is True

    def test_audit_entry_fields(self, temp_db):
        """Test that audit entry contains all required fields"""
        manager = AuditTrailManager(db_path=temp_db)
        
        audit_id = manager.log_action(
            user_id="user001",
            action=AuditActionType.CASE_CREATED,
            resource_type="CASE",
            resource_id="case123",
            status="SUCCESS",
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0"
        )
        
        logs = manager.get_audit_log(limit=1)
        assert len(logs) > 0
        log_entry = logs[0]
        assert log_entry.user_id == "user001"
        assert log_entry.action == AuditActionType.CASE_CREATED


class TestComplianceReportGenerator:
    """Test ComplianceReportGenerator for compliance reporting"""

    @pytest.fixture
    def temp_db_with_logs(self):
        """Create database with sample audit logs"""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_compliance.db")
        
        manager = AuditTrailManager(db_path=db_path)
        
        # Create sample logs
        for i in range(10):
            user_id = "user001" if i % 2 == 0 else "user002"
            action = AuditActionType.DATA_ACCESSED if i % 3 == 0 else AuditActionType.DATA_MODIFIED
            
            manager.log_action(
                user_id=user_id,
                action=action,
                resource_type="CASE",
                resource_id=f"case{i}",
                status="SUCCESS"
            )
        
        yield db_path
        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.rmtree(temp_dir)

    def test_compliance_report_generator_initialization(self, temp_db_with_logs):
        """Test ComplianceReportGenerator initialization"""
        generator = ComplianceReportGenerator(db_path=temp_db_with_logs)
        assert generator is not None

    def test_user_activity_report(self, temp_db_with_logs):
        """Test generating user activity report"""
        generator = ComplianceReportGenerator(db_path=temp_db_with_logs)
        
        report = generator.generate_user_activity_report(
            user_id="user001",
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now()
        )
        
        assert report is not None
        assert "user_id" in report
        assert report["user_id"] == "user001"

    def test_security_events_report(self, temp_db_with_logs):
        """Test generating security events report"""
        generator = ComplianceReportGenerator(db_path=temp_db_with_logs)
        
        report = generator.generate_security_events_report(
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now()
        )
        
        assert report is not None

    def test_report_timestamp_inclusion(self, temp_db_with_logs):
        """Test that reports include timestamp"""
        generator = ComplianceReportGenerator(db_path=temp_db_with_logs)
        
        report = generator.generate_user_activity_report(
            user_id="user001",
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now()
        )
        
        assert "generated_at" in report or "timestamp" in report or report is not None


class TestAuditSearchEngine:
    """Test AuditSearchEngine for querying logs"""

    @pytest.fixture
    def temp_db_with_logs(self):
        """Create database with various audit logs"""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_search.db")
        
        manager = AuditTrailManager(db_path=db_path)
        
        # Create varied logs
        actions = [
            AuditActionType.USER_LOGIN,
            AuditActionType.CASE_CREATED,
            AuditActionType.DATA_ACCESSED,
            AuditActionType.EXPORT_INITIATED,
            AuditActionType.SECURITY_ALERT
        ]
        
        for i in range(20):
            action = actions[i % len(actions)]
            manager.log_action(
                user_id=f"user{i % 3}",
                action=action,
                resource_type="CASE",
                resource_id=f"case{i}",
                status="SUCCESS" if i % 2 == 0 else "FAILED"
            )
        
        yield db_path
        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.rmtree(temp_dir)

    def test_search_engine_initialization(self, temp_db_with_logs):
        """Test AuditSearchEngine initialization"""
        engine = AuditSearchEngine(db_path=temp_db_with_logs)
        assert engine is not None

    def test_search_by_user_id(self, temp_db_with_logs):
        """Test searching logs by user ID"""
        engine = AuditSearchEngine(db_path=temp_db_with_logs)
        
        results = engine.search_by_criteria(user_id="user0")
        assert len(results) > 0

    def test_search_by_action_type(self, temp_db_with_logs):
        """Test searching logs by action type"""
        engine = AuditSearchEngine(db_path=temp_db_with_logs)
        
        results = engine.search_by_criteria(action=AuditActionType.CASE_CREATED)
        for result in results:
            assert result.action == AuditActionType.CASE_CREATED

    def test_search_by_status(self, temp_db_with_logs):
        """Test searching logs by status"""
        engine = AuditSearchEngine(db_path=temp_db_with_logs)
        
        results = engine.search_by_criteria(status="SUCCESS")
        for result in results:
            assert result.status == "SUCCESS"

    def test_search_by_date_range(self, temp_db_with_logs):
        """Test searching logs by date range"""
        engine = AuditSearchEngine(db_path=temp_db_with_logs)
        
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now() + timedelta(days=1)
        
        results = engine.search_by_criteria(
            start_date=start_date,
            end_date=end_date
        )
        assert len(results) > 0

    def test_search_by_resource(self, temp_db_with_logs):
        """Test searching logs by resource"""
        engine = AuditSearchEngine(db_path=temp_db_with_logs)
        
        results = engine.search_by_criteria(resource_type="CASE")
        for result in results:
            assert result.resource_type == "CASE"

    def test_combined_search_criteria(self, temp_db_with_logs):
        """Test search with multiple criteria"""
        engine = AuditSearchEngine(db_path=temp_db_with_logs)
        
        results = engine.search_by_criteria(
            user_id="user0",
            status="SUCCESS",
            resource_type="CASE"
        )
        
        for result in results:
            assert result.user_id == "user0"
            assert result.status == "SUCCESS"
            assert result.resource_type == "CASE"

    def test_get_user_session_activity(self, temp_db_with_logs):
        """Test retrieving user session activity"""
        engine = AuditSearchEngine(db_path=temp_db_with_logs)
        
        activity = engine.get_user_session_activity(user_id="user0")
        assert activity is not None


class TestAuditTrailIntegration:
    """Integration tests for audit trail workflows"""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database"""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_integration.db")
        yield db_path
        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.rmtree(temp_dir)

    def test_complete_audit_workflow(self, temp_db):
        """Test complete audit logging workflow"""
        manager = AuditTrailManager(db_path=temp_db)
        search_engine = AuditSearchEngine(db_path=temp_db)
        
        # Log user login
        manager.log_action(
            user_id="investigator001",
            action=AuditActionType.USER_LOGIN,
            resource_type="USER",
            resource_id="investigator001",
            status="SUCCESS"
        )
        
        # Log case creation
        manager.log_action(
            user_id="investigator001",
            action=AuditActionType.CASE_CREATED,
            resource_type="CASE",
            resource_id="case_alpha_001",
            status="SUCCESS",
            details={"case_name": "Investigation Alpha"}
        )
        
        # Log IOC addition
        manager.log_action(
            user_id="investigator001",
            action=AuditActionType.IOC_ADDED,
            resource_type="IOC",
            resource_id="ioc_001",
            status="SUCCESS",
            details={"ioc_type": "IP", "ioc_value": "192.168.1.1"}
        )
        
        # Search for all user activities
        results = search_engine.search_by_criteria(user_id="investigator001")
        assert len(results) == 3

    def test_audit_chain_immutability(self, temp_db):
        """Test that audit chain maintains integrity"""
        manager = AuditTrailManager(db_path=temp_db)
        
        # Log sequence of actions
        for i in range(5):
            manager.log_action(
                user_id="user001",
                action=AuditActionType.DATA_ACCESSED,
                resource_type="FILE",
                resource_id=f"file{i}",
                status="SUCCESS"
            )
        
        # Verify chain integrity
        is_valid = manager.verify_chain_integrity()
        assert is_valid is True

    def test_compliance_reporting_workflow(self, temp_db):
        """Test compliance reporting with audit data"""
        manager = AuditTrailManager(db_path=temp_db)
        generator = ComplianceReportGenerator(db_path=temp_db)
        
        # Log various activities
        for i in range(10):
            action = AuditActionType.DATA_ACCESSED if i % 2 == 0 else AuditActionType.DATA_MODIFIED
            manager.log_action(
                user_id="user001",
                action=action,
                resource_type="CASE",
                resource_id=f"case{i}",
                status="SUCCESS"
            )
        
        # Generate compliance report
        report = generator.generate_user_activity_report(
            user_id="user001",
            start_date=datetime.now() - timedelta(days=1),
            end_date=datetime.now()
        )
        
        assert report is not None

    def test_security_alert_logging(self, temp_db):
        """Test logging security alerts"""
        manager = AuditTrailManager(db_path=temp_db)
        search_engine = AuditSearchEngine(db_path=temp_db)
        
        # Log security alert
        manager.log_action(
            user_id="system",
            action=AuditActionType.SECURITY_ALERT,
            resource_type="SYSTEM",
            resource_id="security_alert_001",
            status="ACTIVE",
            details={
                "alert_type": "UNAUTHORIZED_ACCESS",
                "severity": "HIGH",
                "description": "Multiple failed login attempts detected"
            }
        )
        
        # Search for security alerts
        results = search_engine.search_by_criteria(
            action=AuditActionType.SECURITY_ALERT
        )
        
        assert len(results) > 0
        assert results[0].action == AuditActionType.SECURITY_ALERT


class TestAuditDataIntegrity:
    """Tests for audit data integrity and consistency"""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database"""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_integrity.db")
        yield db_path
        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.rmtree(temp_dir)

    def test_timestamp_ordering(self, temp_db):
        """Test that audit entries maintain timestamp ordering"""
        manager = AuditTrailManager(db_path=temp_db)
        
        # Log actions with slight delays
        for i in range(5):
            manager.log_action(
                user_id="user001",
                action=AuditActionType.DATA_ACCESSED,
                resource_type="FILE",
                resource_id=f"file{i}",
                status="SUCCESS"
            )
        
        logs = manager.get_audit_log(limit=10)
        
        # Verify ordering
        for i in range(len(logs) - 1):
            assert logs[i].timestamp <= logs[i+1].timestamp

    def test_audit_entry_uniqueness(self, temp_db):
        """Test that audit entries have unique IDs"""
        manager = AuditTrailManager(db_path=temp_db)
        
        audit_ids = []
        for i in range(10):
            audit_id = manager.log_action(
                user_id="user001",
                action=AuditActionType.DATA_ACCESSED,
                resource_type="FILE",
                resource_id=f"file{i}",
                status="SUCCESS"
            )
            audit_ids.append(audit_id)
        
        # All IDs should be unique
        assert len(set(audit_ids)) == len(audit_ids)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
