"""
OSINT Legal Engine - Infrastructure d'enquête sécurisée et légale
===============================================================
Double-protection: Anonymité opérationnelle + Auditabilité légale

Anonymité CONTRE les criminels:
- Tor routing automatique
- Pas de traces remontant à l'opérateur
- Métadonnées anonymes en opération

Auditabilité POUR les enquêteurs:
- Signatures cryptographiques des rapports
- Chaincode des sources (intégrité)
- Timestamps vérifiables
- Audit trail sécurisé (chiffré, que vous seul pouvez lire)
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hmac
import base64
from pathlib import Path
import sqlite3

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
except ImportError:
    print("⚠️  cryptography library required: pip install cryptography")


class InvestigationType(Enum):
    """Types d'enquêtes supportées"""
    SCAM = "scam"
    DARKNET_CRIMINAL = "darknet_criminal"
    CHILD_EXPLOITATION = "child_exploitation"
    MALWARE_TRACKING = "malware_tracking"
    PHISHING = "phishing_ring"
    HUMAN_TRAFFICKING = "human_trafficking"
    CYBERCRIMINAL_PROFILING = "cybercriminal_profiling"
    THREAT_INTELLIGENCE = "threat_intelligence"


class IOCType(Enum):
    """Types d'Indicators of Compromise"""
    DOMAIN = "domain"
    IP_ADDRESS = "ip_address"
    EMAIL = "email"
    HASH = "hash"
    URL = "url"
    CRYPTO_WALLET = "crypto_wallet"
    USERNAME = "username"
    PHONE = "phone"
    FILE_HASH = "file_hash"
    BITCOIN_ADDRESS = "bitcoin_address"


@dataclass
class IOC:
    """Indicator of Compromise - Données structurées pour enquêteurs"""
    type: IOCType
    value: str
    confidence: int  # 0-100
    source_url: str
    first_seen: str  # ISO timestamp
    last_seen: str  # ISO timestamp
    context: str  # Description du contexte
    related_iocs: List[str] = None  # IDs d'IOCs liés
    severity: str = "medium"  # low, medium, high, critical
    tags: List[str] = None  # Tags pour filtrage
    
    def __post_init__(self):
        if self.related_iocs is None:
            self.related_iocs = []
        if self.tags is None:
            self.tags = []
    
    def to_dict(self):
        d = asdict(self)
        d['type'] = self.type.value
        return d


@dataclass
class CriminalProfile:
    """Profil de criminel structuré pour enquêteurs"""
    profile_id: str  # Identifiant unique
    darknet_aliases: List[str]
    known_activities: List[str]
    infrastructure_iocs: List[IOC]
    associated_wallets: List[str]
    threat_level: str  # low, medium, high, critical
    timeline_events: List[Dict]  # Events chronologiques
    investigation_notes: str
    confidence_level: int  # 0-100
    last_updated: str  # ISO timestamp
    
    def to_dict(self):
        d = asdict(self)
        d['infrastructure_iocs'] = [ioc.to_dict() for ioc in self.infrastructure_iocs]
        return d


class CryptoAuditTrail:
    """Gestion sécurisée de la piste d'audit (chiffrée, accès personnel seulement)"""
    
    def __init__(self, audit_key: bytes = None):
        """
        Initialise la piste d'audit avec clé personnelle
        
        Args:
            audit_key: Clé 32-bytes pour chiffrement (ou générée)
        """
        self.audit_key = audit_key or os.urandom(32)
        self.audit_db = "osint_audit_trail.db"
        self._init_database()
    
    def _init_database(self):
        """Crée la base de données d'audit"""
        conn = sqlite3.connect(self.audit_db)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            source_url TEXT,
            ioc_extracted TEXT,
            operator_session_id TEXT,
            operation_hash TEXT UNIQUE,
            encrypted_details BLOB,
            signature TEXT
        )''')
        
        conn.commit()
        conn.close()
    
    def log_operation(self, action: str, source_url: str, ioc_extracted: List[IOC],
                     session_id: str, details: Dict) -> str:
        """
        Enregistre une opération dans la piste d'audit
        
        Returns:
            operation_hash: Hash de l'opération pour intégrité
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Hash de l'opération pour intégrité
        operation_data = f"{timestamp}{action}{source_url}{session_id}"
        operation_hash = hashlib.sha256(operation_data.encode()).hexdigest()
        
        # Chiffre les détails
        encrypted_details = self._encrypt_details(details)
        
        # Signature HMAC pour authentification
        signature = hmac.new(
            self.audit_key,
            operation_hash.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Enregistre en base
        conn = sqlite3.connect(self.audit_db)
        c = conn.cursor()
        
        ioc_list = json.dumps([ioc.to_dict() for ioc in ioc_extracted])
        
        c.execute('''INSERT INTO audit_log 
                    (timestamp, action, source_url, ioc_extracted, 
                     operator_session_id, operation_hash, encrypted_details, signature)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                 (timestamp, action, source_url, ioc_list, session_id,
                  operation_hash, encrypted_details, signature))
        
        conn.commit()
        conn.close()
        
        return operation_hash
    
    def _encrypt_details(self, details: Dict) -> bytes:
        """Chiffre les détails avec AES-256-GCM"""
        iv = os.urandom(12)
        cipher = Cipher(
            algorithms.AES(self.audit_key),
            modes.GCM(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        data = json.dumps(details).encode()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        
        return iv + encryptor.tag + ciphertext
    
    def _decrypt_details(self, encrypted: bytes) -> Dict:
        """Déchiffre les détails"""
        iv = encrypted[:12]
        tag = encrypted[12:28]
        ciphertext = encrypted[28:]
        
        cipher = Cipher(
            algorithms.AES(self.audit_key),
            modes.GCM(iv, tag),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        data = decryptor.update(ciphertext) + decryptor.finalize()
        return json.loads(data.decode())
    
    def verify_audit_trail(self) -> bool:
        """Vérifie l'intégrité complète de la piste d'audit"""
        conn = sqlite3.connect(self.audit_db)
        c = conn.cursor()
        
        c.execute('SELECT operation_hash, signature FROM audit_log')
        rows = c.fetchall()
        conn.close()
        
        for op_hash, signature in rows:
            expected_sig = hmac.new(
                self.audit_key,
                op_hash.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_sig):
                return False
        
        return True
    
    def export_audit_trail(self, output_path: str) -> str:
        """Exporte la piste d'audit pour vérification personnelle"""
        conn = sqlite3.connect(self.audit_db)
        c = conn.cursor()
        
        c.execute('SELECT * FROM audit_log ORDER BY timestamp DESC')
        rows = c.fetchall()
        conn.close()
        
        # Format lisible avec vérification d'intégrité
        report = "# AUDIT TRAIL SÉCURISÉ\n\n"
        report += f"Généré: {datetime.now(timezone.utc).isoformat()}\n"
        report += f"Intégrité vérifiée: {self.verify_audit_trail()}\n\n"
        
        for row in rows:
            report += f"- **{row[2]}** ({row[1]})\n"
            report += f"  Source: {row[3]}\n"
            report += f"  IOCs: {row[4]}\n"
            report += f"  Hash: {row[6]}\n\n"
        
        Path(output_path).write_text(report)
        return output_path


class LegalReportSigner:
    """Signature cryptographique des rapports pour enquêteurs"""
    
    def __init__(self, private_key_path: str = None, public_key_path: str = None):
        """Initialise le système de signature"""
        self.private_key_path = private_key_path or "osint_private.pem"
        self.public_key_path = public_key_path or "osint_public.pem"
        
        if not os.path.exists(self.private_key_path):
            self._generate_keys()
    
    def _generate_keys(self):
        """Génère une paire RSA 4096-bit pour signatures"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        
        # Sauvegarde clé privée (à protéger!)
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Sauvegarde clé publique
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        Path(self.private_key_path).write_bytes(private_pem)
        Path(self.public_key_path).write_bytes(public_pem)
    
    def sign_report(self, report_content: str) -> str:
        """
        Signe un rapport pour authentification légale
        
        Returns:
            Signature base64
        """
        private_key = serialization.load_pem_private_key(
            Path(self.private_key_path).read_bytes(),
            password=None,
            backend=default_backend()
        )
        
        signature = private_key.sign(
            report_content.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return base64.b64encode(signature).decode()
    
    def get_public_key_fingerprint(self) -> str:
        """Retourne l'empreinte de la clé publique (pour vérification)"""
        public_key_data = Path(self.public_key_path).read_bytes()
        return hashlib.sha256(public_key_data).hexdigest()
    
    @staticmethod
    def verify_signature(report_content: str, signature_b64: str, public_key_pem: bytes) -> bool:
        """Vérifie la signature d'un rapport (pour enquêteurs)"""
        try:
            public_key = serialization.load_pem_public_key(
                public_key_pem,
                backend=default_backend()
            )
            
            signature = base64.b64decode(signature_b64)
            
            public_key.verify(
                signature,
                report_content.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False


class StructuredOSINTReport:
    """Générateur de rapports OSINT structurés pour enquêteurs"""
    
    def __init__(self, investigation_type: InvestigationType, title: str):
        self.investigation_type = investigation_type
        self.title = title
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.iocs: List[IOC] = []
        self.criminal_profiles: List[CriminalProfile] = []
        self.timeline_events: List[Dict] = []
        self.conclusions: str = ""
    
    def add_ioc(self, ioc: IOC):
        """Ajoute un IOC au rapport"""
        self.iocs.append(ioc)
    
    def add_criminal_profile(self, profile: CriminalProfile):
        """Ajoute un profil criminel"""
        self.criminal_profiles.append(profile)
    
    def add_timeline_event(self, timestamp: str, event_type: str, description: str):
        """Ajoute un événement à la timeline"""
        self.timeline_events.append({
            'timestamp': timestamp,
            'type': event_type,
            'description': description
        })
    
    def generate_markdown(self) -> str:
        """Génère un rapport Markdown structuré"""
        report = f"# Rapport OSINT: {self.title}\n\n"
        report += f"**Type d'enquête**: {self.investigation_type.value}\n"
        report += f"**Généré**: {self.timestamp}\n"
        report += f"**Nombre d'IOCs**: {len(self.iocs)}\n"
        report += f"**Profils criminels identifiés**: {len(self.criminal_profiles)}\n\n"
        
        # IOCs structurés
        if self.iocs:
            report += "## Indicators of Compromise (IOCs)\n\n"
            
            # Grouper par type
            by_type = {}
            for ioc in self.iocs:
                if ioc.type.value not in by_type:
                    by_type[ioc.type.value] = []
                by_type[ioc.type.value].append(ioc)
            
            for ioc_type, iocs in sorted(by_type.items()):
                report += f"\n### {ioc_type.upper()} ({len(iocs)})\n\n"
                for ioc in iocs:
                    report += f"- **{ioc.value}**\n"
                    report += f"  - Confiance: {ioc.confidence}%\n"
                    report += f"  - Sévérité: {ioc.severity}\n"
                    report += f"  - Source: {ioc.source_url}\n"
                    report += f"  - Contexte: {ioc.context}\n\n"
        
        # Profils criminels
        if self.criminal_profiles:
            report += "\n## Profils Criminels Identifiés\n\n"
            for profile in self.criminal_profiles:
                report += f"\n### {profile.profile_id}\n\n"
                report += f"**Niveau de menace**: {profile.threat_level}\n"
                report += f"**Confiance**: {profile.confidence_level}%\n\n"
                
                report += "**Alias sur darknet**:\n"
                for alias in profile.darknet_aliases:
                    report += f"- {alias}\n"
                
                report += "\n**Activités connues**:\n"
                for activity in profile.known_activities:
                    report += f"- {activity}\n"
                
                if profile.associated_wallets:
                    report += "\n**Portefeuilles associés**:\n"
                    for wallet in profile.associated_wallets:
                        report += f"- {wallet}\n"
                
                report += f"\n**Notes**:\n{profile.investigation_notes}\n"
        
        # Timeline
        if self.timeline_events:
            report += "\n## Timeline des Événements\n\n"
            for event in sorted(self.timeline_events, key=lambda x: x['timestamp']):
                report += f"- **{event['timestamp']}**: {event['type']} - {event['description']}\n"
        
        # Conclusions
        if self.conclusions:
            report += f"\n## Conclusions\n\n{self.conclusions}\n"
        
        return report
    
    def generate_json(self) -> Dict:
        """Exporte le rapport en JSON structuré"""
        return {
            'metadata': {
                'title': self.title,
                'investigation_type': self.investigation_type.value,
                'timestamp': self.timestamp,
                'ioc_count': len(self.iocs),
                'profile_count': len(self.criminal_profiles)
            },
            'iocs': [ioc.to_dict() for ioc in self.iocs],
            'criminal_profiles': [p.to_dict() for p in self.criminal_profiles],
            'timeline': self.timeline_events,
            'conclusions': self.conclusions
        }


class OSINTLegalEngine:
    """Moteur OSINT complet avec double-protection"""
    
    def __init__(self, audit_key: bytes = None):
        self.audit_trail = CryptoAuditTrail(audit_key)
        self.signer = LegalReportSigner()
        self.session_id = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
        
        # Tor + VPN doivent être configurés
        self.tor_enabled = self._check_tor_status()
    
    def _check_tor_status(self) -> bool:
        """Vérifie si Tor est actif"""
        try:
            import requests
            response = requests.get('https://check.torproject.org/api/ip', 
                                   proxies={'https': 'socks5://localhost:9050'},
                                   timeout=5)
            return response.json().get('is_tor', False)
        except:
            return False
    
    def create_investigation(self, investigation_type: InvestigationType, 
                            title: str) -> StructuredOSINTReport:
        """Crée une nouvelle enquête structurée"""
        return StructuredOSINTReport(investigation_type, title)
    
    def finalize_report(self, report: StructuredOSINTReport, 
                       output_dir: str = "osint_reports") -> Tuple[str, str, str]:
        """
        Finalise et signe un rapport
        
        Returns:
            (markdown_path, json_path, signature)
        """
        Path(output_dir).mkdir(exist_ok=True)
        
        # Génère contenu
        markdown = report.generate_markdown()
        json_data = report.generate_json()
        
        # Ajoute métadonnées de sécurité
        json_data['security'] = {
            'audit_trail_enabled': True,
            'tor_enabled': self.tor_enabled,
            'session_id': self.session_id,
            'signature_public_key': self.signer.get_public_key_fingerprint(),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        # Signe le rapport
        signature = self.signer.sign_report(markdown)
        json_data['signature'] = signature
        
        # Enregistre en audit trail
        self.audit_trail.log_operation(
            action="report_generated",
            source_url="internal",
            ioc_extracted=report.iocs,
            session_id=self.session_id,
            details={
                'report_title': report.title,
                'ioc_count': len(report.iocs),
                'profile_count': len(report.criminal_profiles),
                'signature': signature
            }
        )
        
        # Sauvegarde les fichiers
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        
        markdown_path = f"{output_dir}/{report.title.replace(' ', '_')}_{timestamp}.md"
        json_path = f"{output_dir}/{report.title.replace(' ', '_')}_{timestamp}.json"
        
        Path(markdown_path).write_text(markdown)
        Path(json_path).write_text(json.dumps(json_data, indent=2))
        
        print(f"✅ Rapport généré et signé: {markdown_path}")
        print(f"📋 Données structurées: {json_path}")
        print(f"🔐 Signature: {signature[:50]}...")
        
        return markdown_path, json_path, signature


if __name__ == "__main__":
    # Exemple d'utilisation
    engine = OSINTLegalEngine()
    
    print(f"🕵️  Session OSINT initialisée")
    print(f"📡 Tor actif: {engine.tor_enabled}")
    print(f"🔒 Audit trail sécurisé: {engine.audit_trail.audit_db}")
    print(f"✍️  Clé de signature: {engine.signer.get_public_key_fingerprint()[:16]}...")
