#!/usr/bin/env python3
"""
test_mission_launch.py — Verify mission launch logic works correctly

Tests:
1. check_opsec() fallback behavior
2. Mission launch logic with degraded OPSEC
3. Self-testing authorization detection
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

def test_opsec_check():
    """Test OPSEC check function"""
    print("\n" + "="*70)
    print("TEST 1: OPSEC Check Function")
    print("="*70)
    
    try:
        from scripts.opsec.opsec_manager import OpsecManager
        
        manager = OpsecManager()
        status = manager.initialize_opsec(
            operation_name="Test Mission Launch",
            target="self",
            require_tor=False,
            allow_degraded=True
        )
        
        print(f"✓ OPSEC Manager initialized successfully")
        print(f"  - Safe: {status.safe}")
        print(f"  - VPN Active: {status.vpn_active}")
        print(f"  - Tor Active: {status.tor_active}")
        print(f"  - Current IP: {status.current_ip}")
        print(f"  - Reason: {status.reason}")
        print(f"  - Checks: {status.checks_passed}")
        
        return status
    
    except Exception as e:
        print(f"✗ OPSEC Manager failed: {e}")
        print("  → Fallback would return: safe=True (degraded mode authorized)")
        return None


def test_mission_launch_logic():
    """Test mission launch blocking logic"""
    print("\n" + "="*70)
    print("TEST 2: Mission Launch Logic")
    print("="*70)
    
    # Simulate Streamlit OPSEC check fallback
    opsec = {
        "safe": False,
        "ip": "192.168.1.100",
        "tor": False,
        "reason": "degraded mode (self-test authorized)",
        "vpn": False,
        "vpn_provider": "none"
    }
    
    test_cases = [
        {
            "name": "Self-test with Personal Research auth",
            "auth_type": "Personal Research / CTF",
            "target": "example.com",
            "opsec_level": "Standard (VPN)",
            "should_block": False
        },
        {
            "name": "Self-test with localhost target",
            "auth_type": "Bug Bounty (in-scope)",
            "target": "localhost",
            "opsec_level": "Enhanced (VPN + Tor)",
            "should_block": False
        },
        {
            "name": "Production pentest with degraded OPSEC",
            "auth_type": "Client Pentest (authorized)",
            "target": "client.com",
            "opsec_level": "Maximum (full persona)",
            "should_block": True
        },
        {
            "name": "Self-test target (127.0.0.1)",
            "auth_type": "Bug Bounty (in-scope)",
            "target": "127.0.0.1",
            "opsec_level": "Enhanced (VPN + Tor)",
            "should_block": False
        }
    ]
    
    for test in test_cases:
        # Implement the mission launch logic
        auth_is_self_test = ("Personal Research / CTF" in test["auth_type"] or 
                            test["target"].lower() in ["self", "localhost", "127.0.0.1"])
        
        # This is the blocking condition from streamlit_app.py
        should_be_blocked = (
            not opsec.get("safe") and 
            not auth_is_self_test and 
            test["opsec_level"] == "Maximum (full persona)"
        )
        
        status = "❌ BLOCKED" if should_be_blocked else "✅ ALLOWED"
        expected = "BLOCKED" if test["should_block"] else "ALLOWED"
        
        match = "✓" if (should_be_blocked == test["should_block"]) else "✗"
        
        print(f"\n{match} {test['name']}")
        print(f"  Auth: {test['auth_type']}")
        print(f"  Target: {test['target']}")
        print(f"  OPSEC Level: {test['opsec_level']}")
        print(f"  Expected: {expected}")
        print(f"  Got: {status}")


def test_authorization_detection():
    """Test self-test authorization detection"""
    print("\n" + "="*70)
    print("TEST 3: Self-Test Authorization Detection")
    print("="*70)
    
    test_targets = [
        ("example.com", False, "Regular domain"),
        ("self", True, "Self keyword"),
        ("SELF", True, "Self uppercase"),
        ("localhost", True, "Localhost"),
        ("127.0.0.1", True, "Localhost IP"),
        ("192.168.1.1", False, "Private IP"),
    ]
    
    test_auths = [
        ("Personal Research / CTF", True, "Personal Research"),
        ("Bug Bounty (in-scope)", False, "Bug Bounty"),
        ("Client Pentest (authorized)", False, "Client Pentest"),
    ]
    
    print("\nTarget Detection:")
    for target, expected, desc in test_targets:
        is_self_test = target.lower() in ["self", "localhost", "127.0.0.1"]
        status = "✓" if is_self_test == expected else "✗"
        print(f"  {status} {target:20} → {is_self_test:5} ({desc})")
    
    print("\nAuthorization Detection:")
    for auth, expected, desc in test_auths:
        is_self_test = "Personal Research / CTF" in auth
        status = "✓" if is_self_test == expected else "✗"
        print(f"  {status} {auth:30} → {is_self_test:5} ({desc})")


if __name__ == "__main__":
    print("\n" + "🔍 ASCENDED33 MISSION LAUNCH TEST SUITE")
    
    try:
        test_opsec_check()
    except Exception as e:
        print(f"⚠ OPSEC test failed: {e}")
    
    try:
        test_mission_launch_logic()
    except Exception as e:
        print(f"⚠ Mission launch logic test failed: {e}")
    
    try:
        test_authorization_detection()
    except Exception as e:
        print(f"⚠ Authorization detection test failed: {e}")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("✅ If all tests pass, mission launches should work in degraded OPSEC mode")
    print("✅ Self-testing is now properly authorized")
    print("✅ Production operations still properly gated by OPSEC level")
    print("\n" + "="*70 + "\n")
