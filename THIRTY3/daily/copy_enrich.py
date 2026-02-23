#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
from datetime import datetime

source_dir = Path(r"D:\Vault\Vault\REPORT\Février")
dest_dir = Path(r"D:\Vault\Vault\THIRTY3\daily")

processed = 0
errors = 0

# Find all markdown files
md_files = list(source_dir.glob("**/*.md"))

print(f"Found {len(md_files)} markdown files")

for md_file in md_files:
    try:
        # Extract date from directory path (DD-MM-YYYY format)
        path_str = str(md_file)
        match = re.search(r'(\d{2})-(\d{2})-(\d{4})', path_str)
        
        if match:
            day, month, year = match.groups()
            
            # Create destination directory
            dest_month_dir = dest_dir / year / month
            dest_month_dir.mkdir(parents=True, exist_ok=True)
            
            # Create new filename
            new_filename = f"{year}-{month}-{day}_learning_progress.md"
            dest_path = dest_month_dir / new_filename
            
            # Read original content
            with open(md_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Create YAML frontmatter
            yaml_frontmatter = f"""---
date: {year}-{month}-{day}
type: learning-progress
phase: [2]
tags: [learning, phase-2, development, security, hacking]
status: active
source: REPORT/Février
---

"""
            
            # Combine and write
            enriched_content = yaml_frontmatter + original_content
            
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(enriched_content)
            
            processed += 1
            print(f"✓ {year}-{month}-{day}")
        else:
            errors += 1
            
    except Exception as e:
        errors += 1
        print(f"✗ Error: {md_file.name} - {e}")

print(f"\n=== SUMMARY ===")
print(f"Processed: {processed}")
print(f"Errors: {errors}")
print(f"Total: {len(md_files)}")
