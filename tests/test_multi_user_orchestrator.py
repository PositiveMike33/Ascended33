"""
JOUR 2 - Multi-user Orchestrator Module Tests
Test suite for UserManager, authentication, quotas, and Docker isolation
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

from multi_user_orchestrator import (
    UserProfile,
    UserSession,
    UserQuota,
    UserManager,
    UserAuthenticationHandler,
    UserConfigGenerator,
    UserQuotaManager,
    DockerUserIsolation,
    UserRole
)


class TestUserProfile:
    """Test UserProfile dataclass"""

    def test_user_profile_creation(self):
        """Test creating a user profile"""
        profile = UserProfile(
            user_id="user001",
            username="testuser",
            email="test@example.com",
            role=UserRole.INVESTIGATOR,
            created_at=datetime.now()
        )
        assert profile.user_id == "user001"
        assert profile.username == "testuser"
        assert profile.email == "test@example.com"
        assert profile.role == UserRole.INVESTIGATOR

    def test_user_profile_roles(self):
        """Test different user roles"""
        admin_profile = UserProfile(
            user_id="admin001",
            username="admin",
            email="admin@example.com",
            role=UserRole.ADMIN,
            created_at=datetime.now()
        )
        assert admin_profile.role == UserRole.ADMIN


class TestUserSession:
    """Test UserSession dataclass"""

    def test_user_session_creation(self):
        """Test creating a user session"""
        session = UserSession(
            session_id="sess001",
            user_id="user001",
            token="token_abc123",
            created_at=datetime.now(),
            last_activity=datetime.now(),
            is_active=True
        )
        assert session.session_id == "sess001"
        assert session.user_id == "user001"
        assert session.is_active is True

    def test_user_session_expiry(self):
        """Test session expiry calculation"""
        created = datetime.now() - timedelta(hours=1)
        session = UserSession(
            session_id="sess001",
            user_id="user001",
            token="token_abc123",
            created_at=created,
            last_activity=created,
            is_active=True
        )
        assert session.created_at < datetime.now()


class TestUserQuota:
    """Test UserQuota dataclass"""

    def test_user_quota_creation(self):
        """Test creating user quota"""
        quota = UserQuota(
            user_id="user001",
            max_cases=10,
            max_storage_gb=100,
            max_api_calls_per_day=1000,
            max_concurrent_exports=5
        )
        assert quota.max_cases == 10
        assert quota.max_storage_gb == 100
        assert quota.max_api_calls_per_day == 1000
        assert quota.max_concurrent_exports == 5

    def test_quota_tracking_values(self):
        """Test quota usage tracking"""
        quota = UserQuota(
            user_id="user001",
            max_cases=10,
            max_storage_gb=100,
            max_api_calls_per_day=1000,
            max_concurrent_exports=5,
            current_cases=2,
            current_storage_gb=25.5,
            current_api_calls=500
        )
        assert quota.current_cases == 2
        assert quota.current_storage_gb == 25.5
        assert quota.current_api_calls == 500


class TestUserAuthenticationHandler:
    """Test UserAuthenticationHandler"""

    def test_hash_password(self):
        """Test password hashing"""
        password = "SecurePassword123!"
        hashed = UserAuthenticationHandler.hash_password(password)
        assert hashed != password
        assert len(hashed) > 0

    def test_verify_password_success(self):
        """Test password verification success"""
        password = "SecurePassword123!"
        hashed = UserAuthenticationHandler.hash_password(password)
        is_valid = UserAuthenticationHandler.verify_password(password, hashed)
        assert is_valid is True

    def test_verify_password_failure(self):
        """Test password verification failure"""
        password = "SecurePassword123!"
        wrong_password = "WrongPassword123!"
        hashed = UserAuthenticationHandler.hash_password(password)
        is_valid = UserAuthenticationHandler.verify_password(wrong_password, hashed)
        assert is_valid is False

    def test_generate_api_key(self):
        """Test API key generation"""
        api_key = UserAuthenticationHandler.generate_api_key()
        assert api_key is not None
        assert len(api_key) > 20
        assert isinstance(api_key, str)

    def test_generate_multiple_api_keys_are_unique(self):
        """Test that generated API keys are unique"""
        key1 = UserAuthenticationHandler.generate_api_key()
        key2 = UserAuthenticationHandler.generate_api_key()
        assert key1 != key2


class TestUserManager:
    """Test UserManager database operations"""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing"""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_users.db")
        yield db_path
        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.rmtree(temp_dir)

    def test_user_manager_initialization(self, temp_db):
        """Test UserManager initialization"""
        manager = UserManager(db_path=temp_db)
        assert manager is not None
        assert os.path.exists(temp_db)

    def test_create_user(self, temp_db):
        """Test user creation"""
        manager = UserManager(db_path=temp_db)
        result = manager.create_user(
            username="testuser",
            email="test@example.com",
            password="SecurePass123!",
            role=UserRole.INVESTIGATOR
        )
        assert result is not None
        assert result.username == "testuser"
        assert result.email == "test@example.com"

    def test_get_user(self, temp_db):
        """Test retrieving user"""
        manager = UserManager(db_path=temp_db)
        user = manager.create_user(
            username="testuser",
            email="test@example.com",
            password="SecurePass123!",
            role=UserRole.INVESTIGATOR
        )
        retrieved = manager.get_user(user.user_id)
        assert retrieved is not None
        assert retrieved.username == "testuser"

    def test_get_user_by_username(self, temp_db):
        """Test retrieving user by username"""
        manager = UserManager(db_path=temp_db)
        manager.create_user(
            username="testuser",
            email="test@example.com",
            password="SecurePass123!",
            role=UserRole.INVESTIGATOR
        )
        retrieved = manager.get_user_by_username("testuser")
        assert retrieved is not None
        assert retrieved.username == "testuser"

    def test_user_not_found(self, temp_db):
        """Test retrieving non-existent user"""
        manager = UserManager(db_path=temp_db)
        retrieved = manager.get_user("nonexistent")
        assert retrieved is None

    def test_list_users(self, temp_db):
        """Test listing all users"""
        manager = UserManager(db_path=temp_db)
        manager.create_user(
            username="user1",
            email="user1@example.com",
            password="Pass1",
            role=UserRole.INVESTIGATOR
        )
        manager.create_user(
            username="user2",
            email="user2@example.com",
            password="Pass2",
            role=UserRole.ANALYST
        )
        users = manager.list_users()
        assert len(users) >= 2

    def test_update_user(self, temp_db):
        """Test updating user"""
        manager = UserManager(db_path=temp_db)
        user = manager.create_user(
            username="testuser",
            email="test@example.com",
            password="Pass123",
            role=UserRole.INVESTIGATOR
        )
        manager.update_user(user.user_id, email="newemail@example.com")
        updated = manager.get_user(user.user_id)
        assert updated.email == "newemail@example.com"

    def test_delete_user(self, temp_db):
        """Test deleting user"""
        manager = UserManager(db_path=temp_db)
        user = manager.create_user(
            username="testuser",
            email="test@example.com",
            password="Pass123",
            role=UserRole.INVESTIGATOR
        )
        manager.delete_user(user.user_id)
        retrieved = manager.get_user(user.user_id)
        assert retrieved is None


class TestUserQuotaManager:
    """Test UserQuotaManager"""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database"""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_quotas.db")
        yield db_path
        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.rmtree(temp_dir)

    def test_quota_manager_initialization(self, temp_db):
        """Test QuotaManager initialization"""
        manager = UserQuotaManager(db_path=temp_db)
        assert manager is not None

    def test_check_quota_within_limits(self, temp_db):
        """Test quota checking within limits"""
        manager = UserQuotaManager(db_path=temp_db)
        manager.set_user_quota(
            user_id="user001",
            max_cases=10,
            max_storage_gb=100,
            max_api_calls_per_day=1000
        )
        result = manager.check_quota("user001", "cases", 5)
        assert result is True

    def test_check_quota_exceeds_limits(self, temp_db):
        """Test quota checking exceeds limits"""
        manager = UserQuotaManager(db_path=temp_db)
        manager.set_user_quota(
            user_id="user001",
            max_cases=10,
            max_storage_gb=100,
            max_api_calls_per_day=1000
        )
        result = manager.check_quota("user001", "cases", 15)
        assert result is False

    def test_increment_usage(self, temp_db):
        """Test incrementing usage"""
        manager = UserQuotaManager(db_path=temp_db)
        manager.set_user_quota(
            user_id="user001",
            max_cases=10,
            max_storage_gb=100,
            max_api_calls_per_day=1000
        )
        manager.increment_usage("user001", "cases", 3)
        quota = manager.get_user_quota("user001")
        assert quota.current_cases == 3


class TestUserConfigGenerator:
    """Test UserConfigGenerator"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_generate_user_config(self, temp_dir):
        """Test generating user configuration"""
        generator = UserConfigGenerator(config_dir=temp_dir)
        config = generator.generate_user_config(
            user_id="user001",
            username="testuser",
            role=UserRole.INVESTIGATOR
        )
        assert config is not None
        assert config["user_id"] == "user001"
        assert config["username"] == "testuser"
        assert config["role"] == "investigator"

    def test_save_user_config(self, temp_dir):
        """Test saving user configuration"""
        generator = UserConfigGenerator(config_dir=temp_dir)
        config = generator.generate_user_config(
            user_id="user001",
            username="testuser",
            role=UserRole.INVESTIGATOR
        )
        config_path = generator.save_user_config("user001", config)
        assert os.path.exists(config_path)


class TestDockerUserIsolation:
    """Test DockerUserIsolation"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_generate_dockerfile(self, temp_dir):
        """Test generating Dockerfile"""
        isolation = DockerUserIsolation(output_dir=temp_dir)
        dockerfile = isolation.generate_dockerfile(
            user_id="user001",
            memory_limit="2g",
            cpu_limit="2"
        )
        assert dockerfile is not None
        assert "FROM python:3.11" in dockerfile
        assert "user001" in dockerfile

    def test_generate_docker_compose(self, temp_dir):
        """Test generating docker-compose configuration"""
        isolation = DockerUserIsolation(output_dir=temp_dir)
        compose_config = isolation.generate_docker_compose(
            users=[
                {"user_id": "user001", "memory_limit": "2g", "cpu_limit": "2"},
                {"user_id": "user002", "memory_limit": "1g", "cpu_limit": "1"}
            ]
        )
        assert compose_config is not None
        assert "services" in compose_config
        assert "user001" in compose_config
        assert "user002" in compose_config


class TestMultiUserIntegration:
    """Integration tests for multi-user orchestrator"""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database"""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_integration.db")
        yield db_path
        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.rmtree(temp_dir)

    def test_complete_user_lifecycle(self, temp_db):
        """Test complete user creation, authentication, and quota workflow"""
        manager = UserManager(db_path=temp_db)
        quota_manager = UserQuotaManager(db_path=temp_db)

        # Create user
        user = manager.create_user(
            username="investigator",
            email="investigator@example.com",
            password="SecurePass123!",
            role=UserRole.INVESTIGATOR
        )
        assert user is not None

        # Verify password
        retrieved = manager.get_user_by_username("investigator")
        password_valid = UserAuthenticationHandler.verify_password(
            "SecurePass123!",
            retrieved.password_hash
        )
        assert password_valid is True

        # Set quotas
        quota_manager.set_user_quota(
            user_id=user.user_id,
            max_cases=20,
            max_storage_gb=50,
            max_api_calls_per_day=2000
        )

        # Check quotas
        can_create_case = quota_manager.check_quota(user.user_id, "cases", 5)
        assert can_create_case is True

        # Increment usage
        quota_manager.increment_usage(user.user_id, "cases", 5)
        quota = quota_manager.get_user_quota(user.user_id)
        assert quota.current_cases == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
