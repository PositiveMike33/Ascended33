"""
JOUR 2 Complete Validation Suite
Validates all 5 JOUR 2 modules with comprehensive testing
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

# Project paths
PROJECT_ROOT = Path(__file__).parent
TESTS_DIR = PROJECT_ROOT / "tests"
CORE_DIR = PROJECT_ROOT / "core"

# Test files to run
TEST_FILES = [
    "test_multi_user_orchestrator.py",
    "test_docker_containerization.py",
    "test_rsa_cryptographic_system.py",
    "test_audit_trail_system.py",
    "test_user_session_management.py"
]

# Module descriptions
MODULE_DESCRIPTIONS = {
    "test_multi_user_orchestrator.py": "Multi-user Orchestrator (712 lines)",
    "test_docker_containerization.py": "Docker Containerization (558 lines)",
    "test_rsa_cryptographic_system.py": "RSA-4096 Cryptographic System (479 lines)",
    "test_audit_trail_system.py": "Audit Trail System (513 lines)",
    "test_user_session_management.py": "User Session Management (525 lines)"
}

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")

def print_section(text):
    """Print formatted section"""
    print("\n" + "-" * 80)
    print(text)
    print("-" * 80)

def verify_modules_exist():
    """Verify all core modules exist"""
    print_section("VERIFICATION: Checking core module files...")
    
    required_modules = [
        "multi_user_orchestrator.py",
        "docker_containerization.py",
        "rsa_cryptographic_system.py",
        "audit_trail_system.py",
        "user_session_management.py"
    ]
    
    all_exist = True
    for module in required_modules:
        module_path = CORE_DIR / module
        status = "PASS" if module_path.exists() else "FAIL"
        size = f"({module_path.stat().st_size} bytes)" if module_path.exists() else "(MISSING)"
        print(f"  [{status}] {module:<40} {size}")
        if not module_path.exists():
            all_exist = False
    
    return all_exist

def verify_test_files_exist():
    """Verify all test files exist"""
    print_section("VERIFICATION: Checking test files...")
    
    all_exist = True
    for test_file in TEST_FILES:
        test_path = TESTS_DIR / test_file
        status = "PASS" if test_path.exists() else "FAIL"
        size = f"({test_path.stat().st_size} bytes)" if test_path.exists() else "(MISSING)"
        print(f"  [{status}] {test_file:<45} {size}")
        if not test_path.exists():
            all_exist = False
    
    return all_exist

def run_pytest_tests():
    """Run all pytest tests"""
    print_section("EXECUTION: Running pytest test suites...")
    
    results = {}
    total_tests = 0
    total_passed = 0
    
    for test_file in TEST_FILES:
        test_path = TESTS_DIR / test_file
        module_name = MODULE_DESCRIPTIONS.get(test_file, test_file)
        
        print(f"\nTesting {module_name}...")
        print(f"  Path: {test_path}")
        
        try:
            # Run pytest with verbose output
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_path), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Parse output for pass/fail count
            output = result.stdout + result.stderr
            
            # Extract test counts
            import re
            passed_match = re.search(r"(\d+) passed", output)
            failed_match = re.search(r"(\d+) failed", output)
            
            passed = int(passed_match.group(1)) if passed_match else 0
            failed = int(failed_match.group(1)) if failed_match else 0
            
            total_tests += passed + failed
            total_passed += passed
            
            status = "PASS" if failed == 0 else "FAIL"
            print(f"  [{status}] {passed} passed, {failed} failed")
            
            results[test_file] = {
                "status": "PASS" if failed == 0 else "FAIL",
                "passed": passed,
                "failed": failed,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            print(f"  [FAIL] Test timeout (60 seconds)")
            results[test_file] = {
                "status": "FAIL",
                "passed": 0,
                "failed": 1,
                "return_code": -1
            }
        except Exception as e:
            print(f"  [FAIL] Error running tests: {str(e)}")
            results[test_file] = {
                "status": "FAIL",
                "passed": 0,
                "failed": 1,
                "return_code": -1
            }
    
    return results, total_tests, total_passed

def generate_summary_report(results, total_tests, total_passed):
    """Generate summary report"""
    print_section("SUMMARY REPORT")
    
    print("\nJOUR 2 Module Test Results:")
    print("-" * 80)
    
    for test_file, result in results.items():
        module_name = MODULE_DESCRIPTIONS.get(test_file, test_file)
        status = result["status"]
        passed = result["passed"]
        failed = result["failed"]
        
        status_symbol = "✓" if status == "PASS" else "✗"
        print(f"{status_symbol} {module_name:<45} {passed:3d} passed, {failed:3d} failed")
    
    print("-" * 80)
    
    total_failed = total_tests - total_passed
    pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\nOverall Results:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {total_passed}")
    print(f"  Failed: {total_failed}")
    print(f"  Pass Rate: {pass_rate:.1f}%")
    
    return total_failed == 0

def main():
    """Main validation function"""
    print_header("JOUR 2 VALIDATION SUITE")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Verify modules exist
    if not verify_modules_exist():
        print("\nERROR: Not all core modules found!")
        return False
    
    # Step 2: Verify test files exist
    if not verify_test_files_exist():
        print("\nERROR: Not all test files found!")
        return False
    
    # Step 3: Run tests
    results, total_tests, total_passed = run_pytest_tests()
    
    # Step 4: Generate report
    all_passed = generate_summary_report(results, total_tests, total_passed)
    
    # Final status
    print_header("JOUR 2 VALIDATION COMPLETE")
    
    if all_passed and total_tests > 0:
        print("\nSTATUS: SUCCESS - All JOUR 2 deliverables operational\n")
        print("JOUR 2 Implementation Summary:")
        print("  - Multi-user Orchestrator: 712 lines (user management, auth, quotas)")
        print("  - Docker Containerization: 558 lines (container lifecycle, networking)")
        print("  - RSA-4096 Cryptographic: 479 lines (encryption, signatures, certs)")
        print("  - Audit Trail System: 513 lines (immutable logging, compliance)")
        print("  - User Session Management: 525 lines (sessions, activities, tracking)")
        print(f"  - Total Code Written: 2,787 lines")
        print(f"  - Tests Created: 5 comprehensive test suites")
        print(f"  - Test Coverage: {total_passed}/{total_tests} tests passing")
        return True
    else:
        print("\nSTATUS: FAILURE - Some tests did not pass\n")
        print(f"Tests Passed: {total_passed}/{total_tests}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
