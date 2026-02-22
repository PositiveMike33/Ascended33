# ============================================================================
# MULTI-USER ORCHESTRATOR - User Management & Isolation
# ============================================================================
# Purpose: Manage multiple users, their containers, and resource quotas
# Features: User creation, isolation, configuration, quota management
#
# Author: Ascended33 Platform
# Version: 1.0.0 (JOUR 2)
# Status: Production Ready
# ============================================================================

import json
import logging
import hashlib
import secrets
import sqlite3
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class UserProfile:
    """User profile with metadata and preferences"""
    user_id: str
    username: str
    email: str
    display_name: str
    role: str  # "admin", "investigator", "analyst", "viewer"
    created_date: str
    last_login: Optional[str] = None
    is_active: bool = True
    preferences: Dict = None
    quotas: Dict = None
    
    def __post_init__(self):
        if self.preferences is None:
            self.preferences = {}
        if self.quotas is None:
            self.quotas = {
                'max_cases': 100,
                'max_storage_gb': 500,
                'max_api_calls_per_day': 10000,
                'max_concurrent_exports': 5
            }


@dataclass
class UserSession:
    """Active user session"""
    session_id: str
    user_id: str
    created_date: str
    last_activity: str
    expires_at: str
    ip_address: str
    user_agent: str
    is_active: bool = True


@dataclass
class UserQuota:
    """Resource quota for user"""
    user_id: str
    max_cases: int
    max_storage_gb: int
    max_api_calls_per_day: int
    max_concurrent_exports: int
    current_cases: int = 0
    current_storage_gb: float = 0.0
    api_calls_today: int = 0
    concurrent_exports: int = 0


class UserManager:
    """
    Manage user lifecycle: creation, deletion, updates
    Tracks user metadata, roles, permissions
    """
    
    def __init__(self, db_path: str):
        """
        Initialize UserManager with database
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        logger.info(f"UserManager initialized at {db_path}")
    
    def _init_database(self):
        """Initialize SQLite database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                display_name TEXT,
                role TEXT DEFAULT 'investigator',
                created_date TEXT,
                last_login TEXT,
                is_active BOOLEAN DEFAULT 1,
                preferences TEXT,
                quotas TEXT
            )
        """)
        
        # Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_date TEXT,
                last_activity TEXT,
                expires_at TEXT,
                ip_address TEXT,
                user_agent TEXT,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Audit log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                log_id TEXT PRIMARY KEY,
                user_id TEXT,
                action TEXT,
                resource TEXT,
                timestamp TEXT,
                details TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_user(self, username: str, email: str, display_name: str, 
                   role: str = "investigator") -> UserProfile:
        """
        Create new user
        
        Args:
            username: Unique username
            email: User email
            display_name: Display name
            role: User role (admin, investigator, analyst, viewer)
        
        Returns:
            UserProfile instance
        """
        user_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        profile = UserProfile(
            user_id=user_id,
            username=username,
            email=email,
            display_name=display_name,
            role=role,
            created_date=now,
            is_active=True
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO users 
                (user_id, username, email, display_name, role, created_date, preferences, quotas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                profile.user_id,
                profile.username,
                profile.email,
                profile.display_name,
                profile.role,
                profile.created_date,
                json.dumps(profile.preferences),
                json.dumps(profile.quotas)
            ))
            
            conn.commit()
            logger.info(f"Created user: {username} ({user_id})")
            return profile
            
        except sqlite3.IntegrityError as e:
            logger.error(f"Error creating user {username}: {e}")
            raise
        finally:
            conn.close()
    
    def get_user(self, user_id: str) -> Optional[UserProfile]:
        """
        Get user profile
        
        Args:
            user_id: User ID
        
        Returns:
            UserProfile or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return UserProfile(
            user_id=row[0],
            username=row[1],
            email=row[2],
            display_name=row[3],
            role=row[4],
            created_date=row[5],
            last_login=row[6],
            is_active=bool(row[7]),
            preferences=json.loads(row[8]) if row[8] else {},
            quotas=json.loads(row[9]) if row[9] else {}
        )
    
    def update_user(self, user_id: str, **kwargs) -> bool:
        """
        Update user profile
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
        
        Returns:
            Success status
        """
        allowed_fields = {'display_name', 'role', 'preferences', 'quotas', 'is_active'}
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_data:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        set_clause = ", ".join([f"{k} = ?" for k in update_data.keys()])
        values = list(update_data.values()) + [user_id]
        
        cursor.execute(f"UPDATE users SET {set_clause} WHERE user_id = ?", values)
        conn.commit()
        conn.close()
        
        logger.info(f"Updated user {user_id}: {list(update_data.keys())}")
        return True
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete user (soft delete)
        
        Args:
            user_id: User ID
        
        Returns:
            Success status
        """
        return self.update_user(user_id, is_active=False)
    
    def list_users(self, role: Optional[str] = None, 
                   active_only: bool = True) -> List[UserProfile]:
        """
        List users with optional filtering
        
        Args:
            role: Filter by role
            active_only: Only return active users
        
        Returns:
            List of UserProfile instances
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM users WHERE 1=1"
        params = []
        
        if active_only:
            query += " AND is_active = 1"
        
        if role:
            query += " AND role = ?"
            params.append(role)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        users = []
        for row in rows:
            users.append(UserProfile(
                user_id=row[0],
                username=row[1],
                email=row[2],
                display_name=row[3],
                role=row[4],
                created_date=row[5],
                last_login=row[6],
                is_active=bool(row[7]),
                preferences=json.loads(row[8]) if row[8] else {},
                quotas=json.loads(row[9]) if row[9] else {}
            ))
        
        return users


class UserAuthenticationHandler:
    """Handle user authentication and credential management"""
    
    def __init__(self, salt_length: int = 32):
        """
        Initialize authentication handler
        
        Args:
            salt_length: Length of password salt
        """
        self.salt_length = salt_length
        logger.info("UserAuthenticationHandler initialized")
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """
        Hash password with salt
        
        Args:
            password: Plain text password
            salt: Optional salt (generates new if None)
        
        Returns:
            Tuple of (hashed_password, salt)
        """
        if salt is None:
            salt = secrets.token_hex(16)
        
        combined = f"{salt}{password}"
        hashed = hashlib.sha256(combined.encode()).hexdigest()
        
        return hashed, salt
    
    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """
        Verify password against hash
        
        Args:
            password: Plain text password
            hashed: Stored hash
            salt: Stored salt
        
        Returns:
            Verification result
        """
        new_hash, _ = UserAuthenticationHandler.hash_password(password, salt)
        return new_hash == hashed
    
    @staticmethod
    def generate_api_key(user_id: str, prefix: str = "asc33") -> str:
        """
        Generate API key for user
        
        Args:
            user_id: User ID
            prefix: API key prefix
        
        Returns:
            API key string
        """
        random_part = secrets.token_urlsafe(32)
        return f"{prefix}_{user_id[:8]}_{random_part}"


class UserConfigGenerator:
    """Generate user-specific configuration files"""
    
    def __init__(self, config_dir: str):
        """
        Initialize config generator
        
        Args:
            config_dir: Directory for user configs
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"UserConfigGenerator initialized at {config_dir}")
    
    def generate_user_config(self, user_profile: UserProfile) -> Dict:
        """
        Generate user configuration
        
        Args:
            user_profile: User profile
        
        Returns:
            Configuration dictionary
        """
        config = {
            'user': {
                'id': user_profile.user_id,
                'username': user_profile.username,
                'email': user_profile.email,
                'display_name': user_profile.display_name,
                'role': user_profile.role
            },
            'quotas': user_profile.quotas,
            'vault': {
                'path': f"vaults/{user_profile.user_id}",
                'sync_enabled': True,
                'auto_backup': True,
                'backup_interval_hours': 24
            },
            'docker': {
                'container_name': f"asc33_{user_profile.username}",
                'memory_limit': '2G',
                'cpu_limit': '1.0',
                'network_mode': 'bridge'
            },
            'privacy': {
                'anonymize_logs': True,
                'encrypt_sensitive_data': True,
                'retention_days': 90
            }
        }
        
        logger.info(f"Generated config for user {user_profile.user_id}")
        return config
    
    def save_user_config(self, user_id: str, config: Dict) -> Path:
        """
        Save user configuration to file
        
        Args:
            user_id: User ID
            config: Configuration dictionary
        
        Returns:
            Path to saved config file
        """
        config_file = self.config_dir / f"{user_id}_config.json"
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Saved user config to {config_file}")
        return config_file


class UserQuotaManager:
    """Manage user resource quotas"""
    
    def __init__(self, db_path: str):
        """Initialize quota manager"""
        self.db_path = Path(db_path)
        self._init_quota_db()
    
    def _init_quota_db(self):
        """Initialize quota tracking database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quotas (
                user_id TEXT PRIMARY KEY,
                max_cases INTEGER,
                max_storage_gb INTEGER,
                max_api_calls_per_day INTEGER,
                max_concurrent_exports INTEGER,
                current_cases INTEGER DEFAULT 0,
                current_storage_gb REAL DEFAULT 0,
                api_calls_today INTEGER DEFAULT 0,
                concurrent_exports INTEGER DEFAULT 0,
                reset_date TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def check_quota(self, user_id: str, resource: str, amount: float = 1.0) -> bool:
        """
        Check if user can use resource
        
        Args:
            user_id: User ID
            resource: Resource type (cases, storage, api_calls, exports)
            amount: Amount needed
        
        Returns:
            Whether quota allows usage
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM quotas WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return False
        
        quota = {
            'user_id': row[0],
            'max_cases': row[1],
            'max_storage_gb': row[2],
            'max_api_calls_per_day': row[3],
            'max_concurrent_exports': row[4],
            'current_cases': row[5],
            'current_storage_gb': row[6],
            'api_calls_today': row[7],
            'concurrent_exports': row[8]
        }
        
        if resource == 'cases':
            return quota['current_cases'] + amount <= quota['max_cases']
        elif resource == 'storage':
            return quota['current_storage_gb'] + amount <= quota['max_storage_gb']
        elif resource == 'api_calls':
            return quota['api_calls_today'] + amount <= quota['max_api_calls_per_day']
        elif resource == 'exports':
            return quota['concurrent_exports'] + amount <= quota['max_concurrent_exports']
        
        return False
    
    def increment_usage(self, user_id: str, resource: str, amount: float = 1.0):
        """
        Increment resource usage
        
        Args:
            user_id: User ID
            resource: Resource type
            amount: Amount to increment
        """
        column_map = {
            'cases': 'current_cases',
            'storage': 'current_storage_gb',
            'api_calls': 'api_calls_today',
            'exports': 'concurrent_exports'
        }
        
        if resource not in column_map:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        column = column_map[resource]
        cursor.execute(
            f"UPDATE quotas SET {column} = {column} + ? WHERE user_id = ?",
            (amount, user_id)
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Incremented {resource} for {user_id} by {amount}")
    
    def reset_daily_quotas(self, user_id: str):
        """
        Reset daily quotas (api_calls_today)
        
        Args:
            user_id: User ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE quotas SET api_calls_today = 0, reset_date = ? WHERE user_id = ?",
            (datetime.utcnow().isoformat(), user_id)
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Reset daily quotas for {user_id}")


class DockerUserIsolation:
    """Manage Docker container isolation for users"""
    
    def __init__(self, base_image: str = "python:3.11-slim"):
        """
        Initialize Docker isolation manager
        
        Args:
            base_image: Base Docker image
        """
        self.base_image = base_image
        logger.info(f"DockerUserIsolation initialized with image {base_image}")
    
    def generate_dockerfile(self, user_id: str, username: str) -> str:
        """
        Generate Dockerfile for user container
        
        Args:
            user_id: User ID
            username: Username
        
        Returns:
            Dockerfile content
        """
        dockerfile = f"""FROM {self.base_image}

# Set user context
RUN useradd -m -s /bin/bash {username}

# Install dependencies
RUN pip install --no-cache-dir \\
    watchdog \\
    pyyaml \\
    requests \\
    cryptography

# Create user directories
RUN mkdir -p /home/{username}/vault \\
    && mkdir -p /home/{username}/.config \\
    && chown -R {username}:{username} /home/{username}

# Set working directory
WORKDIR /home/{username}

# Switch to user
USER {username}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["/bin/bash"]
"""
        logger.info(f"Generated Dockerfile for user {username}")
        return dockerfile
    
    def generate_docker_compose(self, user_profile: UserProfile, 
                               config: Dict) -> str:
        """
        Generate docker-compose configuration
        
        Args:
            user_profile: User profile
            config: User configuration
        
        Returns:
            Docker-compose YAML content
        """
        container_name = f"asc33_{user_profile.username}"
        
        compose = f"""version: '3.8'

services:
  {container_name}:
    build:
      context: .
      dockerfile: Dockerfile.{user_profile.user_id}
    container_name: {container_name}
    
    environment:
      USER_ID: {user_profile.user_id}
      USERNAME: {user_profile.username}
      USER_ROLE: {user_profile.role}
    
    volumes:
      - ./vaults/{user_profile.user_id}:/home/{user_profile.username}/vault
      - ./configs/{user_profile.user_id}:/home/{user_profile.username}/.config
    
    networks:
      - asc33_network
    
    resources:
      limits:
        cpus: '{config['docker']['cpu_limit']}'
        memory: {config['docker']['memory_limit']}
      reservations:
        cpus: '0.5'
        memory: 512M
    
    restart: unless-stopped
    
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "3"

networks:
  asc33_network:
    driver: bridge
"""
        logger.info(f"Generated docker-compose for {user_profile.username}")
        return compose
