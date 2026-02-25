#!/usr/bin/env python3
"""
Obsidian Links Checker Script
Purpose: Verify that Obsidian markdown links are not broken after file moves
Author: Claude Code
Date: 2026-02-22
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set

class ObsidianLinkChecker:
    def __init__(self, vault_root: str = "D:/Vault/Vault"):
        self.vault_root = Path(vault_root)
        self.broken_links = []
        self.file_mapping = {}  # Maps old paths to new paths
        self.all_files = {}  # Maps file names to their full paths
        
    def find_all_markdown_files(self) -> Dict[str, Path]:
        """Find all markdown files in vault and create a mapping"""
        files = {}
        for md_file in self.vault_root.rglob("*.md"):
            # Normalize path
            rel_path = md_file.relative_to(self.vault_root)
            file_name = md_file.stem
            
            # Store with relative path as key
            files[str(rel_path)] = md_file
        
        return files
    
    def extract_links_from_file(self, file_path: Path) -> List[Tuple[str, int]]:
        """Extract all markdown links from a file
        
        Returns list of (link_target, line_number) tuples
        Supports formats:
        - [[link]]
        - [[link|display text]]
        - [display text](path/to/file.md)
        - [display text](path/to/file.md#heading)
        """
        links = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    # Find [[link]] format
                    wiki_links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', line)
                    for link in wiki_links:
                        links.append((link, line_num))
                    
                    # Find [text](path) format
                    md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', line)
                    for _, link in md_links:
                        links.append((link, line_num))
        
        except Exception as e:
            print(f"ERROR reading {file_path}: {e}")
        
        return links
    
    def resolve_link_target(self, link: str, from_file: Path) -> Tuple[bool, str]:
        """Resolve a link and check if it exists
        
        Returns (exists, resolved_path)
        """
        # Remove anchor/heading reference
        link_without_anchor = link.split('#')[0] if '#' in link else link
        
        if not link_without_anchor:
            return False, "Empty link target"
        
        # Get directory of the file containing the link
        file_dir = from_file.parent
        
        # Try to resolve the link
        if link_without_anchor.endswith('.md'):
            # Markdown file link
            target_path = file_dir / link_without_anchor
            
            # Also try as relative from vault root
            if not target_path.exists():
                target_path = self.vault_root / link_without_anchor
            
            if target_path.exists():
                return True, str(target_path.relative_to(self.vault_root))
            else:
                return False, str(target_path.relative_to(self.vault_root))
        else:
            # Wiki link - try to find file with this stem
            for file_path in self.vault_root.rglob(f"{link_without_anchor}.md"):
                return True, str(file_path.relative_to(self.vault_root))
            
            return False, f"Wikilink: {link_without_anchor}"
    
    def check_file_links(self, file_path: Path) -> List[Dict]:
        """Check all links in a file"""
        issues = []
        links = self.extract_links_from_file(file_path)
        
        for link, line_num in links:
            exists, resolved = self.resolve_link_target(link, file_path)
            
            if not exists:
                issues.append({
                    'file': str(file_path.relative_to(self.vault_root)),
                    'line': line_num,
                    'link': link,
                    'resolved_to': resolved,
                    'status': 'BROKEN'
                })
        
        return issues
    
    def check_all_links(self) -> Dict:
        """Check all links in the vault"""
        print("🔍 Scanning vault for markdown files...")
        all_files = self.find_all_markdown_files()
        total_files = len(all_files)
        
        all_issues = []
        checked_count = 0
        
        for rel_path, file_path in all_files.items():
            checked_count += 1
            if checked_count % 50 == 0:
                print(f"  Checked {checked_count}/{total_files} files...")
            
            issues = self.check_file_links(file_path)
            all_issues.extend(issues)
        
        return {
            'total_files_checked': total_files,
            'total_issues': len(all_issues),
            'broken_links': all_issues,
            'timestamp': datetime.now().isoformat()
        }
    
    def check_file_after_move(self, old_path: str, new_path: str) -> List[Dict]:
        """Check specific file after it has been moved
        
        Args:
            old_path: Original location (for logging)
            new_path: New location to check
        """
        new_full_path = self.vault_root / new_path
        
        if not new_full_path.exists():
            return [{
                'file': new_path,
                'status': 'FILE_NOT_FOUND',
                'message': f'File does not exist at {new_path}'
            }]
        
        return self.check_file_links(new_full_path)
    
    def generate_report(self, issues: Dict) -> str:
        """Generate a human-readable report"""
        report = []
        report.append("=" * 60)
        report.append("OBSIDIAN LINKS CHECK REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {issues['timestamp']}")
        report.append(f"Files checked: {issues['total_files_checked']}")
        report.append(f"Issues found: {issues['total_issues']}")
        report.append("")
        
        if issues['total_issues'] == 0:
            report.append("✅ No broken links detected!")
        else:
            report.append("❌ BROKEN LINKS DETECTED:")
            report.append("-" * 60)
            
            # Group by file
            by_file = {}
            for issue in issues['broken_links']:
                file_name = issue['file']
                if file_name not in by_file:
                    by_file[file_name] = []
                by_file[file_name].append(issue)
            
            for file_name, file_issues in sorted(by_file.items()):
                report.append(f"\n📄 {file_name}")
                for issue in file_issues:
                    report.append(f"  Line {issue['line']}: [[{issue['link']}]]")
                    report.append(f"    → Could not resolve to: {issue['resolved_to']}")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def save_report(self, issues: Dict, output_path: str = None) -> str:
        """Save report to file"""
        if output_path is None:
            output_path = self.vault_root / "SKILLS" / "organize-daily-reports" / "reports" / f"link-check-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(issues, f, indent=2, ensure_ascii=False)
        
        return str(output_path)


def main():
    """Main entry point"""
    print("🚀 Obsidian Links Checker")
    print("-" * 60)
    
    checker = ObsidianLinkChecker()
    
    # Check all links
    issues = checker.check_all_links()
    
    # Generate report
    report = checker.generate_report(issues)
    print(report)
    
    # Save report
    report_path = checker.save_report(issues)
    print(f"\n📋 Detailed report saved to: {report_path}")
    
    return issues


if __name__ == "__main__":
    main()
