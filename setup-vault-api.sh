#!/bin/bash
# setup-vault-api.sh — Configure Obsidian Local REST API

cat << 'EOF'
╔════════════════════════════════════════════════════════════════════╗
║ OBSIDIAN VAULT REST API SETUP                                      ║
╚════════════════════════════════════════════════════════════════════╝

Step 1: Open Obsidian
  - Make sure Obsidian is running
  - Vault should be: D:\Vault

Step 2: Enable Local REST API Plugin
  - Click Settings icon (bottom-left gear)
  - Go to: Settings → Community Plugins
  - Search for: "Local REST API"
  - Click Install
  - Click Enable (toggle on)

Step 3: Configure Plugin
  - Click the gear icon next to "Local REST API"
  - You'll see an API key like: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  - Copy this long alphanumeric string

Step 4: Configure Ascended33
  - Edit file: config/config.yaml
  - Find line: api_key: ""
  - Paste your key: api_key: "your_copied_key_here"
  - Example:
    api_key: "khu29d8fh29d89hd29dh29hd29"

Step 5: Test Connection
  - Run this test script (see below)
  - Or restart Streamlit dashboard
  - Click "Full Vault Sync" button

Step 6: Troubleshooting
  If you still get 401 errors:
  - Verify Obsidian is running (check system tray)
  - Verify REST API plugin is ENABLED (toggle on)
  - Clear browser cache: Ctrl+Shift+Del
  - Restart Streamlit: Kill process and rerun

═══════════════════════════════════════════════════════════════════════

EOF

# Try to detect and update the config
if [ -f "config/config.yaml" ]; then
    echo ""
    echo "Current config.yaml vault section:"
    echo "───────────────────────────────────"
    grep -A3 "^vault:" config/config.yaml || echo "  (vault section not found)"
    echo ""
    echo "To update your API key:"
    echo "  1. Edit config/config.yaml manually"
    echo "  2. Find the 'vault:' section"
    echo "  3. Update api_key: \"your_key_here\""
fi
