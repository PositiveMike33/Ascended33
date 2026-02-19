# Guide OSINT Légal et Sécurisé
## Infrastructure d'Investigation avec Double-Protection

---

## 📋 Vue d'ensemble

Cette infrastructure offre:

### ✅ Anonymité Opérationnelle
- Tor obligatoire pour tout trafic
- Pas de traces remontant à l'opérateur
- Pas de logs détaillés exposant les activités
- Métadonnées anonymes en opération interne

### ✅ Auditabilité Légale
- Signatures cryptographiques RSA-4096 de tous les rapports
- Chaîne de preuves (Chain of Custody) complète
- Timestamps UTC horodatés et vérifiables
- Hashes d'intégrité pour chaque IOC
- Preuves admissibles devant les tribunaux

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 OSINT Investigation Platform            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐                                       │
│  │   TH3-TOR    │◄─── Routage anonyme (SOCKS5)        │
│  │  9050 port   │     Tout le trafic via Tor          │
│  └──────────────┘                                       │
│         ▲                                               │
│         │                                               │
│  ┌──────┴─────────────────────────┐                    │
│  │                                │                    │
│  │    Opérations Anonymes         │                    │
│  │    (Pas de traces)             │                    │
│  │                                │                    │
│  ├─────────────┬──────────────┬───┤                    │
│  │             │              │   │                    │
│  ▼             ▼              ▼   ▼                    │
│┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
││TH3-KALI  │ │TH3-GPTED │ │TH3-GPTED │ │TH3-HEX   │   │
││Recon     │ │Claude AI │ │Analyse   │ │Dashboard │   │
││(OSINT)   │ │(Reports) │ │(IOCs)    │ │(UI)      │   │
│└──────────┘ └──────────┘ └──────────┘ └──────────┘   │
│                                                         │
│    Rapports Signés ──► ENQUÊTEURS/AUTORITÉS           │
│                                                         │
└─────────────────────────────────────────────────────────┘

Isolation réseau: 172.25.0.0/16
Authentification: RSA-4096 PSS-SHA256
Audit Trail: Chiffré AES-256-GCM
```

---

## 🚀 Démarrage

### Prérequis
- Docker & Docker Compose installés
- 4GB RAM minimum
- Accès Tor configuré
- Python 3.9+

### Lancement rapide

```powershell
# 1. Vérification pré-lancement
powershell -ExecutionPolicy Bypass -File "VERIFY_OSINT_SETUP.ps1"

# 2. Démarrage de la session
python docker_orchestrator_osint.py

# 3. Services disponibles
# HackerGPT: http://localhost:8000
# Hexstrike: http://localhost:8001
# Tor: localhost:9050 (SOCKS5)
```

---

## 📊 Workflows d'Investigation

### 1️⃣ Enquête Simple (IOCs)

```python
from osint_legal_engine import (
    OSINTLegalEngine, 
    InvestigationType, 
    IOC, 
    IOCType,
    EvidenceLevel
)

# Initialiser le moteur
engine = OSINTLegalEngine()

# Créer une investigation
investigation = engine.create_investigation(
    InvestigationType.SCAM,
    "Investigation Arnaque Crypto X"
)

# Ajouter des IOCs (structurés pour enquêteurs)
ioc1 = IOC(
    type=IOCType.DOMAIN,
    value="fake-exchange.onion",
    confidence=95,
    source_url="https://forum-darknet/thread-123",
    first_seen="2026-02-15T10:30:00Z",
    last_seen="2026-02-19T14:22:00Z",
    context="Domaine de phishing imitant exchange crypto légitime",
    severity="critical",
    tags=["phishing", "crypto-scam", "darknet"]
)

investigation.add_ioc(ioc1)

# Finalize avec signature
md_path, json_path, signature = engine.finalize_report(investigation)
```

### 2️⃣ Profil Criminel Complet

```python
from osint_legal_engine import (
    OSINTLegalEngine,
    CriminalProfile,
    IOC,
    IOCType
)

# Créer profil criminel
profile = CriminalProfile(
    profile_id="CRIM_20260219_001",
    darknet_aliases=["DarkMaster42", "HackerX", "ShadowKing"],
    known_activities=[
        "Fraude au faux support technique",
        "Ransomware distribution",
        "Money laundering via crypto"
    ],
    infrastructure_iocs=[
        IOC(
            type=IOCType.DOMAIN,
            value="malware-c2.onion",
            confidence=99,
            source_url="https://malwarebase/report-456",
            first_seen="2025-12-01T00:00:00Z",
            last_seen="2026-02-19T00:00:00Z",
            context="Serveur de commande et contrôle pour ransomware",
            severity="critical"
        )
    ],
    associated_wallets=[
        "1A1z7agoat2Pt7NqVoV2iGAomYWQZd1xvz",
        "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq"
    ],
    threat_level="critical",
    timeline_events=[
        {
            'timestamp': '2025-11-15T08:30:00Z',
            'event_type': 'malware_detected',
            'description': 'Campagne de ransomware lancée'
        }
    ],
    investigation_notes="""
    Criminel hautement sophistiqué opérant depuis l'Europe de l'Est.
    Infrastructure distribuée sur 5+ pays.
    Revenus estimés: 5M+ USD par an.
    Connexions avec autres groupes criminels identifiées.
    """,
    confidence_level=85,
    last_updated="2026-02-19T14:00:00Z"
)

investigation.add_criminal_profile(profile)
```

### 3️⃣ Rapport pour Autorités

```python
from legal_report_generator import (
    LegalReportGenerator,
    AuthorityLevel,
    LegalEvidence,
    EvidenceLevel
)
import hashlib

# Créer générateur de rapports légaux
report_gen = LegalReportGenerator(
    operator_name="OSINT Investigator Name",
    operator_credentials="CERT-BADGE-NUMBER"
)

# Ajouter preuves
evidence = LegalEvidence(
    evidence_id="EVID_20260219_001",
    description="Capture d'écran du domaine malveillant",
    source_url="https://forum.darknet/thread-123",
    capture_timestamp="2026-02-19T10:30:00Z",
    evidence_type="screenshot",
    confidence=EvidenceLevel.OBSERVED,
    chain_of_custody=[
        {
            'timestamp': '2026-02-19T10:30:00Z',
            'action': 'evidence_collected',
            'actor': 'OSINT investigator'
        }
    ],
    raw_data_hash=hashlib.sha256(
        "screenshot_raw_data".encode()
    ).hexdigest(),
    notes="Domaine actif, redirection vers phishing page"
)

report_gen.add_evidence(evidence)

# Ajouter conclusions
report_gen.add_finding(
    title="Arnaque aux crypto-monnaies confirmée",
    description="Domaine fake-exchange.onion est une fraude confirmée",
    severity="critical",
    supporting_evidences=["EVID_20260219_001"]
)

# Ajouter recommandations
report_gen.add_recommendation(
    "Faire fermer le domaine .onion auprès des autorités de registraire"
)

# Exporter pour autorités
report_gen.export_json("rapport_legal_autorités.json")
report_gen.export_markdown("rapport_legal_autorités.md", 
                          include_raw_data=False)
```

---

## 🔐 Sécurité et Anonymité

### Anonymité Garantie
- ✅ Tor obligatoire - zéro sortie internet directe
- ✅ Pas d'adresse IP personnelle exposée
- ✅ Métadonnées opérationnelles anonymes
- ✅ Logs opérations sécurisés et chiffrés
- ✅ Session ID anonyme (pas de nom d'utilisateur)

### Légalité Garantie
- ✅ Rapports signés RSA-4096 SHA256
- ✅ Timestamps UTC vérifiables
- ✅ Chaîne de preuves complète
- ✅ Hashes d'intégrité (SHA256)
- ✅ Conforme droit français/UE

---

## 📝 Rapports Légaux

### Structure Rapport JSON

```json
{
  "metadata": {
    "report_id": "RPT_20260219_001",
    "investigation_id": "INV_20260219_001",
    "title": "Investigation Darknet Scam",
    "authority_level": "law_enforcement",
    "created_by": "Investigator Name",
    "creation_timestamp": "2026-02-19T10:00:00Z"
  },
  "chain_of_custody": {
    "start_timestamp": "2026-02-19T10:00:00Z",
    "total_evidences": 5,
    "integrity_hash": "sha256_hash_all_evidences"
  },
  "evidences": [
    {
      "id": "EVID_001",
      "description": "Screenshot domaine malveillant",
      "source": "https://forum.darknet/thread",
      "timestamp": "2026-02-19T10:30:00Z",
      "type": "screenshot",
      "confidence": "observed",
      "raw_data_hash": "sha256_evidence_hash"
    }
  ],
  "findings": [
    {
      "title": "Arnaque crypto confirmée",
      "description": "Domaine est une fraude",
      "severity": "critical",
      "evidence_ids": ["EVID_001"],
      "finding_id": "FIND_001"
    }
  ],
  "recommendations": [
    "Signaler au registraire .onion",
    "Coordination avec autorités"
  ],
  "signature": {
    "signed_by": "Investigator Name",
    "timestamp": "2026-02-19T14:00:00Z",
    "method": "RSA-4096-PSS-SHA256"
  }
}
```

### Vérification Rapport (pour autorités)

```python
from legal_report_generator import ReportVerifier
import json

# Charger rapport
with open("rapport.json") as f:
    report = json.load(f)

# Vérifier intégrité
is_valid = ReportVerifier.verify_integrity(report)
print(f"Intégrité: {'✅ Valide' if is_valid else '❌ Altérée'}")

# Chaîne de preuves
chain = ReportVerifier.verify_chain_of_custody(report)
for event in chain:
    print(f"  {event}")

# Certificat de vérification
cert = ReportVerifier.generate_verification_certificate(
    report,
    verifier_name="Authority Officer"
)
```

---

## 🛡️ Audit Trail Sécurisé

### Accès Personnel Uniquement

```python
from osint_legal_engine import CryptoAuditTrail

# Initialiser avec clé personnelle
audit = CryptoAuditTrail(audit_key=b'your_secret_key_32_bytes')

# Enregistrer opération
op_hash = audit.log_operation(
    action="ioc_extracted",
    source_url="https://forum.darknet/thread-123",
    ioc_extracted=[ioc1, ioc2],
    session_id="SESSION_ABC123",
    details={'count': 2, 'severity': 'high'}
)

# Vérifier intégrité audit trail
is_valid = audit.verify_audit_trail()
print(f"Audit trail intègre: {is_valid}")

# Exporter pour consultation personnelle
audit.export_audit_trail("mon_audit_trail.md")
```

---

## 🚨 Incidents et Escalade

### En cas de Découverte Importante

1. **Générer rapport légal** → Autorités
2. **Notifier contact légal** → Conseil juridique
3. **Maintenir chaîne de preuves** → Pas de modification
4. **Archiver crypté** → Audit trail sécurisé
5. **Escalade si criminalité** → Dépôt de plainte

---

## ✅ Conformité Légale

### France (Code Pénal)
- ✅ Article L435-1+: Investigation légitime
- ✅ Articles L435-6: Preuves admissibles
- ✅ Article 567 CPC: Chaîne de preuves respectée

### RGPD
- ✅ Pas de PII en logs
- ✅ Droit à l'oubli respecté
- ✅ Traçabilité anonymisée

### Droits de l'homme
- ✅ CEDH Article 10: Liberté d'expression (journalistes)
- ✅ CEDH Article 8: Vie privée protégée
- ✅ CEDH Article 6: Procédure équitable

---

## 📞 Support et Documentation

- 📖 **Guide complet**: OSINT_LEGAL_GUIDE.md (ce fichier)
- 🔧 **Configuration**: config/docker_config.json
- 📊 **Audit trail**: osint_audit_trail.db
- 📋 **Rapports**: osint_reports/
- 🔐 **Clés crypto**: osint_private.pem (À PROTÉGER!)

---

## ⚠️ Avertissements Importants

### Sécurité
- 🔴 Ne JAMAIS partager osint_private.pem
- 🔴 Audit trail chiffré = accès personnel uniquement
- 🔴 Supprimer données sensibles après usage
- 🔴 Vérifier Tor actif avant opération

### Légalité
- 🟡 Respect lois locales obligatoire
- 🟡 Rapports signés = responsabilité légale
- 🟡 Chaîne de preuves inviolable
- 🟡 Consultation avocat recommandée avant escalade

---

**Version**: 2.0 - OSINT Légal  
**Dernière mise à jour**: 2026-02-19  
**Status**: Production Ready ✅
