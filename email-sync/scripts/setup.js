#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const question = (prompt) =>
  new Promise((resolve) => {
    rl.question(prompt, resolve);
  });

async function setup() {
  console.log('\n📧 Email Sync MCP Setup\n');
  console.log('This wizard will help you configure OAuth credentials for Gmail and Outlook.\n');

  // Step 1: Create .env file
  console.log('Step 1: Creating .env file from .env.example...\n');
  const envPath = path.join(process.cwd(), '.env');
  const envExamplePath = path.join(process.cwd(), '.env.example');

  if (fs.existsSync(envPath)) {
    console.log('✓ .env file already exists\n');
  } else {
    fs.copyFileSync(envExamplePath, envPath);
    console.log('✓ .env file created\n');
  }

  // Step 2: Google OAuth Setup
  console.log('Step 2: Google OAuth Configuration\n');
  console.log('To set up Gmail and Calendar integration:');
  console.log('1. Go to https://console.cloud.google.com/');
  console.log('2. Create a new project');
  console.log('3. Enable Gmail API and Google Calendar API');
  console.log('4. Create OAuth 2.0 credentials (Web application)');
  console.log('5. Add http://localhost:3000/auth/google/callback as authorized redirect URI\n');

  const googleClientId = await question(
    'Enter GOOGLE_CLIENT_ID (or press Enter to skip): '
  );
  const googleClientSecret = await question(
    'Enter GOOGLE_CLIENT_SECRET (or press Enter to skip): '
  );

  // Step 3: Microsoft OAuth Setup
  console.log('\nStep 3: Microsoft OAuth Configuration\n');
  console.log('To set up Outlook integration:');
  console.log('1. Go to https://portal.azure.com/');
  console.log('2. Register a new application');
  console.log('3. Create a client secret');
  console.log('4. Add http://localhost:3000/auth/microsoft/callback as redirect URI\n');

  const microsoftClientId = await question(
    'Enter MICROSOFT_CLIENT_ID (or press Enter to skip): '
  );
  const microsoftClientSecret = await question(
    'Enter MICROSOFT_CLIENT_SECRET (or press Enter to skip): '
  );

  // Step 4: Obsidian Configuration
  console.log('\nStep 4: Obsidian Vault Configuration\n');
  console.log('Enter the path to your Obsidian vault. Example: C:/Users/th3th/Obsidian/Main Vault\n');

  const vaultPath = await question('Enter OBSIDIAN_VAULT_PATH: ');

  // Update .env file
  let envContent = fs.readFileSync(envPath, 'utf8');

  if (googleClientId) {
    envContent = envContent.replace(
      /GOOGLE_CLIENT_ID=.*/,
      `GOOGLE_CLIENT_ID=${googleClientId}`
    );
  }
  if (googleClientSecret) {
    envContent = envContent.replace(
      /GOOGLE_CLIENT_SECRET=.*/,
      `GOOGLE_CLIENT_SECRET=${googleClientSecret}`
    );
  }
  if (microsoftClientId) {
    envContent = envContent.replace(
      /MICROSOFT_CLIENT_ID=.*/,
      `MICROSOFT_CLIENT_ID=${microsoftClientId}`
    );
  }
  if (microsoftClientSecret) {
    envContent = envContent.replace(
      /MICROSOFT_CLIENT_SECRET=.*/,
      `MICROSOFT_CLIENT_SECRET=${microsoftClientSecret}`
    );
  }
  if (vaultPath) {
    envContent = envContent.replace(
      /OBSIDIAN_VAULT_PATH=.*/,
      `OBSIDIAN_VAULT_PATH=${vaultPath}`
    );
  }

  fs.writeFileSync(envPath, envContent);

  console.log('\n✓ .env file updated with credentials\n');

  // Step 5: Create config directory
  const configDir = path.join(process.cwd(), 'config');
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
    console.log('✓ config/ directory created\n');
  }

  // Step 6: Instructions for OAuth tokens
  console.log('Step 5: Obtaining OAuth Tokens\n');
  console.log('After setting up OAuth credentials, run:');
  console.log('  npm run dev\n');
  console.log('The server will provide URLs to authorize your accounts.\n');

  console.log('✅ Setup complete!\n');
  console.log('Next steps:');
  console.log('1. Place your Google OAuth credentials at: config/credentials.json');
  console.log('2. Run: npm run dev');
  console.log('3. Follow the authorization links displayed\n');

  rl.close();
}

setup().catch(console.error);
