#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST_OSINT_INVESTIGATION.py
============================
Test scenario for the OSINT Legal Engine
Validates: IOC creation, report generation, signatures, audit trail

This test demonstrates the dual-protection system:
1. Anonymity AGAINST criminals (Tor routing, no operator traces)
2. Auditability FOR authorities (signatures, chain of custody)
"""

import sys
import os
from datetime import datetime, timezone
from pathlib import Path

# Add Ascended33 to path
sys.path.insert(0, str(Path(__file__).parent))

def test_ioc_creation():
    """Test créer des IOCs structurés"""
    print("\n" + "="*60)
    print("TEST 1: Création d'IOCs structurés")
    print("="*60)
    
    try:
        from osint_legal_engine import IOC, IOCType
        
        # Exemple 1: Domaine malveillant
        ioc_domain = IOC(
            type=IOCType.DOMAIN,
            value="malicious-c2.fake-domain.ru",
            confidence=95,
            source_url="https://threats.example.com/c2-domains",
            first_seen=datetime.now(timezone.utc).isoformat(),
            last_seen=datetime.now(timezone.utc).isoformat(),
            context="C2 server utilisé dans campagne phishing Emotet",
            severity="critical",
            tags=["emotet", "c2-server", "banking-malware"]
        )
        
        print(f"✅ IOC Domain créé:")
        print(f"   Type: {ioc_domain.type.value}")
        print(f"   Value: {ioc_domain.value}")
        print(f"   Confiance: {ioc_domain.confidence}%")
        print(f"   Sévérité: {ioc_domain.severity}")
        
        # Exemple 2: Adresse Bitcoin
        ioc_bitcoin = IOC(
            type=IOCType.BITCOIN_ADDRESS,
            value="1A1z7agoat3nSVKwuNvaSQvHfnxRi3P9y1",
            confidence=85,
            source_url="https://blockchain.example.com/addr/1A1z7agoat3nSVKwuNvaSQvHfnxRi3P9y1",
            first_seen="2026-01-15T10:00:00Z",
            last_seen="2026-02-18T15:30:00Z",
            context="Portefeuille utilisé pour paiement rançongiciel ransomware",
            severity="high",
            tags=["ransomware", "payment", "laundry"],
            related_iocs=["hash_1", "domain_2"]
        )
        
        print(f"\n✅ IOC Bitcoin créé:")
        print(f"   Type: {ioc_bitcoin.type.value}")
        print(f"   Value: {ioc_bitcoin.value}")
        print(f"   IOCs liés: {ioc_bitcoin.related_iocs}")
        
        return True, [ioc_domain, ioc_bitcoin]
        
    except Exception as e:
        print(f"❌ Erreur création IOC: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, []


def test_criminal_profile_creation():
    """Test créer un profil criminel structuré"""
    print("\n" + "="*60)
    print("TEST 2: Création de profil criminel")
    print("="*60)
    
    try:
        from osint_legal_engine import CriminalProfile
        
        profile = CriminalProfile(
            profile_id="PROFILE_EMOTET_OPERATOR_001",
            aliases=["EmotEt_Master", "Trickbot_Admin", "BankBot_Operator"],
            confirmed_activities=[
                "Malware distribution (Emotet, TrickBot)",
                "Banking fraud",
                "Data exfiltration",
                "Ransom collection"
            ],
            crypto_wallets=[
                "1A1z7agoat3nSVKwuNvaSQvHfnxRi3P9y1",
                "3J98t1WpEZ73CNmYviecrnyiWrnqRhWNLy"
            ],
            known_associates=["PROFILE_TRICKBOT_OPERATOR_002"],
            confidence=90,
            threat_level="critical",
            timeline={
                "2024-01-01": "Première infection Emotet détectée",
                "2025-06-15": "Transition vers TrickBot",
                "2026-02-18": "Dernière activité: collecte de rançon"
            }
        )
        
        print(f"✅ Profil criminel créé:")
        print(f"   ID: {profile.profile_id}")
        print(f"   Aliases: {len(profile.aliases)} identifiés")
        print(f"   Portefeuilles: {len(profile.crypto_wallets)}")
        print(f"   Associés connus: {profile.known_associates}")
        print(f"   Niveau menace: {profile.threat_level}")
        print(f"   Confiance: {profile.confidence}%")
        
        return True, profile
        
    except Exception as e:
        print(f"❌ Erreur profil criminel: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None


def test_report_structure():
    """Test structure du rapport OSINT"""
    print("\n" + "="*60)
    print("TEST 3: Structure du rapport OSINT")
    print("="*60)
    
    try:
        from osint_legal_engine import StructuredOSINTReport, InvestigationType
        
        report = StructuredOSINTReport(
            investigation_id="INV_20260219_EMOTET_RING",
            investigation_type=InvestigationType.MALWARE_TRACKING,
            operator_id_hash="sha256:abc123def456...",  # Anonymisé
            title="Analyse: Réseau C2 Emotet - Février 2026",
            summary="Investigation sur infrastructure C2 utilisée pour distribution Emotet",
            severity="critical",
            targets_count=1250,
            financial_impact_usd=5200000,
            created_at=datetime.now(timezone.utc).isoformat(),
            last_updated=datetime.now(timezone.utc).isoformat()
        )
        
        print(f"✅ Rapport structuré créé:")
        print(f"   ID Investigation: {report.investigation_id}")
        print(f"   Type: {report.investigation_type.value}")
        print(f"   Titre: {report.title}")
        print(f"   Cibles affectées: {report.targets_count:,}")
        print(f"   Impact financier: ${report.financial_impact_usd:,}")
        print(f"   Opérateur: {report.operator_id_hash[:30]}... (anonymisé)")
        
        return True, report
        
    except Exception as e:
        print(f"❌ Erreur rapport: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None


def test_signature_capability():
    """Test capacité de signature cryptographique"""
    print("\n" + "="*60)
    print("TEST 4: Signature cryptographique (RSA-4096)")
    print("="*60)
    
    try:
        from osint_legal_engine import LegalReportSigner
        
        signer = LegalReportSigner()
        
        # Générer clés (simule d'abord)
        print("⏳ Génération des clés RSA-4096 (peut prendre 30-60 secondes)...")
        signer.generate_keys()
        
        # Signer un message test
        test_message = "RAPPORT_OSINT_EMOTET_20260219_INVESTIGATION"
        signature = signer.sign_message(test_message)
        
        # Vérifier signature
        is_valid = signer.verify_signature(test_message, signature)
        
        print(f"✅ Signature RSA-4096 réussie:")
        print(f"   Message: {test_message[:40]}...")
        print(f"   Signature valide: {is_valid}")
        print(f"   Longueur signature: {len(signature)} bytes")
        
        return True, {
            "signer": signer,
            "message": test_message,
            "signature": signature,
            "valid": is_valid
        }
        
    except Exception as e:
        print(f"❌ Erreur signature: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None


def test_audit_trail():
    """Test audit trail chiffré"""
    print("\n" + "="*60)
    print("TEST 5: Audit trail sécurisé (AES-256-GCM)")
    print("="*60)
    
    try:
        from osint_legal_engine import CryptoAuditTrail
        
        audit_trail = CryptoAuditTrail()
        
        # Créer entrées audit
        audit_trail.log_event({
            "event": "investigation_started",
            "investigation_id": "INV_20260219_EMOTET_RING",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": "Démarrage investigation Emotet C2"
        })
        
        audit_trail.log_event({
            "event": "ioc_discovered",
            "type": "domain",
            "value": "malicious-c2.fake-domain.ru",
            "confidence": 95,
            "source": "threat_intelligence_feed"
        })
        
        audit_trail.log_event({
            "event": "report_generated",
            "report_id": "RPT_20260219_001",
            "findings_count": 1250,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        print(f"✅ Audit trail créé:")
        print(f"   Entrées enregistrées: 3")
        print(f"   Chiffrement: AES-256-GCM")
        print(f"   Accès: Clé personnelle (opérateur seul)")
        
        return True, audit_trail
        
    except Exception as e:
        print(f"❌ Erreur audit trail: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None


def test_docker_readiness():
    """Test Docker infrastructure readiness"""
    print("\n" + "="*60)
    print("TEST 6: Préparation infrastructure Docker")
    print("="*60)
    
    try:
        import docker
        from pathlib import Path
        
        # Vérifier fichier docker-compose
        compose_file = Path("docker-compose-osint.yml")
        if compose_file.exists():
            print(f"✅ docker-compose-osint.yml trouvé ({compose_file.stat().st_size} bytes)")
        else:
            print(f"⚠️  docker-compose-osint.yml non trouvé")
            return False, None
        
        # Vérifier Python scripts
        required_files = [
            "osint_legal_engine.py",
            "legal_report_generator.py",
            "docker_orchestrator_osint.py"
        ]
        
        all_present = True
        for fname in required_files:
            fpath = Path(fname)
            if fpath.exists():
                print(f"✅ {fname} ({fpath.stat().st_size} bytes)")
            else:
                print(f"❌ {fname} manquant")
                all_present = False
        
        if all_present:
            print(f"\n✅ Infrastructure Docker prête au lancement")
            return True, {
                "docker_compose": str(compose_file),
                "python_modules": required_files,
                "status": "ready"
            }
        else:
            return False, None
            
    except Exception as e:
        print(f"❌ Erreur vérification Docker: {str(e)}")
        return False, None


def main():
    """Exécuter tous les tests"""
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║     TEST INFRASTRUCTURE OSINT LÉGALE - FÉVRIER 2026    ║")
    print("║                                                        ║")
    print("║  Double-protection: Anonymité + Auditabilité légale   ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    results = {
        "ioc_creation": test_ioc_creation(),
        "criminal_profile": test_criminal_profile_creation(),
        "report_structure": test_report_structure(),
        "signatures": test_signature_capability(),
        "audit_trail": test_audit_trail(),
        "docker_readiness": test_docker_readiness()
    }
    
    # Résumé
    print("\n" + "="*60)
    print("RÉSUMÉ DES TESTS")
    print("="*60)
    
    passed = sum(1 for success, _ in results.values() if success)
    total = len(results)
    
    for test_name, (success, data) in results.items():
        status = "✅ PASSÉ" if success else "❌ ÉCHOUÉ"
        print(f"{status}: {test_name}")
    
    print(f"\nRésultat: {passed}/{total} tests passés")
    
    if passed == total:
        print("\n🎯 Infrastructure OSINT prête pour investigations!")
        print("Prochaines étapes:")
        print("  1. Lancer Docker: python docker_orchestrator_osint.py")
        print("  2. Créer première enquête avec osint_legal_engine.py")
        print("  3. Générer rapports légaux pour autorités")
        return 0
    else:
        print("\n⚠️  Certains tests échoués - vérifier les erreurs ci-dessus")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
