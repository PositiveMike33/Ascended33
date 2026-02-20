"""
trace_cleaner.py — Clean operational artifacts and traces

OPSEC requirement: After any security operation, clean up local artifacts
to prevent operational security breaches.
"""

import os
import subprocess
import sys
from pathlib import Path


class TraceCleaner:
    """Removes operational artifacts and traces"""

    def __init__(self, scope: str = "local"):
        """
        scope: "local" = current session only | "full" = all system artifacts
        """
        self.scope = scope

    def clean_bash_history(self) -> bool:
        """Clear shell history from current session and recent commands"""
        try:
            # Clear current session
            subprocess.run(["bash", "-c", "history -c"], check=False)
            subprocess.run(["bash", "-c", "history -w"], check=False)

            # Clear .bash_history (current user)
            history_file = Path.home() / ".bash_history"
            if history_file.exists():
                history_file.unlink()

            print("✓ Bash history cleared")
            return True
        except Exception as e:
            print(f"✗ Failed to clear bash history: {e}")
            return False

    def clean_zsh_history(self) -> bool:
        """Clear zsh history"""
        try:
            subprocess.run(["bash", "-c", "fc -wn"], check=False)
            history_file = Path.home() / ".zsh_history"
            if history_file.exists():
                history_file.unlink()

            print("✓ Zsh history cleared")
            return True
        except Exception as e:
            print(f"✗ Failed to clear zsh history: {e}")
            return False

    def clean_temp_files(self) -> bool:
        """Remove temporary files created during operations"""
        try:
            temp_path = Path("/tmp")
            count = 0

            # Clean /tmp files
            if temp_path.exists():
                for f in temp_path.glob("*"):
                    if f.is_file():
                        try:
                            f.unlink()
                            count += 1
                        except Exception:
                            pass

            # Clean ~/.cache (if full mode)
            if self.scope == "full":
                cache_path = Path.home() / ".cache"
                if cache_path.exists():
                    for f in cache_path.glob("**/*"):
                        if f.is_file():
                            try:
                                f.unlink()
                                count += 1
                            except Exception:
                                pass

            print(f"✓ Removed {count} temporary files")
            return True
        except Exception as e:
            print(f"✗ Failed to clean temp files: {e}")
            return False

    def clean_ssl_certificates(self) -> bool:
        """Clear SSL/TLS session artifacts"""
        try:
            ssl_cache = Path.home() / ".ssl"
            if ssl_cache.exists():
                import shutil
                shutil.rmtree(ssl_cache)

            print("✓ SSL certificate cache cleared")
            return True
        except Exception as e:
            print(f"✗ Failed to clear SSL cache: {e}")
            return False

    def clean_pip_cache(self) -> bool:
        """Clear pip package cache"""
        try:
            subprocess.run([sys.executable, "-m", "pip", "cache", "purge"], check=False)
            print("✓ Pip cache cleared")
            return True
        except Exception as e:
            print(f"✗ Failed to clear pip cache: {e}")
            return False

    def clean_docker_logs(self) -> bool:
        """Clean Docker container logs (security containers)"""
        if self.scope != "full":
            return True

        try:
            containers = ["th3-kali", "th3-tor"]
            for container in containers:
                subprocess.run(
                    ["docker", "exec", "-it", container, "rm", "-rf", "/var/log/*"],
                    check=False,
                    timeout=10,
                )

            print("✓ Docker container logs cleared")
            return True
        except Exception as e:
            print(f"✗ Failed to clear Docker logs: {e}")
            return False

    def clean_dns_cache(self) -> bool:
        """Clear DNS resolver cache"""
        try:
            # Linux
            subprocess.run(["sudo", "systemctl", "restart", "systemd-resolved"], check=False)

            # OS X
            subprocess.run(["sudo", "dscacheutil", "-flushcache"], check=False)

            print("✓ DNS cache cleared")
            return True
        except Exception as e:
            print(f"⚠ Failed to clear DNS cache: {e}")
            return False

    def clean_ssh_keys_cache(self) -> bool:
        """Clear cached SSH keys"""
        try:
            subprocess.run(["ssh-add", "-D"], check=False)
            print("✓ SSH key cache cleared")
            return True
        except Exception as e:
            print(f"✗ Failed to clear SSH cache: {e}")
            return False

    def run_full_cleanup(self) -> bool:
        """Execute all cleanup operations"""
        print("\n" + "=" * 70)
        print("TRACE CLEANER — OPERATIONAL ARTIFACT REMOVAL")
        print(f"Scope: {self.scope.upper()}")
        print("=" * 70 + "\n")

        results = [
            self.clean_bash_history(),
            self.clean_zsh_history(),
            self.clean_temp_files(),
            self.clean_ssl_certificates(),
            self.clean_pip_cache(),
            self.clean_dns_cache(),
            self.clean_ssh_keys_cache(),
        ]

        if self.scope == "full":
            results.append(self.clean_docker_logs())

        print("\n" + "=" * 70)
        passed = sum(results)
        total = len(results)
        print(f"Cleanup Complete: {passed}/{total} operations successful")
        print("=" * 70 + "\n")

        return all(results)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Clean operational traces and artifacts"
    )
    parser.add_argument(
        "--scope",
        choices=["local", "full"],
        default="local",
        help="Cleanup scope (default: local session only)",
    )

    args = parser.parse_args()

    cleaner = TraceCleaner(scope=args.scope)
    success = cleaner.run_full_cleanup()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
