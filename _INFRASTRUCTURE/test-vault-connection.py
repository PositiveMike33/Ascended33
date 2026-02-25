#!/usr/bin/env python3
"""
Test Vault Connection - Diagnostic Script
Checks connectivity between Streamlit, HexStrike, Obsidian Vault, and Docker containers
"""

import sys
import os
import subprocess
import socket
from pathlib import Path
from datetime import datetime

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_result(name, status, details=""):
    """Print test result"""
    symbol = "[OK]" if status else "[FAIL]"
    print(f"{symbol} {name}")
    if details:
        print(f"   -> {details}")

def test_port(host, port, service_name):
    """Test if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False

def test_vault_path():
    """Test if vault path exists"""
    vault_path = Path("/vault")
    if vault_path.exists():
        return True, str(vault_path.absolute())
    
    # Check Windows mount
    vault_path_win = Path("D:\\Vault\\Vault")
    if vault_path_win.exists():
        return True, str(vault_path_win.absolute())
    
    return False, "Not found"

def test_docker_containers():
    """Test if Docker containers are running"""
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        containers = result.stdout.strip().split('\n')
        return containers
    except Exception as e:
        return []

def test_python_modules():
    """Test if required Python modules are available"""
    modules = {
        'streamlit': False,
        'yaml': False,
        'pandas': False,
        'plotly': False,
        'requests': False,
        'altair': False,
    }
    
    for module in modules:
        try:
            __import__(module)
            modules[module] = True
        except ImportError:
            modules[module] = False
    
    return modules

def main():
    print_header("VAULT CONNECTION DIAGNOSTIC TEST")
    print(f"Timestamp: {datetime.now().isoformat()}\n")
    
    # 1. Check Vault Path
    print_header("1. VAULT PATH")
    vault_exists, vault_path = test_vault_path()
    print_result("Vault path accessible", vault_exists, vault_path)
    
    # 2. Check Network Services
    print_header("2. NETWORK SERVICES")
    
    services = [
        ("Streamlit", "localhost", 8501),
        ("HexStrike UI", "localhost", 8001),
        ("HexStrike-AI", "localhost", 8888),
        ("Obsidian REST API", "localhost", 27123),
        ("Tor SOCKS5", "localhost", 9050),
        ("Kali VNC", "localhost", 5901),
    ]
    
    online_services = 0
    for service_name, host, port in services:
        is_open = test_port(host, port, service_name)
        print_result(f"{service_name} (:{port})", is_open)
        if is_open:
            online_services += 1
    
    print(f"\n=> Online services: {online_services}/{len(services)}")
    
    # 3. Check Docker Containers
    print_header("3. DOCKER CONTAINERS")
    
    try:
        containers = test_docker_containers()
        expected_containers = [
            "th3-streamlit",
            "th3-hexstrike",
            "th3-kali",
            "th3-tor",
            "vault-sync",
        ]
        
        if containers and containers[0]:
            print(f"Found {len(containers)} running containers:\n")
            for container in containers:
                if container:
                    is_expected = any(exp in container for exp in expected_containers)
                    status = "[OK]" if is_expected else "[WARN]"
                    print(f"  {status} {container}")
        else:
            print("[FAIL] No Docker containers detected")
            print("   => Is Docker running?")
    except Exception as e:
        print(f"[FAIL] Cannot access Docker: {e}")
    
    # 4. Check Python Modules
    print_header("4. PYTHON MODULES")
    
    modules = test_python_modules()
    missing_modules = []
    
    for module, available in modules.items():
        print_result(f"Module: {module}", available)
        if not available:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n[WARN] Missing modules: {', '.join(missing_modules)}")
        print("   Run: pip install -r requirements.txt")
    
    # 5. Check Files
    print_header("5. KEY FILES")
    
    files_to_check = [
        ("streamlit_app.py", "Streamlit dashboard"),
        ("requirements.txt", "Python dependencies"),
        ("docker-compose.yml", "Container configuration"),
        ("Instructions Claude — HexStrike THIRTY3.md", "HexStrike guidelines"),
    ]
    
    for filename, description in files_to_check:
        file_path = Path(filename)
        exists = file_path.exists()
        print_result(f"{description}", exists, filename)
    
    # 6. Summary
    print_header("DIAGNOSTIC SUMMARY")
    
    print("[OK] All systems nominal" if all([vault_exists, online_services >= 4]) else "[WARN] Some issues detected")
    
    if missing_modules:
        print(f"\n[ACTION REQUIRED]")
        print(f"   Install missing modules:")
        print(f"   $ pip install {' '.join(missing_modules)}")
    
    if online_services < len(services):
        print(f"\n[ACTION REQUIRED]")
        print(f"   Start Docker containers:")
        print(f"   $ docker-compose up -d")
    
    print(f"\n[NEXT STEPS]")
    print(f"   1. Ensure all containers are running")
    print(f"   2. Install all Python modules")
    print(f"   3. Start Streamlit: streamlit run streamlit_app.py")
    print(f"   4. Access dashboard: http://localhost:8501")
    print()

if __name__ == "__main__":
    main()
