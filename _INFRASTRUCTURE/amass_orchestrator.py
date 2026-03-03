#!/usr/bin/env python3

"""
═══════════════════════════════════════════════════════════════════════════════
AMASS Integration for HexStrike Ascended33
Complete OSINT reconnaissance orchestration with AMASS
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import json
import yaml
import subprocess
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import logging

# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═════════════════════════════════════════════════════════════════════════════

@dataclass
class AmassConfig:
    """AMASS configuration parameters"""
    domains: List[str]
    output_dir: str = "/vault/REPORT/Classified/amass"
    wordlist: str = "/usr/share/amass/wordlists/subdomains-top1million-5000.txt"
    dns_resolvers: List[str] = None
    max_workers: int = 50
    timeout: int = 30
    brute_force: bool = True
    active_scan: bool = False
    tor_proxy: Optional[str] = None
    verbose: bool = True
    
    def __post_init__(self):
        if self.dns_resolvers is None:
            self.dns_resolvers = [
                "8.8.8.8",
                "8.8.4.4",
                "1.1.1.1",
                "1.0.0.1",
                "9.9.9.9"
            ]

# ═════════════════════════════════════════════════════════════════════════════
# LOGGING SETUP
# ═════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# ═════════════════════════════════════════════════════════════════════════════
# AMASS ORCHESTRATOR
# ═════════════════════════════════════════════════════════════════════════════

class AmassOrchestrator:
    """Orchestrates AMASS reconnaissance"""
    
    def __init__(self, config: AmassConfig):
        self.config = config
        self.results = {}
        self.setup_output_dirs()
    
    def setup_output_dirs(self):
        """Create output directories"""
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory: {self.config.output_dir}")
    
    def build_amass_command(self, domain: str) -> List[str]:
        """Build AMASS command with parameters"""
        cmd = ["amass", "enum"]
        
        # Domain
        cmd.extend(["-d", domain])
        
        # Output format
        cmd.extend(["-o", f"{self.config.output_dir}/{domain}_subdomains.txt"])
        
        # Brute force
        if self.config.brute_force:
            cmd.append("-brute")
            cmd.extend(["-w", self.config.wordlist])
        
        # DNS resolvers
        for resolver in self.config.dns_resolvers:
            cmd.extend(["-r", resolver])
        
        # Max workers
        cmd.extend(["-max-dns-queries", str(self.config.timeout)])
        
        # Timeout
        cmd.extend(["-timeout", str(self.config.timeout)])
        
        # Verbose
        if self.config.verbose:
            cmd.append("-v")
        
        # Tor proxy (if configured)
        if self.config.tor_proxy:
            cmd.extend(["-proxy", self.config.tor_proxy])
        
        return cmd
    
    async def run_amass(self, domain: str) -> Dict:
        """Run AMASS enumeration for domain"""
        logger.info(f"Starting AMASS enumeration for {domain}")
        
        cmd = self.build_amass_command(domain)
        logger.debug(f"Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                logger.info(f"✓ AMASS completed for {domain}")
                
                # Read results
                output_file = f"{self.config.output_dir}/{domain}_subdomains.txt"
                subdomains = self.parse_results(output_file)
                
                return {
                    "domain": domain,
                    "status": "success",
                    "subdomains_found": len(subdomains),
                    "subdomains": subdomains,
                    "timestamp": datetime.now().isoformat(),
                    "output_file": output_file
                }
            else:
                logger.error(f"✗ AMASS failed for {domain}: {result.stderr}")
                return {
                    "domain": domain,
                    "status": "failed",
                    "error": result.stderr,
                    "timestamp": datetime.now().isoformat()
                }
        
        except subprocess.TimeoutExpired:
            logger.error(f"✗ AMASS timeout for {domain}")
            return {
                "domain": domain,
                "status": "timeout",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"✗ Error running AMASS for {domain}: {str(e)}")
            return {
                "domain": domain,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def parse_results(self, output_file: str) -> List[str]:
        """Parse AMASS output file"""
        subdomains = []
        try:
            if Path(output_file).exists():
                with open(output_file, 'r') as f:
                    subdomains = [line.strip() for line in f if line.strip()]
            logger.info(f"Parsed {len(subdomains)} subdomains from {output_file}")
        except Exception as e:
            logger.error(f"Error parsing results: {e}")
        
        return subdomains
    
    async def run_all_domains(self) -> Dict:
        """Run AMASS for all configured domains"""
        logger.info(f"Starting enumeration for {len(self.config.domains)} domains")
        
        tasks = [self.run_amass(domain) for domain in self.config.domains]
        results = await asyncio.gather(*tasks)
        
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "total_domains": len(self.config.domains),
            "domains": results,
            "config": asdict(self.config)
        }
        
        return self.results
    
    def save_results(self, output_file: Optional[str] = None):
        """Save results to JSON"""
        if not output_file:
            output_file = f"{self.config.output_dir}/amass_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            logger.info(f"Results saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    def generate_report(self) -> str:
        """Generate markdown report"""
        report_file = f"{self.config.output_dir}/amass_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        try:
            with open(report_file, 'w') as f:
                f.write("# AMASS Reconnaissance Report\n\n")
                f.write(f"**Generated**: {datetime.now().isoformat()}\n\n")
                
                for domain_result in self.results.get("domains", []):
                    domain = domain_result.get("domain", "unknown")
                    status = domain_result.get("status", "unknown")
                    
                    f.write(f"## Domain: {domain}\n")
                    f.write(f"**Status**: {status}\n")
                    
                    if status == "success":
                        subdomains = domain_result.get("subdomains", [])
                        f.write(f"**Subdomains Found**: {len(subdomains)}\n\n")
                        
                        for subdomain in subdomains[:50]:  # First 50
                            f.write(f"- {subdomain}\n")
                        
                        if len(subdomains) > 50:
                            f.write(f"\n... and {len(subdomains) - 50} more subdomains\n")
                    else:
                        error = domain_result.get("error", "Unknown error")
                        f.write(f"**Error**: {error}\n")
                    
                    f.write("\n---\n\n")
            
            logger.info(f"Report generated: {report_file}")
            return report_file
        
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return ""

# ═════════════════════════════════════════════════════════════════════════════
# COMMAND LINE INTERFACE
# ═════════════════════════════════════════════════════════════════════════════

def load_config(config_file: str) -> AmassConfig:
    """Load configuration from YAML"""
    try:
        with open(config_file, 'r') as f:
            data = yaml.safe_load(f)
            return AmassConfig(**data.get('amass', {}))
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        # Return default config
        return AmassConfig(domains=["example.com"])

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AMASS Integration for HexStrike')
    parser.add_argument('--config', default='./_INFRASTRUCTURE/amass_config.yaml',
                        help='Configuration file (YAML)')
    parser.add_argument('--domains', nargs='+', help='Domains to enumerate')
    parser.add_argument('--brute-force', action='store_true', help='Enable brute forcing')
    parser.add_argument('--tor-proxy', help='Tor proxy URL')
    parser.add_argument('--output-dir', help='Output directory')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Load or create config
    if Path(args.config).exists():
        config = load_config(args.config)
    else:
        config = AmassConfig(domains=["example.com"])
    
    # Override with CLI arguments
    if args.domains:
        config.domains = args.domains
    if args.output_dir:
        config.output_dir = args.output_dir
    if args.tor_proxy:
        config.tor_proxy = args.tor_proxy
    if args.brute_force:
        config.brute_force = True
    if args.verbose:
        config.verbose = True
    
    # Run orchestrator
    orchestrator = AmassOrchestrator(config)
    
    try:
        # Run async enumeration
        results = asyncio.run(orchestrator.run_all_domains())
        
        # Save results
        orchestrator.save_results()
        
        # Generate report
        report_file = orchestrator.generate_report()
        
        logger.info(f"✓ AMASS enumeration complete")
        logger.info(f"  Results: {orchestrator.config.output_dir}")
        logger.info(f"  Report: {report_file}")
        
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
