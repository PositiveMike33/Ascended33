 # Kali linux
``curl -fsSL https://openclaw.ai/install.sh | bash ``
 
 Clawdbot 2026.1.24-3 (885167d) — iMessage green bubble energy, but for everyone.

Usage: clawdbot [options] [command]

Options:
  -V, --version     output the version number
  --dev             Dev profile: isolate state under ~/.clawdbot-dev, default gateway port 19001, and shift derived  
                    ports (browser/canvas)
  --profile <name>  Use a named profile (isolates CLAWDBOT_STATE_DIR/CLAWDBOT_CONFIG_PATH under ~/.clawdbot-<name>)  
  --no-color        Disable ANSI colors
  -h, --help        display help for command

Commands:
  setup             Initialize ~/.clawdbot/clawdbot.json and the agent workspace
  onboard           Interactive wizard to set up the gateway, workspace, and skills
  configure         Interactive prompt to set up credentials, devices, and agent defaults
  config            Config helpers (get/set/unset). Run without subcommand for the wizard.
  doctor            Health checks + quick fixes for the gateway and channels
  dashboard         Open the Control UI with your current token
  reset             Reset local config/state (keeps the CLI installed)
  uninstall         Uninstall the gateway service + local data (CLI remains)
  message           Send messages and channel actions
  memory            Memory search tools
  agent             Run an agent turn via the Gateway (use --local for embedded)
  agents            Manage isolated agents (workspaces + auth + routing)
  acp               Agent Control Protocol tools
  gateway           Gateway control
  daemon            Gateway service (legacy alias)
  logs              Gateway logs
  system            System events, heartbeat, and presence
  models            Model configuration
  approvals         Exec approvals
  nodes             Node commands
  devices           Device pairing + token management
  node              Node control
  sandbox           Sandbox tools
  tui               Terminal UI
  cron              Cron scheduler
  dns               DNS helpers
  docs              Docs helpers
  hooks             Hooks tooling
  webhooks          Webhook helpers
  pairing           Pairing helpers
  plugins           Plugin management
  channels          Channel management
  directory         Directory commands
  security          Security helpers
  skills            Skills management
  update            CLI update helpers
  status            Show channel health and recent session recipients
  health            Fetch health from the running gateway
  sessions          List stored conversation sessions
  browser           Manage clawd's dedicated browser (Chrome/Chromium)
  help              display help for command

Examples:
  clawdbot channels login --verbose
    Link personal WhatsApp Web and show QR + connection logs.
  clawdbot message send --target +15555550123 --message "Hi" --json
    Send via your web session and print JSON result.
  clawdbot gateway --port 18789
    Run the WebSocket Gateway locally.
  clawdbot --dev gateway
    Run a dev Gateway (isolated state/config) on ws://127.0.0.1:19001.
  clawdbot gateway --force
    Kill anything bound to the default gateway port, then start it.
  clawdbot gateway ...
    Gateway control via WebSocket.
  clawdbot agent --to +14385432555 --message "Clawdbot Activé" --deliver
    Talk directly to the agent using the Gateway; optionally send the WhatsApp reply.
  clawdbot message send --channel telegram --target @mychat --message "Hi"
    Send via your Telegram bot.
