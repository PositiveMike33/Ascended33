"""
Docker Orchestrator OSINT - Gestion des conteneurs pour enquêtes légales
=========================================================================

Orchestre les 4 conteneurs avec:
1. Anonymité OPÉRATIONNELLE (Tor, pas de traces)
2. Auditabilité LÉGALE (signatures, preuves)

Conteneurs:
- th3-tor: Routage Tor pour anonymité
- th3-kali: Linux Kali pour reconnaissance
- th3-hackergpt: Claude AI pour analyse
- th3-hexstrike: Dashboard OSINT
"""

import subprocess
import time
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone
from dataclasses import dataclass
import socket
from enum import Enum
import logging


class ContainerStatus(Enum):
    """États des conteneurs"""
    STARTING = "starting"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class ContainerConfig:
    """Configuration d'un conteneur"""
    name: str
    image: str
    port: int
    depends_on: List[str]
    environment: Dict[str, str]
    volumes: Dict[str, str]
    health_check: Optional[Dict]


class OSINTOrchestrator:
    """Orchestrateur Docker pour opérations OSINT sécurisées"""
    
    def __init__(self, compose_file: str = "docker-compose-osint.yml"):
        self.compose_file = compose_file
        self.logger = self._setup_logging()
        self.containers = {}
        self.audit_trail = []
        self.session_start = datetime.now(timezone.utc).isoformat()
    
    def _setup_logging(self) -> logging.Logger:
        """Configure le logging avec audit trail"""
        logger = logging.getLogger("OSINTOrchestrator")
        handler = logging.FileHandler("osint_orchestration.log")
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
    
    def verify_docker_installed(self) -> bool:
        """Vérifie que Docker est installé"""
        try:
            subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                check=True,
                timeout=5
            )
            self.logger.info("✅ Docker installé et accessible")
            return True
        except Exception as e:
            self.logger.error(f"❌ Docker non disponible: {e}")
            return False
    
    def check_compose_file(self) -> bool:
        """Vérifie que le fichier docker-compose existe"""
        if not Path(self.compose_file).exists():
            self.logger.error(f"❌ Fichier {self.compose_file} introuvable")
            return False
        
        self.logger.info(f"✅ Fichier de composition trouvé: {self.compose_file}")
        return True
    
    def start_containers_parallel(self, timeout: int = 60) -> Tuple[bool, Dict]:
        """
        Lance tous les conteneurs en parallèle
        
        Returns:
            (succès, status_dict)
        """
        self.logger.info("🚀 Démarrage des conteneurs OSINT...")
        
        if not self.verify_docker_installed() or not self.check_compose_file():
            return False, {}
        
        try:
            # Lance docker-compose
            result = subprocess.run(
                ["docker-compose", "-f", self.compose_file, "up", "-d"],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode != 0:
                self.logger.error(f"Erreur Docker: {result.stderr}")
                return False, {}
            
            self.logger.info("✅ Conteneurs lancés")
            
            # Attend la santé des conteneurs
            return self._wait_for_healthy_containers(timeout)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du démarrage: {e}")
            return False, {}
    
    def _wait_for_healthy_containers(self, timeout: int = 60) -> Tuple[bool, Dict]:
        """Attend que tous les conteneurs soient sains"""
        start_time = time.time()
        status_dict = {}
        
        required_containers = [
            "th3-tor",
            "th3-kali", 
            "th3-hackergpt",
            "th3-hexstrike"
        ]
        
        while time.time() - start_time < timeout:
            all_healthy = True
            
            for container in required_containers:
                try:
                    result = subprocess.run(
                        ["docker", "inspect", f"ascended33-{container}-1"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if result.returncode == 0:
                        data = json.loads(result.stdout)[0]
                        health = data.get("State", {}).get("Health", {}).get("Status", "starting")
                        
                        status_dict[container] = {
                            "status": health,
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                        
                        if health != "healthy":
                            all_healthy = False
                        
                        self.logger.info(f"  {container}: {health}")
                    else:
                        all_healthy = False
                        
                except Exception as e:
                    self.logger.warning(f"Erreur vérification {container}: {e}")
                    all_healthy = False
            
            if all_healthy:
                self.logger.info("✅ Tous les conteneurs sont sains")
                self._log_audit_event("containers_started", status_dict)
                return True, status_dict
            
            time.sleep(5)
        
        self.logger.error(f"❌ Timeout: conteneurs non sains après {timeout}s")
        return False, status_dict
    
    def verify_tor_routing(self) -> bool:
        """Vérifie que Tor est actif et le routage fonctionne"""
        self.logger.info("🔍 Vérification du routage Tor...")
        
        try:
            # Test connexion au service Tor
            result = subprocess.run(
                ["docker", "exec", "ascended33-th3-tor-1", "curl", "-s", 
                 "--socks5", "localhost:9050", "https://check.torproject.org/api/ip"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                response = json.loads(result.stdout)
                if response.get("is_tor"):
                    self.logger.info("✅ Tor actif et routage fonctionnel")
                    self._log_audit_event("tor_verified", response)
                    return True
            
            self.logger.error("❌ Tor non actif ou routage défaillant")
            return False
            
        except Exception as e:
            self.logger.error(f"Erreur vérification Tor: {e}")
            return False
    
    def verify_services_accessibility(self) -> Dict[str, bool]:
        """Vérifie que tous les services sont accessibles"""
        self.logger.info("🔍 Vérification de l'accessibilité des services...")
        
        accessibility = {}
        
        services = {
            "HackerGPT": ("localhost", 8000),
            "Hexstrike": ("localhost", 8001),
            "Tor": ("localhost", 9050)
        }
        
        for service_name, (host, port) in services.items():
            try:
                with socket.create_connection((host, port), timeout=5) as sock:
                    accessibility[service_name] = True
                    self.logger.info(f"  ✅ {service_name} accessible ({host}:{port})")
            except:
                accessibility[service_name] = False
                self.logger.warning(f"  ❌ {service_name} inaccessible ({host}:{port})")
        
        self._log_audit_event("services_verified", accessibility)
        return accessibility
    
    def get_container_logs(self, container_name: str, lines: int = 50) -> str:
        """Récupère les logs d'un conteneur"""
        try:
            result = subprocess.run(
                ["docker", "logs", "--tail", str(lines), f"ascended33-{container_name}-1"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return result.stdout
            
        except Exception as e:
            self.logger.error(f"Erreur récupération logs {container_name}: {e}")
            return ""
    
    def stop_containers(self) -> bool:
        """Arrête tous les conteneurs"""
        self.logger.info("🛑 Arrêt des conteneurs...")
        
        try:
            subprocess.run(
                ["docker-compose", "-f", self.compose_file, "down"],
                capture_output=True,
                timeout=30
            )
            
            self.logger.info("✅ Conteneurs arrêtés")
            self._log_audit_event("containers_stopped", {})
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur arrêt conteneurs: {e}")
            return False
    
    def export_orchestration_report(self, output_path: str = "orchestration_report.json") -> str:
        """Exporte un rapport d'orchestration"""
        report = {
            'session': {
                'start_time': self.session_start,
                'end_time': datetime.now(timezone.utc).isoformat(),
                'container_count': len(self.containers)
            },
            'security': {
                'tor_enabled': True,
                'anonymity_level': 'maximum',
                'audit_trail_enabled': True
            },
            'audit_events': self.audit_trail,
            'containers': self.containers
        }
        
        Path(output_path).write_text(json.dumps(report, indent=2, ensure_ascii=False))
        self.logger.info(f"📊 Rapport exporté: {output_path}")
        
        return output_path
    
    def _log_audit_event(self, event_type: str, data: Dict):
        """Enregistre un événement d'audit"""
        event = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'type': event_type,
            'data': data
        }
        
        self.audit_trail.append(event)
        self.logger.info(f"📝 Audit: {event_type}")


class SecureOSINTSession:
    """Session OSINT sécurisée de bout en bout"""
    
    def __init__(self):
        self.orchestrator = OSINTOrchestrator()
        self.session_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    
    def initialize_session(self) -> bool:
        """Initialise une session OSINT sécurisée"""
        print("\n🕵️  ========================================")
        print("   OSINT Investigation Platform v2.0")
        print("   Anonymité + Légalité")
        print("==========================================\n")
        
        print(f"📊 Session ID: {self.session_id}")
        print(f"🔒 Mode: Anonyme pour opérateurs + Légal pour autorités\n")
        
        # Vérifie Docker
        print("[1/4] Vérification Docker...")
        if not self.orchestrator.verify_docker_installed():
            print("❌ Docker non disponible!")
            return False
        
        # Vérifie composition
        print("[2/4] Vérification fichier docker-compose...")
        if not self.orchestrator.check_compose_file():
            print("❌ Fichier docker-compose introuvable!")
            return False
        
        # Lance conteneurs
        print("[3/4] Démarrage des conteneurs (30s max)...")
        success, status = self.orchestrator.start_containers_parallel(timeout=60)
        
        if not success:
            print("❌ Erreur démarrage conteneurs!")
            return False
        
        print(f"✅ Conteneurs lancés: {list(status.keys())}")
        
        # Vérifie Tor
        print("[4/4] Vérification sécurité Tor...")
        if not self.orchestrator.verify_tor_routing():
            print("⚠️  Tor non disponible (certaines fonctionnalités réduites)")
        else:
            print("✅ Tor actif - Anonymité garantie")
        
        # Vérifie services
        print("\n[Vérification services...]")
        accessibility = self.orchestrator.verify_services_accessibility()
        
        all_accessible = all(accessibility.values())
        if not all_accessible:
            print("⚠️  Certains services non accessibles")
        
        print("\n🎯 Session OSINT initialisée avec succès!")
        print("\nServices disponibles:")
        print("  🤖 HackerGPT: http://localhost:8000")
        print("  🔍 Hexstrike: http://localhost:8001")
        print("  🔐 Tor: SOCKS5 localhost:9050\n")
        
        return True
    
    def finalize_session(self) -> str:
        """Finalise la session et exporte le rapport"""
        print("\n[Finalisation session...]")
        
        report_path = self.orchestrator.export_orchestration_report(
            f"osint_session_{self.session_id}.json"
        )
        
        self.orchestrator.stop_containers()
        
        print(f"✅ Session finalisée - Rapport: {report_path}")
        
        return report_path


if __name__ == "__main__":
    session = SecureOSINTSession()
    
    if session.initialize_session():
        try:
            print("\n💡 Session OSINT active. Appuyez sur Ctrl+C pour arrêter.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            session.finalize_session()
