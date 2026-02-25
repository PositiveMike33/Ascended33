#!/usr/bin/env python3
"""
Script d'exploration du projet Vault
Scanne la structure, dépendances, backend et configuration
"""
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
def scan_directory_structure(root_path):
    """Scanne la structure des répertoires"""
    structure = {}
    for root, dirs, files in os.walk(root_path):
        # Ignore les dossiers inutiles
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv', '.streamlit']]
        level = root.replace(root_path, '').count(os.sep)
        indent = ' ' * 2 * level
        rel_path = os.path.relpath(root, root_path)
        structure[rel_path] = {
            'files': files[:10],  # Limite à 10 fichiers
            'subdirs': dirs[:10]
        }
    return structure
def find_streamlit_apps(root_path):
    """Trouve tous les fichiers Streamlit (app.py, *_app.py, pages/*.py)"""
    streamlit_files = []
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'venv']]
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                # Vérifier si c'est un fichier Streamlit
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(1000)
                    if 'streamlit' in content.lower() or 'st.' in content:
                        streamlit_files.append(full_path)
    return streamlit_files
def find_requirements_files(root_path):
    """Trouve requirements.txt, pyproject.toml, setup.py"""
    req_files = {}
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv']]
        for file in ['requirements.txt', 'pyproject.toml', 'setup.py', 'setup.cfg', 'Pipfile', 'poetry.lock']:
            if file in files:
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    req_files[full_path] = f.read()
    return req_files
def find_backend_files(root_path):
    """Identifie les fichiers backend (Flask, FastAPI, Django, etc.)"""
    backend_indicators = {
        'fastapi': ['main.py', 'app.py', 'server.py'],
        'flask': ['app.py', 'application.py'],
        'django': ['manage.py', 'settings.py'],
        'custom_api': ['api.py', 'server.py', 'backend.py']
    }
    found_backends = {}
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'node_modules']]
        for backend_type, indicators in backend_indicators.items():
            for indicator in indicators:
                if indicator in files:
                    full_path = os.path.join(root, indicator)
                    if full_path not in found_backends.values():
                        found_backends[full_path] = backend_type
    return found_backends
def find_docker_files(root_path):
    """Trouve docker-compose.yml, Dockerfile"""
    docker_files = {}
    for root, dirs, files in os.walk(root_path):
        for file in ['docker-compose.yml', 'docker-compose.yaml', 'Dockerfile']:
            if file in files:
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    docker_files[full_path] = f.read()
    return docker_files
def check_running_services():
    """Vérifie les services Docker en cours d'exécution"""
    try:
        result = subprocess.run(['docker', 'ps', '--format', 'json'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            containers = json.loads('[' + ','.join(result.stdout.strip().split('\\n')) + ']')
            return containers
    except:
        pass
    return []
def main():
    root_path = "D:/Vault/Vault"
    print("=" * 80)
    print("🔍 SCAN DU PROJET VAULT - Démarrage")
    print("=" * 80)
    print(f"\\n📂 Répertoire racine: {root_path}\\n")
    # 1. Structure générale
    print("1️⃣  Structure du projet:")
    print("-" * 80)
    structure = scan_directory_structure(root_path)
    print(json.dumps(structure, indent=2, ensure_ascii=False)[:2000])
    # 2. Applications Streamlit
    print("\\n\\n2️⃣  Applications Streamlit trouvées:")
    print("-" * 80)
    streamlit_apps = find_streamlit_apps(root_path)
    for app in streamlit_apps:
        print(f"  ✓ {app}")
    # 3. Fichiers de dépendances
    print("\\n\\n3️⃣  Fichiers de dépendances:")
    print("-" * 80)
    req_files = find_requirements_files(root_path)
    for req_file, content in req_files.items():
        print(f"\\n📄 {req_file}:")
        print(content[:1500])
    # 4. Backend
    print("\\n\\n4️⃣  Fichiers Backend détectés:")
    print("-" * 80)
    backends = find_backend_files(root_path)
    for backend_file, backend_type in backends.items():
        print(f"  ✓ {backend_type}: {backend_file}")
    # 5. Docker
    print("\\n\\n5️⃣  Configuration Docker:")
    print("-" * 80)
    docker_files = find_docker_files(root_path)
    for docker_file, content in docker_files.items():
        print(f"\\n📄 {docker_file}:")
        print(content)
    # 6. Services Docker actifs
    print("\\n\\n6️⃣  Conteneurs Docker actifs:")
    print("-" * 80)
    containers = check_running_services()
    if containers:
        for container in containers[:10]:
            print(f"  ✓ {container.get('Names', 'Unknown')} ({container.get('Image', 'N/A')})")
    else:
        print("  ⚠️  Aucun conteneur Docker détecté ou Docker non disponible")
    print("\\n" + "=" * 80)
    print("✅ Scan terminé")
    print("=" * 80)
if __name__ == "__main__":
    main()