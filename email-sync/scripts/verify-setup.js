#!/usr/bin/env node

/**
 * Setup Verification Script
 * 
 * Verifies that all required dependencies, environment variables,
 * and OAuth credentials are properly configured for the email-sync MCP server.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, '..');
const ENV_FILE = path.join(PROJECT_ROOT, '.env');

// Color output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

const log = {
  success: (msg) => console.log(`${colors.green}✅${colors.reset} ${msg}`),
  error: (msg) => console.log(`${colors.red}❌${colors.reset} ${msg}`),
  warning: (msg) => console.log(`${colors.yellow}⚠️${colors.reset}  ${msg}`),
  info: (msg) => console.log(`${colors.blue}ℹ️${colors.reset}  ${msg}`),
  header: (msg) => console.log(`\n${colors.cyan}${msg}${colors.reset}`),
  blank: () => console.log('')
};

let hasErrors = false;
let hasWarnings = false;

async function verifySetup() {
  log.header('📋 Email Sync MCP Server - Setup Verification');
  
  // Check 1: Node version
  log.header('1️⃣  Node.js Version');
  const nodeVersion = process.version;
  const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);
  
  if (majorVersion >= 18) {
    log.success(`Node.js ${nodeVersion} (Required: >= 18.0.0)`);
  } else {
    log.error(`Node.js ${nodeVersion} (Required: >= 18.0.0)`);
    hasErrors = true;
  }
  
  // Check 2: Project structure
  log.header('2️⃣  Project Structure');
  const requiredDirs = ['src', 'config', 'docs', 'scripts'];
  const requiredFiles = ['package.json', '.env.example', 'dashboard.html'];
  
  requiredDirs.forEach(dir => {
    const dirPath = path.join(PROJECT_ROOT, dir);
    if (fs.existsSync(dirPath)) {
      log.success(`Directory: ${dir}/`);
    } else {
      log.error(`Directory missing: ${dir}/`);
      hasErrors = true;
    }
  });
  
  requiredFiles.forEach(file => {
    const filePath = path.join(PROJECT_ROOT, file);
    if (fs.existsSync(filePath)) {
      log.success(`File: ${file}`);
    } else {
      log.error(`File missing: ${file}`);
      hasErrors = true;
    }
  });
  
  // Check 3: npm dependencies
  log.header('3️⃣  NPM Dependencies');
  const packageJsonPath = path.join(PROJECT_ROOT, 'package.json');
  if (!fs.existsSync(packageJsonPath)) {
    log.error('package.json not found');
    hasErrors = true;
  } else {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    const dependencies = packageJson.dependencies || {};
    const requiredDeps = ['googleapis', 'nodemailer', 'dotenv', 'express', 'keytar', 'uuid'];
    
    requiredDeps.forEach(dep => {
      if (dependencies[dep]) {
        log.success(`${dep}: ${dependencies[dep]}`);
      } else {
        log.error(`Missing dependency: ${dep}`);
        hasErrors = true;
      }
    });
  }
  
  // Check 4: Environment variables
  log.header('4️⃣  Environment Configuration');
  if (fs.existsSync(ENV_FILE)) {
    log.success(`.env file exists`);
    
    const env = dotenv.parse(fs.readFileSync(ENV_FILE, 'utf8'));
    
    const requiredVars = [
      'GOOGLE_CLIENT_ID',
      'GOOGLE_CLIENT_SECRET',
      'MICROSOFT_CLIENT_ID',
      'MICROSOFT_CLIENT_SECRET'
    ];
    
    requiredVars.forEach(varName => {
      if (env[varName] && env[varName].trim()) {
        const masked = env[varName].slice(0, 5) + '*'.repeat(Math.max(0, env[varName].length - 10));
        log.success(`${varName}: ${masked}`);
      } else {
        log.warning(`${varName}: Not configured`);
        hasWarnings = true;
      }
    });
    
    // Optional variables
    if (env.MCP_PORT) {
      log.info(`MCP_PORT: ${env.MCP_PORT}`);
    } else {
      log.info(`MCP_PORT: (default 3000)`);
    }
    
    if (env.NODE_ENV) {
      log.info(`NODE_ENV: ${env.NODE_ENV}`);
    }
  } else {
    log.error(`.env file not found at ${ENV_FILE}`);
    log.info(`Please copy .env.example to .env and configure OAuth credentials`);
    hasWarnings = true;
  }
  
  // Check 5: Source files
  log.header('5️⃣  Source Files');
  const requiredSrcFiles = [
    'index.js',
    'tools/gmail.js',
    'tools/outlook.js',
    'tools/calendar.js',
    'config/oauth.js'
  ];
  
  requiredSrcFiles.forEach(file => {
    const filePath = path.join(PROJECT_ROOT, 'src', file);
    if (fs.existsSync(filePath)) {
      log.success(`src/${file}`);
    } else {
      log.warning(`src/${file} not found (may not be critical)`);
    }
  });
  
  // Check 6: Documentation
  log.header('6️⃣  Documentation');
  const docFiles = [
    'README.md',
    'OAUTH_SETUP_GUIDE.md',
    'MCP_INTEGRATION.md',
    'INTEGRATIONS_ROADMAP.md',
    'DEPLOYMENT_GUIDE.md',
    'PHASE_2_QUICKSTART.md'
  ];
  
  docFiles.forEach(file => {
    const filePath = path.join(PROJECT_ROOT, 'docs', file);
    if (fs.existsSync(filePath)) {
      log.success(`docs/${file}`);
    } else {
      log.warning(`docs/${file} not found`);
    }
  });
  
  // Check 7: MCP Configuration
  log.header('7️⃣  MCP Configuration');
  const mcpConfigPath = path.join(PROJECT_ROOT, '..', '.mcp.json');
  if (fs.existsSync(mcpConfigPath)) {
    try {
      const mcpConfig = JSON.parse(fs.readFileSync(mcpConfigPath, 'utf8'));
      if (mcpConfig.mcpServers && mcpConfig.mcpServers['email-sync']) {
        log.success('.mcp.json configured for email-sync server');
      } else {
        log.warning('.mcp.json exists but email-sync not configured');
        hasWarnings = true;
      }
    } catch (e) {
      log.error(`.mcp.json is not valid JSON: ${e.message}`);
      hasErrors = true;
    }
  } else {
    log.warning(`.mcp.json not found at project root`);
    log.info(`This file is needed for Claude Code integration`);
    hasWarnings = true;
  }
  
  // Final summary
  log.header('📊 Verification Summary');
  
  if (!hasErrors && !hasWarnings) {
    log.success('All checks passed! ✨');
    log.info('Next steps: Run "npm run start" to start the MCP server');
    return 0;
  } else if (!hasErrors && hasWarnings) {
    log.warning('Setup complete, but some items need attention');
    log.info('Review warnings above and configure OAuth credentials in .env');
    return 1;
  } else {
    log.error('Setup incomplete - fix errors above before proceeding');
    return 2;
  }
}

verifySetup().then(exitCode => process.exit(exitCode));
