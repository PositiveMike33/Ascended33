#!/usr/bin/env python3

"""
═══════════════════════════════════════════════════════════════════════════════
AMASS HexStrike Integration Module
Seamless integration of AMASS with HexStrike Tools
═══════════════════════════════════════════════════════════════════════════════
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# ═════════════════════════════════════════════════════════════════════════════
# AMASS HEXSTRIKE WRAPPER
# ═════════════════════════════════════════════════════════════════════════════

class AmassHexStrike:
    """HexStrike AMASS integration wrapper"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.output_dir = Path(config.get('output_dir', '/vault/REPORT/Classified/amass'))
        self.domains = config.get('domains', [])
        self.results = {}
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        if not self.domains:
            print("Error: No domains specified")
            return False
        
        if not isinstance(self.domains, list):
            self.domains = [self.domains]
        
        return True
    
    def build_command(self) -> List[str]:
        """Build AMASS command"""
        cmd = ["amass", "enum"]
        
        # Add domains
        for domain in self.domains:
            cmd.extend(["-d", domain])
        
        # Brute force
        if self.config.get('brute_force', True):
            cmd.append("-brute")
            wordlist = self.config.get('wordlist', '/usr/share/amass/wordlists/subdomains-top1million-5000.txt')
            cmd.extend(["-w", wordlist])
        
        # DNS resolvers
        resolvers = self.config.get('dns_resolvers', [])
        if resolvers:
            for resolver in resolvers:
                cmd.extend(["-r", resolver])
        
        # Timeout
        timeout = self.config.get('timeout', 30)
        cmd.extend(["-timeout", str(timeout)])
        
        # Workers
        workers = self.config.get('max_workers', 50)
        cmd.extend(["-max-dns-queries", str(workers)])
        
        # Verbose
        if self.config.get('verbose', True):
            cmd.append("-v")
        
        # Tor proxy
        tor_proxy = self.config.get('tor_proxy')
        if tor_proxy:
            cmd.extend(["-proxy", tor_proxy])
        
        # Output
        output_file = self.output_dir / f"amass_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        cmd.extend(["-json", str(output_file)])
        
        return cmd
    
    def run(self) -> Dict:
        """Run AMASS"""
        if not self.validate_config():
            return {"status": "error", "message": "Invalid configuration"}
        
        cmd = self.build_command()
        
        print(f"[*] Running AMASS with {len(self.domains)} domain(s)")
        print(f"[*] Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes max
            )
            
            if result.returncode == 0:
                print("[+] AMASS completed successfully")
                return {
                    "status": "success",
                    "output": result.stdout,
                    "domains_scanned": len(self.domains),
                    "output_dir": str(self.output_dir)
                }
            else:
                print(f"[-] AMASS failed: {result.stderr}")
                return {
                    "status": "error",
                    "error": result.stderr
                }
        
        except subprocess.TimeoutExpired:
            return {"status": "timeout"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def parse_results(self, json_file: str) -> Dict:
        """Parse AMASS JSON results"""
        try:
            with open(json_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            return {"error": str(e)}
    
    def generate_report(self) -> str:
        """Generate markdown report"""
        report_file = self.output_dir / f"amass_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(report_file, 'w') as f:
            f.write("# AMASS Reconnaissance Report\n\n")
            f.write(f"**Timestamp**: {datetime.now().isoformat()}\n")
            f.write(f"**Domains Scanned**: {', '.join(self.domains)}\n")
            f.write(f"**Configuration**: {json.dumps(self.config, indent=2)}\n\n")
            f.write("## Results\n\n")
            f.write("See JSON files in this directory for detailed results.\n")
        
        return str(report_file)

# ═════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point for HexStrike"""
    
    # Read configuration from stdin or file
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = json.loads(sys.stdin.read())
    
    # Run AMASS
    amass = AmassHexStrike(config)
    result = amass.run()
    
    # Generate report
    if result.get('status') == 'success':
        report = amass.generate_report()
        result['report'] = report
    
    # Output result
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result.get('status') == 'success' else 1)

if __name__ == '__main__':
    main()
