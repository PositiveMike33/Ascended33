#!/usr/bin/env node

/**
 * MCP Server n8n pour Vault
 * Connecteur local pour accéder à n8n depuis D:/Vault/Vault/
 */

const fs = require('fs');
const path = require('path');

const vaultPath = 'D:/Vault/Vault';

// Configuration n8n
const n8nConfig = {
  vault_path: vaultPath,
  n8n_instance: 'http://localhost:5678',
  resources: {
    workflows: path.join(vaultPath, 'n8n_workflows'),
    templates: path.join(vaultPath, 'n8n_templates'),
    data: path.join(vaultPath, 'n8n_data')
  }
};

// Créer les répertoires nécessaires
Object.values(n8nConfig.resources).forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

// Logger
function log(message) {
  fs.appendFileSync(path.join(vaultPath, 'mcp_n8n.log'), `[${new Date().toISOString()}] ${message}\n`);
}

log('MCP n8n Server démarré');
log(`Vault Path: ${vaultPath}`);
log(`Resources créés: ${Object.keys(n8nConfig.resources).join(', ')}`);

console.error(JSON.stringify({
  initialized: true,
  vault_path: vaultPath,
  resources: n8nConfig.resources
}));
