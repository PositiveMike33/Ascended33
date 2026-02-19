#!/usr/bin/env bash
# setup_kali.sh — Install and configure hexstrike-ai on Kali Linux VM
# Run this script ONCE directly on the Kali VM:
#   chmod +x setup_kali.sh && ./setup_kali.sh
# ============================================================

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[+]${NC} $*"; }
warn()  { echo -e "${YELLOW}[!]${NC} $*"; }
error() { echo -e "${RED}[X]${NC} $*"; exit 1; }

echo ""
echo "=============================================="
echo "  ASCENDED33 — Kali VM Setup"
echo "  hexstrike-ai + SSH server configuration"
echo "=============================================="
echo ""

# --- 1. Update system ---
info "Updating system packages..."
sudo apt-get update -qq

# --- 2. Install base dependencies ---
info "Installing base dependencies..."
sudo apt-get install -y -qq \
    git python3 python3-pip python3-venv \
    openssh-server curl wget net-tools \
    nmap masscan nikto sqlmap wpscan \
    ffuf nuclei amass \
    tor torsocks 2>/dev/null || true

# --- 3. Enable SSH server ---
info "Configuring SSH server..."
sudo systemctl enable ssh
sudo systemctl start ssh
SSH_IP=$(ip addr show | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | cut -d/ -f1 | head -1)
info "SSH server running. Kali VM IP: ${SSH_IP}"
echo ""
warn ">>> Add this to Windows ~/.ssh/config (C:\\Users\\th3th\\.ssh\\config):"
echo "    Host kali-lab"
echo "      HostName ${SSH_IP}"
echo "      User kali"
echo "      IdentityFile ~/.ssh/kali_lab_key"
echo "      ServerAliveInterval 60"
echo ""

# --- 4. Generate SSH key if needed ---
if [ ! -f ~/.ssh/authorized_keys ]; then
    mkdir -p ~/.ssh && chmod 700 ~/.ssh
    touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
fi

# --- 5. Clone / update hexstrike-ai ---
HEXSTRIKE_DIR=~/hexstrike-ai

if [ -d "$HEXSTRIKE_DIR/.git" ]; then
    info "hexstrike-ai already cloned — pulling latest..."
    git -C "$HEXSTRIKE_DIR" pull
else
    info "Cloning hexstrike-ai..."
    git clone https://github.com/0x4m4/hexstrike-ai.git "$HEXSTRIKE_DIR"
fi

# --- 6. Set up Python virtual environment ---
info "Setting up Python virtual environment..."
python3 -m venv "$HEXSTRIKE_DIR/hexstrike-env"
source "$HEXSTRIKE_DIR/hexstrike-env/bin/activate"

if [ -f "$HEXSTRIKE_DIR/requirements.txt" ]; then
    pip install -q -r "$HEXSTRIKE_DIR/requirements.txt"
elif [ -f "$HEXSTRIKE_DIR/setup.py" ]; then
    pip install -q -e "$HEXSTRIKE_DIR"
else
    pip install -q flask requests anthropic
fi

deactivate

# --- 7. Create systemd service for hexstrike-ai ---
info "Creating hexstrike-ai systemd service..."
sudo tee /etc/systemd/system/hexstrike-ai.service > /dev/null <<EOF
[Unit]
Description=hexstrike-ai MCP Security Server
After=network.target

[Service]
Type=simple
User=kali
WorkingDirectory=${HEXSTRIKE_DIR}
ExecStart=${HEXSTRIKE_DIR}/hexstrike-env/bin/python3 hexstrike_server.py
Restart=on-failure
RestartSec=5
StandardOutput=append:/var/log/hexstrike-ai.log
StandardError=append:/var/log/hexstrike-ai.log

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable hexstrike-ai
sudo systemctl start hexstrike-ai || warn "Service start failed — check: sudo journalctl -u hexstrike-ai -n 20"

# --- 8. Verify hexstrike-ai is reachable ---
sleep 3
if curl -sf http://localhost:8888/health > /dev/null 2>&1; then
    info "hexstrike-ai MCP server running on http://localhost:8888"
else
    warn "hexstrike-ai not yet responding on :8888 — check: sudo journalctl -u hexstrike-ai -n 30"
fi

# --- 9. Final summary ---
echo ""
echo "=============================================="
echo "  SETUP COMPLETE"
echo "=============================================="
info "Kali VM IP:         ${SSH_IP}"
info "SSH port:           22"
info "hexstrike-ai port:  8888"
info "hexstrike-ai logs:  /var/log/hexstrike-ai.log"
echo ""
warn "Next step — on Windows, run:"
echo "  ssh-keygen -t ed25519 -f C:\\Users\\th3th\\.ssh\\kali_lab_key"
echo "  type C:\\Users\\th3th\\.ssh\\kali_lab_key.pub | ssh kali@${SSH_IP} 'cat >> ~/.ssh/authorized_keys'"
echo ""
warn "Then update Ascended33 config/config.yaml:"
echo "  kali_vm:"
echo "    host: \"${SSH_IP}\""
echo "    user: \"kali\""
echo "    key_file: \"C:/Users/th3th/.ssh/kali_lab_key\""
echo ""
