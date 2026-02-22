#!/usr/bin/env python
"""Direct test runner for Ascended33 JOUR 1 validation"""

import sys
import subprocess
import os

# Change to project directory
os.chdir(r'D:\Vault\Vault\Ascended33')

# First install pytest if needed
print("=" * 70)
print("Installing test dependencies...")
print("=" * 70)
subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'pytest', 'pytest-cov'])

# Run the tests
print("\n" + "=" * 70)
print("JOUR 1 VALIDATION TEST SUITE")
print("=" * 70 + "\n")

result = subprocess.run(
    [sys.executable, '-m', 'pytest', 'tests/test_obsidian_sync.py', '-v', '--tb=short'],
    capture_output=False
)

sys.exit(result.returncode)
