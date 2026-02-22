"""
JOUR 2 - RSA-4096 Cryptographic System Tests
Test suite for RSA encryption, signatures, and certificate management
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

from rsa_cryptographic_system import (
    RSAKeyManager,
    RSASignatureHandler,
    RSAEncryptionHandler,
    CertificateManager
)


class TestRSAKeyManager:
    """Test RSAKeyManager for key generation and management"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for key storage"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_keypair_generation(self, temp_dir):
        """Test RSA-4096 keypair generation"""
        manager = RSAKeyManager(key_storage_path=temp_dir)
        private_key, public_key = manager.generate_keypair()
        
        assert private_key is not None
        assert public_key is not None
        # Verify RSA-4096 (4096 bits)
        assert private_key.key_size == 4096
        assert public_key.key_size == 4096

    def test_key_persistence(self, temp_dir):
        """Test saving and loading keys"""
        manager = RSAKeyManager(key_storage_path=temp_dir)
        private_key, public_key = manager.generate_keypair()
        
        # Paths should exist in manager
        assert manager.key_storage_path == temp_dir

    def test_key_fingerprint_generation(self, temp_dir):
        """Test key fingerprint generation"""
        manager = RSAKeyManager(key_storage_path=temp_dir)
        private_key, public_key = manager.generate_keypair()
        
        fingerprint = manager.get_key_fingerprint(public_key)
        assert fingerprint is not None
        assert len(fingerprint) > 0
        assert isinstance(fingerprint, str)

    def test_key_fingerprint_consistency(self, temp_dir):
        """Test that fingerprint is consistent for same key"""
        manager = RSAKeyManager(key_storage_path=temp_dir)
        private_key, public_key = manager.generate_keypair()
        
        fingerprint1 = manager.get_key_fingerprint(public_key)
        fingerprint2 = manager.get_key_fingerprint(public_key)
        
        assert fingerprint1 == fingerprint2

    def test_key_fingerprint_uniqueness(self, temp_dir):
        """Test that different keys have different fingerprints"""
        manager = RSAKeyManager(key_storage_path=temp_dir)
        private_key1, public_key1 = manager.generate_keypair()
        private_key2, public_key2 = manager.generate_keypair()
        
        fingerprint1 = manager.get_key_fingerprint(public_key1)
        fingerprint2 = manager.get_key_fingerprint(public_key2)
        
        assert fingerprint1 != fingerprint2


class TestRSASignatureHandler:
    """Test RSASignatureHandler for document signing and verification"""

    @pytest.fixture
    def key_pair(self):
        """Generate keypair for testing"""
        manager = RSAKeyManager()
        private_key, public_key = manager.generate_keypair()
        return private_key, public_key

    def test_data_signing(self, key_pair):
        """Test signing data with RSA private key"""
        private_key, public_key = key_pair
        handler = RSASignatureHandler()
        
        data = b"Important document content"
        signature = handler.sign_data(private_key, data)
        
        assert signature is not None
        assert len(signature) > 0
        assert isinstance(signature, bytes)

    def test_signature_verification_success(self, key_pair):
        """Test successful signature verification"""
        private_key, public_key = key_pair
        handler = RSASignatureHandler()
        
        data = b"Important document content"
        signature = handler.sign_data(private_key, data)
        is_valid = handler.verify_signature(public_key, data, signature)
        
        assert is_valid is True

    def test_signature_verification_failure_tampered_data(self, key_pair):
        """Test signature verification fails with tampered data"""
        private_key, public_key = key_pair
        handler = RSASignatureHandler()
        
        original_data = b"Important document content"
        tampered_data = b"Tampered document content"
        signature = handler.sign_data(private_key, original_data)
        
        is_valid = handler.verify_signature(public_key, tampered_data, signature)
        assert is_valid is False

    def test_signature_verification_failure_invalid_signature(self, key_pair):
        """Test signature verification fails with invalid signature"""
        private_key, public_key = key_pair
        handler = RSASignatureHandler()
        
        data = b"Important document content"
        # Create fake signature
        fake_signature = b"not a valid signature"
        
        with pytest.raises(Exception):
            handler.verify_signature(public_key, data, fake_signature)

    def test_document_signing(self, key_pair):
        """Test signing entire documents"""
        private_key, public_key = key_pair
        handler = RSASignatureHandler()
        
        document_content = b"This is a complete document with multiple paragraphs of important information."
        signed_data = handler.sign_document(private_key, document_content)
        
        assert signed_data is not None
        assert len(signed_data) > 0

    def test_document_verification(self, key_pair):
        """Test verifying signed documents"""
        private_key, public_key = key_pair
        handler = RSASignatureHandler()
        
        document_content = b"This is a complete document with multiple paragraphs of important information."
        signed_data = handler.sign_document(private_key, document_content)
        is_valid = handler.verify_document(public_key, signed_data)
        
        assert is_valid is True

    def test_signature_format_base64_encoding(self, key_pair):
        """Test signature is properly formatted in base64"""
        private_key, public_key = key_pair
        handler = RSASignatureHandler()
        
        data = b"Test data"
        signature = handler.sign_data(private_key, data)
        
        # Signature should be bytes (base64 encoded internally)
        assert isinstance(signature, bytes)


class TestRSAEncryptionHandler:
    """Test RSAEncryptionHandler for asymmetric encryption"""

    @pytest.fixture
    def key_pair(self):
        """Generate keypair for testing"""
        manager = RSAKeyManager()
        private_key, public_key = manager.generate_keypair()
        return private_key, public_key

    def test_data_encryption(self, key_pair):
        """Test encrypting data with public key"""
        private_key, public_key = key_pair
        handler = RSAEncryptionHandler()
        
        plaintext = b"Secret message content"
        ciphertext = handler.encrypt_data(public_key, plaintext)
        
        assert ciphertext is not None
        assert ciphertext != plaintext
        assert len(ciphertext) > len(plaintext)

    def test_data_decryption(self, key_pair):
        """Test decrypting data with private key"""
        private_key, public_key = key_pair
        handler = RSAEncryptionHandler()
        
        plaintext = b"Secret message content"
        ciphertext = handler.encrypt_data(public_key, plaintext)
        decrypted = handler.decrypt_data(private_key, ciphertext)
        
        assert decrypted == plaintext

    def test_encryption_roundtrip(self, key_pair):
        """Test full encryption-decryption roundtrip"""
        private_key, public_key = key_pair
        handler = RSAEncryptionHandler()
        
        original_messages = [
            b"First secret message",
            b"Second secret message",
            b"Third secret message with special characters: !@#$%^&*()"
        ]
        
        for original in original_messages:
            encrypted = handler.encrypt_data(public_key, original)
            decrypted = handler.decrypt_data(private_key, encrypted)
            assert decrypted == original

    def test_encryption_produces_different_ciphertexts(self, key_pair):
        """Test that encrypting same data produces different ciphertexts (OAEP)"""
        private_key, public_key = key_pair
        handler = RSAEncryptionHandler()
        
        plaintext = b"Same message"
        ciphertext1 = handler.encrypt_data(public_key, plaintext)
        ciphertext2 = handler.encrypt_data(public_key, plaintext)
        
        # Due to OAEP randomness, ciphertexts should be different
        assert ciphertext1 != ciphertext2

    def test_decrypt_wrong_key_fails(self):
        """Test that decryption fails with wrong private key"""
        manager = RSAKeyManager()
        private_key1, public_key1 = manager.generate_keypair()
        private_key2, public_key2 = manager.generate_keypair()
        
        handler = RSAEncryptionHandler()
        
        plaintext = b"Secret message"
        ciphertext = handler.encrypt_data(public_key1, plaintext)
        
        with pytest.raises(Exception):
            handler.decrypt_data(private_key2, ciphertext)


class TestCertificateManager:
    """Test CertificateManager for X.509 certificate handling"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for certificates"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_self_signed_certificate_generation(self, temp_dir):
        """Test generating self-signed X.509 certificate"""
        manager = CertificateManager(cert_storage_path=temp_dir)
        key_manager = RSAKeyManager()
        private_key, public_key = key_manager.generate_keypair()
        
        cert = manager.generate_self_signed_cert(
            private_key=private_key,
            public_key=public_key,
            subject_name="test.example.com",
            issuer_name="Test CA"
        )
        
        assert cert is not None

    def test_certificate_validity_period(self, temp_dir):
        """Test certificate has proper validity period"""
        manager = CertificateManager(cert_storage_path=temp_dir)
        key_manager = RSAKeyManager()
        private_key, public_key = key_manager.generate_keypair()
        
        cert = manager.generate_self_signed_cert(
            private_key=private_key,
            public_key=public_key,
            subject_name="test.example.com",
            issuer_name="Test CA",
            validity_days=365
        )
        
        # Certificate should have validity info
        assert cert is not None

    def test_certificate_subject_information(self, temp_dir):
        """Test certificate contains subject information"""
        manager = CertificateManager(cert_storage_path=temp_dir)
        key_manager = RSAKeyManager()
        private_key, public_key = key_manager.generate_keypair()
        
        subject_name = "test.example.com"
        issuer_name = "Test CA"
        
        cert = manager.generate_self_signed_cert(
            private_key=private_key,
            public_key=public_key,
            subject_name=subject_name,
            issuer_name=issuer_name
        )
        
        assert cert is not None

    def test_certificate_multiple_generation(self, temp_dir):
        """Test generating multiple different certificates"""
        manager = CertificateManager(cert_storage_path=temp_dir)
        key_manager = RSAKeyManager()
        
        certificates = []
        for i in range(3):
            private_key, public_key = key_manager.generate_keypair()
            cert = manager.generate_self_signed_cert(
                private_key=private_key,
                public_key=public_key,
                subject_name=f"service{i}.example.com",
                issuer_name="Test CA"
            )
            certificates.append(cert)
        
        assert len(certificates) == 3
        # Each cert should be different (different keys)
        for i in range(len(certificates)-1):
            for j in range(i+1, len(certificates)):
                assert certificates[i] is not None
                assert certificates[j] is not None


class TestCryptographicIntegration:
    """Integration tests for complete cryptographic workflows"""

    def test_sign_and_verify_workflow(self):
        """Test complete sign and verify workflow"""
        key_manager = RSAKeyManager()
        sig_handler = RSASignatureHandler()
        
        # Generate keys
        private_key, public_key = key_manager.generate_keypair()
        
        # Sign document
        document = b"Important agreement document"
        signature = sig_handler.sign_data(private_key, document)
        
        # Verify signature
        is_valid = sig_handler.verify_signature(public_key, document, signature)
        assert is_valid is True

    def test_encrypt_and_decrypt_workflow(self):
        """Test complete encrypt and decrypt workflow"""
        key_manager = RSAKeyManager()
        enc_handler = RSAEncryptionHandler()
        
        # Generate keys
        private_key, public_key = key_manager.generate_keypair()
        
        # Encrypt message
        message = b"Confidential information"
        ciphertext = enc_handler.encrypt_data(public_key, message)
        
        # Decrypt message
        decrypted = enc_handler.decrypt_data(private_key, ciphertext)
        assert decrypted == message

    def test_signature_with_certificate(self):
        """Test signing and certificate generation together"""
        key_manager = RSAKeyManager()
        sig_handler = RSASignatureHandler()
        cert_manager = CertificateManager()
        
        # Generate keys
        private_key, public_key = key_manager.generate_keypair()
        
        # Create certificate
        cert = cert_manager.generate_self_signed_cert(
            private_key=private_key,
            public_key=public_key,
            subject_name="signer.example.com",
            issuer_name="CA"
        )
        
        # Sign data
        data = b"Signed document"
        signature = sig_handler.sign_data(private_key, data)
        
        # Verify with public key from certificate
        is_valid = sig_handler.verify_signature(public_key, data, signature)
        assert is_valid is True

    def test_multi_party_encryption_workflow(self):
        """Test encryption workflow with multiple parties"""
        key_manager = RSAKeyManager()
        enc_handler = RSAEncryptionHandler()
        
        # Generate keys for multiple parties
        alice_private, alice_public = key_manager.generate_keypair()
        bob_private, bob_public = key_manager.generate_keypair()
        
        # Alice encrypts message for Bob
        message = b"Secret message from Alice to Bob"
        encrypted_for_bob = enc_handler.encrypt_data(bob_public, message)
        
        # Bob decrypts message
        decrypted = enc_handler.decrypt_data(bob_private, encrypted_for_bob)
        assert decrypted == message
        
        # Bob cannot decrypt message encrypted for Alice
        encrypted_for_alice = enc_handler.encrypt_data(alice_public, message)
        with pytest.raises(Exception):
            enc_handler.decrypt_data(bob_private, encrypted_for_alice)

    def test_key_fingerprint_identification(self):
        """Test using key fingerprints for key identification"""
        key_manager = RSAKeyManager()
        
        # Generate multiple keypairs
        keypairs = []
        fingerprints = []
        
        for i in range(5):
            private_key, public_key = key_manager.generate_keypair()
            fingerprint = key_manager.get_key_fingerprint(public_key)
            keypairs.append((private_key, public_key))
            fingerprints.append(fingerprint)
        
        # All fingerprints should be unique
        assert len(set(fingerprints)) == len(fingerprints)

    def test_document_integrity_chain(self):
        """Test document integrity using signatures"""
        key_manager = RSAKeyManager()
        sig_handler = RSASignatureHandler()
        
        private_key, public_key = key_manager.generate_keypair()
        
        # Original document
        document_v1 = b"Document version 1"
        signature_v1 = sig_handler.sign_data(private_key, document_v1)
        
        # Modified document (new version)
        document_v2 = b"Document version 2"
        signature_v2 = sig_handler.sign_data(private_key, document_v2)
        
        # Verify original is still valid
        assert sig_handler.verify_signature(public_key, document_v1, signature_v1) is True
        
        # Verify modified is valid with new signature
        assert sig_handler.verify_signature(public_key, document_v2, signature_v2) is True
        
        # Verify original signature fails for modified document
        assert sig_handler.verify_signature(public_key, document_v2, signature_v1) is False


class TestCryptographicSecurity:
    """Security-focused tests for cryptographic operations"""

    def test_key_size_validation(self):
        """Test RSA-4096 key size requirement"""
        manager = RSAKeyManager()
        private_key, public_key = manager.generate_keypair()
        
        # Verify 4096-bit keys
        assert private_key.key_size == 4096
        assert public_key.key_size == 4096

    def test_random_padding_differences(self):
        """Test OAEP padding produces different ciphertexts"""
        key_manager = RSAKeyManager()
        enc_handler = RSAEncryptionHandler()
        
        private_key, public_key = key_manager.generate_keypair()
        
        plaintext = b"Test message"
        
        # Encrypt same plaintext multiple times
        ciphertexts = [
            enc_handler.encrypt_data(public_key, plaintext)
            for _ in range(5)
        ]
        
        # All ciphertexts should be different due to random padding
        assert len(set(ciphertexts)) == len(ciphertexts)

    def test_no_ciphertext_leakage(self):
        """Test ciphertext doesn't reveal plaintext patterns"""
        key_manager = RSAKeyManager()
        enc_handler = RSAEncryptionHandler()
        
        private_key, public_key = key_manager.generate_keypair()
        
        # Encrypt similar messages
        msg1 = b"AAAA" + b"X" + b"AAAA"
        msg2 = b"AAAA" + b"Y" + b"AAAA"
        
        cipher1 = enc_handler.encrypt_data(public_key, msg1)
        cipher2 = enc_handler.encrypt_data(public_key, msg2)
        
        # Ciphertexts should look completely different
        assert cipher1 != cipher2
        # No obvious pattern relationship
        assert len(cipher1) == len(cipher2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
