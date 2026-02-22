#!/usr/bin/env python
"""Test runner with full output for Ascended33 JOUR 1 validation"""

import sys
import os
import subprocess

def main():
    os.chdir(r'D:\Vault\Vault\Ascended33')
    
    print("\n" + "=" * 80)
    print("JOUR 1 VALIDATION TEST SUITE - Ascended33 OSINT Platform")
    print("=" * 80 + "\n")
    
    # Install dependencies
    print("Installing test dependencies...")
    install_proc = subprocess.Popen(
        [sys.executable, '-m', 'pip', 'install', '-q', 'pytest', 'pytest-cov', 'watchdog', 'pyyaml'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    install_proc.wait()
    
    print("\n" + "=" * 80)
    print("Running validation tests...")
    print("=" * 80 + "\n")
    
    # Run tests with real-time output
    test_proc = subprocess.Popen(
        [sys.executable, '-m', 'pytest', 'tests/test_obsidian_sync.py', '-v', '--tb=short'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    # Print output line by line
    for line in test_proc.stdout:
        print(line, end='')
    
    test_proc.wait()
    
    print("\n" + "=" * 80)
    print("Test execution complete")
    print("=" * 80 + "\n")
    
    return test_proc.returncode

if __name__ == '__main__':
    sys.exit(main())
