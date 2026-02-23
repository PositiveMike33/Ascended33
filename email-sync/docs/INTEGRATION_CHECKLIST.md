# 🎯 Email Sync MCP - Complete Integration Checklist

A comprehensive checklist covering every step from setup to production deployment.

---

## Phase 0: Prerequisites ✅

### System Requirements
- [ ] Windows 11, macOS, or Linux OS
- [ ] Node.js >= 18.0.0 (download from nodejs.org)
- [ ] npm >= 9.0.0 (comes with Node.js)
- [ ] Git (for version control)
- [ ] Text editor (VS Code recommended)

### Access Requirements
- [ ] Google account for Gmail testing
- [ ] Microsoft account for Outlook testing
- [ ] Access to Google Cloud Console (console.cloud.google.com)
- [ ] Access to Azure Portal (portal.azure.com)
- [ ] Administrative access to local machine (for npm install)

### Verify Prerequisites
```bash
node --version      # Should show v18.x.x or higher
npm --version       # Should show 9.x.x or higher
git --version       # Should show git version info
```

---

## Phase 1: Local Development Setup ✅

### Clone & Install
- [ ] Clone/create email-sync project directory
- [ ] Run: `npm install` (installs dependencies)
- [ ] Run: `npm run verify` (checks environment)
- [ ] Verify output shows: "All checks passed! ✨"

### Project Structure Verification
- [ ] `/src` - Source code directory exists
- [ ] `/config` - Configuration directory exists
- [ ] `/docs` - Documentation directory exists
- [ ] `/scripts` - Setup scripts directory exists
- [ ] `package.json` - Dependencies manifest exists
- [ ] `.env.example` - Environment template exists
- [ ] `.gitignore` - Git ignore rules exist

### First Test Run
- [ ] Run: `npm run start`
- [ ] Should output: "MCP Server running on stdio"
- [ ] Press Ctrl+C to stop server
- [ ] Verify no errors in console output

---

## Phase 2: OAuth Configuration 🔑

### Google Cloud Setup

**Project Creation**
- [ ] Open [Google Cloud Console](https://console.cloud.google.com)
- [ ] Click "Create Project"
- [ ] Enter project name: "email-sync-mcp"
- [ ] Wait for project creation (takes ~30 seconds)

**Enable APIs**
- [ ] In "APIs & Services" → "Library"
- [ ] Search: "Gmail API"
- [ ] Click "Enable"
- [ ] Search: "Google Calendar API"
- [ ] Click "Enable"
- [ ] Search: "Google+ API"
- [ ] Click "Enable"

**Create OAuth Credentials**
- [ ] Go to "APIs & Services" → "Credentials"
- [ ] Click "Create Credentials" → "OAuth client ID"
- [ ] Choose "Desktop application" as application type
- [ ] Click "Create"
- [ ] Copy displayed **Client ID** → Save to notepad
- [ ] Click download icon to save credentials JSON file
- [ ] Click "OK"

**Configure OAuth Consent Screen**
- [ ] Go to "APIs & Services" → "OAuth consent screen"
- [ ] Choose "External" user type
- [ ] Click "Create"
- [ ] Fill "App name": "Email Sync MCP"
- [ ] Fill "User support email": your-email@gmail.com
- [ ] Fill "Developer contact": your-email@gmail.com
- [ ] Click "Save and Continue"
- [ ] Skip "Scopes" section, click "Continue"
- [ ] Add test user: your Gmail address
- [ ] Click "Save and Continue"
- [ ] Review summary, click "Back to Dashboard"

**Get Client Secret**
- [ ] In "Credentials" page, find your OAuth app
- [ ] Click the app name to edit
- [ ] Scroll to "Client secrets" section
- [ ] Copy **Client Secret** → Save to notepad

### Microsoft Azure Setup

**App Registration**
- [ ] Open [Azure Portal](https://portal.azure.com)
- [ ] Go to "Azure Active Directory" → "App registrations"
- [ ] Click "New registration"
- [ ] Enter name: "email-sync-mcp"
- [ ] Choose "Accounts in any organizational directory..."
- [ ] Under "Redirect URI", select "Web"
- [ ] Enter: `http://localhost:3000/auth/microsoft/callback`
- [ ] Click "Register"

**Get Application ID**
- [ ] On Overview page, copy **Application (client) ID** → Save to notepad

**Create Client Secret**
- [ ] Go to "Certificates & secrets"
- [ ] Click "New client secret"
- [ ] Enter description: "MCP Development"
- [ ] Select expiration: "6 months"
- [ ] Click "Add"
- [ ] Copy the **Value** (not ID) → Save to notepad (appears only once!)

**Configure API Permissions**
- [ ] Go to "API permissions"
- [ ] Click "Add a permission"
- [ ] Select "Microsoft Graph"
- [ ] Choose "Delegated permissions"
- [ ] Search and select:
  - [ ] `Mail.Read`
  - [ ] `Mail.Send`
  - [ ] `Calendar.Read`
  - [ ] `User.Read`
- [ ] Click "Add permissions"
- [ ] Click "Grant admin consent for..." (if available)

### Environment Configuration

**Create .env File**
- [ ] Copy file `.env.example` to `.env`
- [ ] Open `.env` in text editor
- [ ] Fill in values from your notes:

```env
# Google OAuth (from Google Cloud Console)
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE
GOOGLE_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE

# Microsoft OAuth (from Azure Portal)
MICROSOFT_CLIENT_ID=YOUR_APPLICATION_ID_HERE
MICROSOFT_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE

# Configuration
NODE_ENV=development
MCP_PORT=3000
DEBUG=email-sync:*
```

**Save & Verify**
- [ ] Save `.env` file
- [ ] Verify `.env` is in `.gitignore` (never commit credentials!)
- [ ] Run: `npm run verify`
- [ ] Verify all environment variables show as configured

---

## Phase 3: Initial Authentication 🔐

### Google Authentication
- [ ] Run: `npm run setup`
- [ ] When prompted, select: "Google"
- [ ] Browser opens Google login page
- [ ] Sign in with your Google account
- [ ] Click "Allow" when permission requested
- [ ] Browser redirects to confirmation page
- [ ] Return to terminal and press Enter
- [ ] Verify output: "✅ Google authentication successful"

### Microsoft Authentication
- [ ] Still in setup wizard, select: "Microsoft"
- [ ] Browser opens Microsoft login page
- [ ] Sign in with your Microsoft account
- [ ] Click "Accept" when permission requested
- [ ] Browser redirects to confirmation page
- [ ] Return to terminal and press Enter
- [ ] Verify output: "✅ Microsoft authentication successful"

### Credential Storage
- [ ] Verify credentials saved to:
  - [ ] Google refresh token stored
  - [ ] Microsoft refresh token stored
- [ ] Run: `npm run verify`
- [ ] Confirm both OAuth providers show as configured

---

## Phase 4: MCP Server Integration 🚀

### Configuration Files

**Update .mcp.json**
- [ ] Open `.mcp.json` in project root
- [ ] Verify structure:
  ```json
  {
    "mcpServers": {
      "email-sync": {
        "command": "node",
        "args": ["email-sync/src/index.js"],
        ...
      }
    }
  }
  ```
- [ ] Verify paths are correct relative to project root
- [ ] Save file

**Verify Claude Code Configuration**
- [ ] Open Claude Code in your IDE
- [ ] Check "Extensions" panel
- [ ] Look for MCP section
- [ ] Verify "email-sync" server appears
- [ ] Status should show: "Connected" (green)

### Server Startup

**Start MCP Server**
- [ ] Run: `npm run start`
- [ ] Verify output:
  ```
  MCP Server running on stdio
  Tools loaded: 13
  ```
- [ ] Leave server running in terminal

**In Claude Code, Verify Tools**
- [ ] Run command: `/tools list`
- [ ] Verify these tools appear:
  - [ ] `gmail-fetch-emails`
  - [ ] `gmail-send-email`
  - [ ] `gmail-search-emails`
  - [ ] `outlook-fetch-emails`
  - [ ] `outlook-send-email`
  - [ ] `calendar-get-events`
  - [ ] `calendar-create-daily-note`
  - [ ] `calendar-create-weekly-note`
  - [ ] `calendar-add-event-from-email`
  - [ ] And others (total 13)

---

## Phase 5: Functional Testing 🧪

### Email Functions

**Test Gmail Fetch**
- [ ] In Claude Code, run: "Fetch my last 5 unread emails from Gmail"
- [ ] Should return list of recent unread emails
- [ ] Verify sender, subject, date fields present
- [ ] Verify no errors in console

**Test Outlook Fetch**
- [ ] In Claude Code, run: "Show me emails from Outlook"
- [ ] Should return list of Outlook emails
- [ ] Verify fields match Gmail format
- [ ] Verify no errors in console

**Test Email Search**
- [ ] In Claude Code, run: "Search for emails about projects"
- [ ] Should return emails matching search term
- [ ] Verify relevance of results

### Calendar Functions

**Test Calendar Read**
- [ ] In Claude Code, run: "Show me my calendar for next 7 days"
- [ ] Should return upcoming events
- [ ] Verify time, title, attendees shown
- [ ] Verify no errors

**Test Daily Note Creation**
- [ ] In Claude Code, run: "Create a daily note for today with calendar events"
- [ ] Should create Obsidian note
- [ ] Verify file created in Obsidian vault
- [ ] Verify calendar events embedded

### Error Handling

**Test Error Conditions**
- [ ] Test with invalid email address
- [ ] Test with expired credentials
- [ ] Test with network offline
- [ ] Verify error messages are helpful
- [ ] Verify server recovers gracefully

---

## Phase 6: Dashboard & Visualization 📊

### Dashboard Setup
- [ ] Open `dashboard.html` in browser
- [ ] Verify glassmorphic UI loads
- [ ] Verify email count displays
- [ ] Verify calendar events show
- [ ] Click through dashboard sections
- [ ] Verify no console errors

### Dashboard Features
- [ ] Email statistics visible
- [ ] Calendar preview works
- [ ] Refresh button functions
- [ ] Responsive design on mobile

---

## Phase 7: Security Hardening 🔒

### Environment Security
- [ ] Verify `.env` in `.gitignore`
- [ ] Verify `.env` not in version history: `git log --all -- .env`
- [ ] Backup `.env` file securely
- [ ] Never share `.env` with anyone
- [ ] Rotate secrets every 3 months

### Credential Security
- [ ] Use strong passwords (20+ characters)
- [ ] Enable 2FA on Google account
- [ ] Enable 2FA on Microsoft account
- [ ] Review OAuth app permissions quarterly
- [ ] Delete unused OAuth apps

### API Security
- [ ] Set OAuth redirect URIs to localhost only
- [ ] Enable rate limiting on API calls
- [ ] Log failed authentication attempts
- [ ] Set API quotas/limits

---

## Phase 8: Production Deployment 🌐

### Choose Deployment Method
- [ ] Decision: Local, Cloud Server, or Serverless?
- [ ] See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for details

### Pre-Deployment Checklist
- [ ] All tests passing
- [ ] Error handling complete
- [ ] Logging configured
- [ ] Environment variables validated
- [ ] Dependencies audited for vulnerabilities
- [ ] Documentation updated
- [ ] Backups created
- [ ] Recovery procedures tested

### Deployment Steps (varies by method)

**For Render (Recommended)**
- [ ] Create Render account
- [ ] Create new service from GitHub
- [ ] Configure environment variables
- [ ] Set build command: `npm install`
- [ ] Set start command: `npm run start`
- [ ] Deploy and verify logs

**For Docker**
- [ ] Build image: `docker build -t email-sync .`
- [ ] Run container: `docker run -e GOOGLE_CLIENT_ID=xxx ...`
- [ ] Verify container health
- [ ] Set up auto-restart

**For Serverless (AWS Lambda)**
- [ ] Package code for Lambda
- [ ] Create Lambda function
- [ ] Configure IAM role
- [ ] Set environment variables
- [ ] Configure API Gateway (optional)

---

## Phase 9: Monitoring & Maintenance 📈

### Monitoring Setup
- [ ] Configure error tracking (Sentry)
- [ ] Set up performance monitoring (Datadog)
- [ ] Enable uptime monitoring (Uptime Robot)
- [ ] Configure alerts for errors
- [ ] Create dashboard for key metrics

### Regular Maintenance
- [ ] Weekly: Check error logs
- [ ] Monthly: Review API usage and quotas
- [ ] Quarterly: Rotate credentials
- [ ] Quarterly: Update dependencies
- [ ] Annually: Security audit

### Backup & Recovery
- [ ] Backup credentials daily
- [ ] Test recovery procedures monthly
- [ ] Document disaster recovery plan
- [ ] Practice failover procedures

---

## Phase 10: Advanced Features 🚀

### Phase 2 Integrations (Optional)
- [ ] Implement Slack notifications
- [ ] Add Todoist sync
- [ ] Create webhook triggers
- [ ] Build email rules engine

### Performance Optimization
- [ ] Implement caching layer
- [ ] Optimize database queries
- [ ] Add request compression
- [ ] Implement connection pooling

### Additional Features
- [ ] Multi-account management
- [ ] Custom email templates
- [ ] Advanced filtering rules
- [ ] Mobile app integration

---

## ✅ Final Verification

Run final integration test:
```bash
npm run verify
npm run start
```

In Claude Code:
```
Fetch my emails, summarize recent calendar events, and create a daily note
```

Expected result:
- ✅ Email list retrieved
- ✅ Calendar events summarized
- ✅ Obsidian note created with today's date
- ✅ All data displays in dashboard
- ✅ No errors in logs

---

## 🎉 Success!

If all items are checked, you've successfully:
- ✅ Set up email-sync MCP server
- ✅ Configured OAuth for Gmail and Outlook
- ✅ Integrated with Claude Code
- ✅ Tested all core functionality
- ✅ Prepared for production deployment

**Next Steps**:
1. Review [INTEGRATIONS_ROADMAP.md](./INTEGRATIONS_ROADMAP.md) for Phase 2 features
2. Choose deployment method from [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
3. Set up monitoring and alerting
4. Plan Phase 2 integrations (Slack, Todoist, Webhooks)

---

**Last Updated**: 2026-02-23
**Version**: 1.0
**Status**: Complete & Ready for Integration
