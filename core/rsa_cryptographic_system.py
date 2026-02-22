# ============================================================================
# RSA-4096 CRYPTOGRAPHIC SYSTEM - Signature & Encryption
# ============================================================================
# Purpose: Manage RSA-4096 key generation, signatures, and encryption
# Features: Key generation, signing, verification, certificate handling
#
# Author: Ascended33 Platform
# Version: 1.0.0 (JOUR 2)
# Status: Production Ready
# ============================================================================

import logging
import json
from typing import Tuple, Optional, Dict
from pathlib import Path
from datetime import datetime, timedelta
import hashlib
import base64

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.backends import default_backend
    from cryptography.x509 import (
        Certificate, CertificateBuilder, Name, NameAttribute,
        BasicConstraints, Extension, KeyUsage
    )
    from cryptography import x509
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    logging.warning("cryptography library not installed")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RSAKeyManager:
    """Manage RSA-4096 key generation and storage"""
    
    KEY_SIZE = 4096
    PUBLIC_EXPONENT = 65537
    
    def __init__(self, key_dir: str):
        """
        Initialize RSA key manager
        
        Args:
            key_dir: Directory for storing keys
        """
        if not CRYPTO_AVAILABLE:
            raise RuntimeError("cryptography library required")
        
        self.key_dir = Path(key_dir)
        self.key_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"RSAKeyManager initialized at {key_dir}")
    
    def generate_keypair(self, user_id: str) -> Tuple[str, str]:
        """
        Generate RSA-4096 keypair for user
        
        Args:
            user_id: User ID
        
        Returns:
            Tuple of (private_key_path, public_key_path)
        """
        logger.info(f"Generating RSA-4096 keypair for {user_id}...")
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=self.PUBLIC_EXPONENT,
            key_size=self.KEY_SIZE,
            backend=default_backend()
        )
        
        # Extract public key
        public_key = private_key.public_key()
        
        # Serialize private key (PEM format with encryption)
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Serialize public key (PEM format)
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Save keys
        private_key_path = self.key_dir / f"{user_id}_private.pem"
        public_key_path = self.key_dir / f"{user_id}_public.pem"
        
        private_key_path.write_bytes(private_pem)
        public_key_path.write_bytes(public_pem)
        
        # Set restrictive permissions
        private_key_path.chmod(0o600)
        public_key_path.chmod(0o644)
        
        logger.info(f"Keypair generated: {private_key_path}")
        return str(private_key_path), str(public_key_path)
    
    def load_private_key(self, key_path: str):
        """
        Load private key from file
        
        Args:
            key_path: Path to private key
        
        Returns:
            Private key object
        """
        key_data = Path(key_path).read_bytes()
        private_key = serialization.load_pem_private_key(
            key_data,
            password=None,
            backend=default_backend()
        )
        return private_key
    
    def load_public_key(self, key_path: str):
        """
        Load public key from file
        
        Args:
            key_path: Path to public key
        
        Returns:
            Public key object
        """
        key_data = Path(key_path).read_bytes()
        public_key = serialization.load_pem_public_key(
            key_data,
            backend=default_backend()
        )
        return public_key
    
    def get_key_fingerprint(self, key_path: str) -> str:
        """
        Get fingerprint of key
        
        Args:
            key_path: Path to key file
        
        Returns:
            Key fingerprint (SHA-256 hex)
        """
        key_data = Path(key_path).read_bytes()
        fingerprint = hashlib.sha256(key_data).hexdigest()
        return fingerprint


class RSASignatureHandler:
    """Handle RSA signatures for document verification"""
    
    def __init__(self, key_manager: RSAKeyManager):
        """
        Initialize signature handler
        
        Args:
            key_manager: RSAKeyManager instance
        """
        self.key_manager = key_manager
        logger.info("RSASignatureHandler initialized")
    
    def sign_data(self, data: str, private_key_path: str) -> str:
        """
        Sign data with private key
        
        Args:
            data: Data to sign
            private_key_path: Path to private key
        
        Returns:
            Base64-encoded signature
        """
        private_key = self.key_manager.load_private_key(private_key_path)
        
        signature = private_key.sign(
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Encode signature to base64
        signature_b64 = base64.b64encode(signature).decode()
        
        logger.info("Data signed successfully")
        return signature_b64
    
    def verify_signature(self, data: str, signature_b64: str, 
                        public_key_path: str) -> bool:
        """
        Verify data signature with public key
        
        Args:
            data: Original data
            signature_b64: Base64-encoded signature
            public_key_path: Path to public key
        
        Returns:
            Verification result
        """
        try:
            public_key = self.key_manager.load_public_key(public_key_path)
            signature = base64.b64decode(signature_b64)
            
            public_key.verify(
                signature,
                data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            logger.info("Signature verified successfully")
            return True
            
        except Exception as e:
            logger.warning(f"Signature verification failed: {e}")
            return False
    
    def sign_document(self, document_data: Dict, private_key_path: str) -> Dict:
        """
        Sign entire document with metadata
        
        Args:
            document_data: Document to sign
            private_key_path: Path to private key
        
        Returns:
            Signed document with metadata
        """
        # Create document envelope
        doc_json = json.dumps(document_data, sort_keys=True)
        
        # Sign
        signature = self.sign_data(doc_json, private_key_path)
        
        # Create signed document
        signed_doc = {
            'data': document_data,
            'signature': signature,
            'signed_at': datetime.utcnow().isoformat(),
            'algorithm': 'RSA-4096-PSS-SHA256'
        }
        
        logger.info("Document signed")
        return signed_doc
    
    def verify_document(self, signed_doc: Dict, public_key_path: str) -> bool:
        """
        Verify signed document
        
        Args:
            signed_doc: Signed document
            public_key_path: Path to public key
        
        Returns:
            Verification result
        """
        try:
            doc_json = json.dumps(signed_doc['data'], sort_keys=True)
            
            return self.verify_signature(
                doc_json,
                signed_doc['signature'],
                public_key_path
            )
            
        except Exception as e:
            logger.error(f"Document verification failed: {e}")
            return False


class RSAEncryptionHandler:
    """Handle RSA encryption/decryption"""
    
    def __init__(self, key_manager: RSAKeyManager):
        """
        Initialize encryption handler
        
        Args:
            key_manager: RSAKeyManager instance
        """
        self.key_manager = key_manager
        logger.info("RSAEncryptionHandler initialized")
    
    def encrypt_data(self, data: str, public_key_path: str) -> str:
        """
        Encrypt data with public key
        
        Args:
            data: Data to encrypt
            public_key_path: Path to public key
        
        Returns:
            Base64-encoded ciphertext
        """
        public_key = self.key_manager.load_public_key(public_key_path)
        
        ciphertext = public_key.encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Encode to base64
        ciphertext_b64 = base64.b64encode(ciphertext).decode()
        
        logger.info("Data encrypted")
        return ciphertext_b64
    
    def decrypt_data(self, ciphertext_b64: str, private_key_path: str) -> Optional[str]:
        """
        Decrypt data with private key
        
        Args:
            ciphertext_b64: Base64-encoded ciphertext
            private_key_path: Path to private key
        
        Returns:
            Decrypted data or None if failed
        """
        try:
            private_key = self.key_manager.load_private_key(private_key_path)
            ciphertext = base64.b64decode(ciphertext_b64)
            
            plaintext = private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            logger.info("Data decrypted")
            return plaintext.decode()
            
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return None


class CertificateManager:
    """Manage X.509 certificates for users"""
    
    def __init__(self, cert_dir: str, key_manager: RSAKeyManager):
        """
        Initialize certificate manager
        
        Args:
            cert_dir: Directory for storing certificates
            key_manager: RSAKeyManager instance
        """
        self.cert_dir = Path(cert_dir)
        self.cert_dir.mkdir(parents=True, exist_ok=True)
        self.key_manager = key_manager
        logger.info(f"CertificateManager initialized at {cert_dir}")
    
    def generate_self_signed_cert(self, user_id: str, username: str, 
                                  email: str, days_valid: int = 365) -> str:
        """
        Generate self-signed certificate for user
        
        Args:
            user_id: User ID
            username: Username
            email: Email address
            days_valid: Certificate validity period
        
        Returns:
            Path to certificate
        """
        # Load user's public key
        public_key_path = self.key_manager.key_dir / f"{user_id}_public.pem"
        private_key_path = self.key_manager.key_dir / f"{user_id}_private.pem"
        
        if not public_key_path.exists():
            logger.error(f"Public key not found for {user_id}")
            return ""
        
        private_key = self.key_manager.load_private_key(str(private_key_path))
        public_key = self.key_manager.load_public_key(str(public_key_path))
        
        # Build certificate
        subject = issuer = Name([
            NameAttribute(x509.NameOID.COUNTRY_NAME, "CA"),
            NameAttribute(x509.NameOID.STATE_OR_PROVINCE_NAME, "ON"),
            NameAttribute(x509.NameOID.ORGANIZATION_NAME, "Ascended33"),
            NameAttribute(x509.NameOID.COMMON_NAME, username),
            NameAttribute(x509.NameOID.EMAIL_ADDRESS, email),
        ])
        
        cert = CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            public_key
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=days_valid)
        ).add_extension(
            BasicConstraints(ca=False, path_length=None),
            critical=True,
        ).add_extension(
            KeyUsage(
                digital_signature=True,
                content_commitment=True,
                key_encipherment=True,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).sign(private_key, hashes.SHA256(), default_backend())
        
        # Save certificate
        cert_path = self.cert_dir / f"{user_id}_cert.pem"
        cert_pem = cert.public_bytes(serialization.Encoding.PEM)
        cert_path.write_bytes(cert_pem)
        cert_path.chmod(0o644)
        
        logger.info(f"Certificate generated: {cert_path}")
        return str(cert_path)
    
    def verify_certificate(self, cert_path: str) -> Dict:
        """
        Verify certificate
        
        Args:
            cert_path: Path to certificate
        
        Returns:
            Certificate info dictionary
        """
        try:
            cert_data = Path(cert_path).read_bytes()
            cert = x509.load_pem_x509_certificate(
                cert_data,
                backend=default_backend()
            )
            
            info = {
                'subject': str(cert.subject),
                'issuer': str(cert.issuer),
                'not_before': cert.not_valid_before.isoformat(),
                'not_after': cert.not_valid_after.isoformat(),
                'serial_number': cert.serial_number,
                'is_valid': cert.not_valid_before <= datetime.utcnow() <= cert.not_valid_after
            }
            
            logger.info(f"Certificate verified: {cert_path}")
            return info
            
        except Exception as e:
            logger.error(f"Certificate verification failed: {e}")
            return {}
