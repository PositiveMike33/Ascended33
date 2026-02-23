# Phase 2: OAuth Setup & Configuration Quick-Start

**Objective**: Configure Gmail and Outlook authentication to enable email sync functionality.

**Estimated Time**: 30-45 minutes

**Prerequisites**:
- ✅ npm packages installed (`npm install` completed)
- ✅ Node.js v18+ installed
- Google/Microsoft accounts for testing
- Access to Google Cloud Console and Azure Portal

---

## 📋 Checklist: Complete These Steps

### Step 1: Google OAuth Setup (15 minutes)
- [ ] Open [Google Cloud Console](https://console.cloud.google.com)
- [ ] Create a new project named "email-sync-mcp"
- [ ] Enable Gmail API
- [ ] Enable Google Calendar API
- [ ] Create OAuth 2.0 credentials (Desktop application)
- [ ] Set redirect URI to `http://localhost:3000/auth/google/callback`
- [ ] Copy `Client ID` and `Client Secret` to `.env`

**Need Help?** See: [OAUTH_SETUP_GUIDE.md](./OAUTH_SETUP_GUIDE.md#google-oauth-setup)

### Step 2: Microsoft OAuth Setup (15 minutes)
- [ ] Open [Azure Portal](https://portal.azure.com)
- [ ] Create a new App Registration named "email-sync-mcp"
- [ ] Add Redirect URI: `http://localhost:3000/auth/microsoft/callback`
- [ ] Create Client Secret
- [ ] Configure API permissions (Mail.Read, Mail.Send, Calendar.Read)
- [ ] Copy `Application ID` and `Client Secret` to `.env`

**Need Help?** See: [OAUTH_SETUP_GUIDE.md](./OAUTH_SETUP_GUIDE.md#microsoft-oauth-setup)

### Step 3: Environment Configuration (5 minutes)
- [ ] Copy `.env.example` to `.env`
- [ ] Fill in Google credentials:
  ```
  GOOGLE_CLIENT_ID=your_client_id
  GOOGLE_CLIENT_SECRET=your_client_secret
  ```
- [ ] Fill in Microsoft credentials:
  ```
  MICROSOFT_CLIENT_ID=your_app_id
  MICROSOFT_CLIENT_SECRET=your_client_secret
  ```
- [ ] Set refresh token storage path (local JSON or secure vault)

### Step 4: Test OAuth Flows (10 minutes)
- [ ] Run: `npm run setup`
- [ ] Follow prompts to authenticate Google account
- [ ] Follow prompts to authenticate Microsoft account
- [ ] Verify credentials stored in `.env` or secure location
- [ ] Run: `npm run verify`
- [ ] Check console for "✅ All authentications successful"

### Step 5: Verify MCP Server Connection (5 minutes)
- [ ] Update `.mcp.json` with correct paths
- [ ] Open Claude Code
- [ ] Verify MCP server shows in extension
- [ ] Test tool availability: `gmail-fetch-emails`
- [ ] Fetch first 5 emails from Gmail to confirm connection

---

## 🔑 Environment File Template

Create `.env` in `/email-sync/` with this structure:

```env
# Google OAuth
GOOGLE_CLIENT_ID=xxxxxxxxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxxx

# Microsoft OAuth  
MICROSOFT_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
MICROSOFT_CLIENT_SECRET=xxx~xxxxxxxxxxxxxxxxxxxxxxxx~xxxx

# Refresh Token Storage (optional)
REFRESH_TOKEN_PATH=./credentials/tokens.json
SECURE_VAULT_URL=https://your-vault.example.com

# Server Configuration
MCP_PORT=3000
NODE_ENV=development
DEBUG=email-sync:*
```

---

## 🧪 Testing Each Component

### Test Gmail Connection
```bash
npm run verify
# Should output:
# ✅ Gmail API connection successful
# ✅ Found 25 emails
```

### Test Outlook Connection
```bash
npm run verify
# Should output:
# ✅ Outlook API connection successful  
# ✅ Found 18 emails
```

### Test MCP Server Startup
```bash
npm run start
# Should output:
# MCP Server running on stdio
# Tools available: [gmail-fetch-emails, outlook-fetch-emails, ...]
```

### Test in Claude Code
In Claude Code, after MCP server is configured:
```
/tools list
# Should show all 13 email-sync tools
```

---

## 🚨 Common Issues & Solutions

### Issue: "Invalid OAuth credentials"
**Cause**: Client ID/Secret mismatch between provider and .env
**Solution**: 
1. Double-check credentials copied exactly (no extra spaces)
2. Verify redirect URI matches exactly in provider settings
3. Check that you're using the right credential type (OAuth 2.0, not API key)

### Issue: "Redirect URI mismatch"
**Cause**: OAuth redirect in .env doesn't match provider configuration
**Solution**:
1. In Google Cloud Console: Verify http://localhost:3000/auth/google/callback
2. In Azure Portal: Verify http://localhost:3000/auth/microsoft/callback
3. Ensure http:// (not https://) for local testing

### Issue: "Token refresh failed"
**Cause**: Refresh token expired or invalidated
**Solution**:
1. Delete stored tokens from credentials/tokens.json
2. Re-run `npm run setup` to re-authenticate
3. Verify token storage has correct read/write permissions

### Issue: "Permission denied on API call"
**Cause**: API scopes not enabled in provider settings
**Solution**:
1. **Google**: Verify Gmail API and Calendar API enabled in Cloud Console
2. **Microsoft**: In App Registration → API permissions, ensure Mail.Read, Mail.Send, Calendar.Read are granted

### Issue: "CORS error when testing from browser"
**Cause**: MCP server doesn't allow browser-based requests
**Solution**: Use Claude Code extension instead (it uses stdio transport, not HTTP)

---

## 📊 Success Criteria

You'll know Phase 2 is complete when:

✅ **Google OAuth**
- [ ] Client ID and Secret copied to .env
- [ ] Test email fetch returns results
- [ ] Refresh token stored securely

✅ **Microsoft OAuth**
- [ ] Application ID and Secret copied to .env
- [ ] Test Outlook email fetch returns results
- [ ] Refresh token stored securely

✅ **MCP Integration**
- [ ] .mcp.json configured correctly
- [ ] MCP server starts without errors
- [ ] All 13 tools appear available
- [ ] Claude Code can invoke `gmail-fetch-emails` successfully

✅ **End-to-End Test**
- [ ] Fetch emails from Gmail via Claude Code
- [ ] Fetch emails from Outlook via Claude Code
- [ ] Retrieve calendar events via Claude Code
- [ ] Create daily note with calendar events

---

## 🔐 Security Best Practices

⚠️ **CRITICAL SECURITY CHECKLIST**:

- [ ] **Never commit .env to Git** - Add to .gitignore (already done)
- [ ] **Use strong Client Secrets** - 32+ characters minimum
- [ ] **Rotate secrets quarterly** - Set calendar reminder
- [ ] **Enable 2FA on OAuth provider accounts**
- [ ] **Use environment variables for production** - Not hardcoded .env
- [ ] **Encrypt refresh tokens at rest** - Use Node's `crypto` module
- [ ] **Validate redirect URIs** - Only allow localhost:3000 in dev
- [ ] **Audit token permissions** - Minimal scopes needed only
- [ ] **Monitor failed auth attempts** - Log and alert on suspicion

---

## 📝 Next: Phase 2 Integration Tasks

Once OAuth is working, consider these Phase 2 integrations:

**High Priority** (1-2 weeks):
1. **Slack Integration** - Post daily summaries to Slack
2. **Todoist Sync** - Create tasks from important emails
3. **Webhook Triggers** - Custom actions on specific events

**Medium Priority** (2-4 weeks):
1. **Email Rules Engine** - Auto-archive, label, forward
2. **Calendar to Obsidian** - Automatic meeting notes
3. **Email Templates** - Quick-reply templates

See: [INTEGRATIONS_ROADMAP.md](./INTEGRATIONS_ROADMAP.md) for full Phase 2-4 plan

---

## 💬 Getting Help

- **OAuth Errors**: See [OAUTH_SETUP_GUIDE.md](./OAUTH_SETUP_GUIDE.md#troubleshooting)
- **MCP Configuration**: See [MCP_INTEGRATION.md](./MCP_INTEGRATION.md)
- **General Questions**: See [README.md](./README.md)
- **Deployment Issues**: See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

---

**Last Updated**: 2026-02-23
**Status**: ✅ Ready for Phase 2 OAuth Setup
