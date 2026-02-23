# ✅ Phase 2 Execution Checklist

**Status**: Ready to Start Phase 2 Implementation  
**Target Start Date**: Week of February 24, 2026  
**Estimated Duration**: 4 weeks (3-4 hours per integration)  
**Team**: Solo development (Claude Code assistance available)

---

## 🎯 Quick Start (Do This First)

### Step 0: Restore Dependencies (5 minutes)
```bash
cd email-sync
npm install --legacy-peer-deps
```

**Verify Success:**
```bash
npm ls slack-api todoist  # Should not error
node -e "console.log('Node works')"
```

---

## 📋 Phase 2 Integration Sequence

### Week 1: Slack Integration (Recommended First) ⭐

**Why Slack First?**
- Highest productivity impact (40% gain in notification processing)
- Fastest implementation (3 hours)
- Best for daily use case (urgent email alerts)
- Simplest API (Slack Web API)
- Clear success metrics (message delivery time, user response time)

#### Pre-Implementation Checklist

- [ ] **Slack Workspace Setup**
  - [ ] Navigate to: https://api.slack.com/apps
  - [ ] Click "Create New App" → "From scratch"
  - [ ] Name: `email-sync-bot`
  - [ ] Pick workspace
  - [ ] Save APP_ID and CLIENT_SECRET

- [ ] **Bot Token Scopes**
  - [ ] Go to "OAuth & Permissions" in left menu
  - [ ] Add these Bot Token Scopes:
    - `chat:write` (send messages)
    - `chat:write.public` (send in public channels)
    - `files:write` (upload files)
    - `channels:read` (list channels)
    - `users:read` (get user info)
  - [ ] Copy Bot User OAuth Token (starts with `xoxb-`)

- [ ] **Event Subscriptions** (Optional for Phase 2.1)
  - [ ] Enable Events
  - [ ] Request URL: `https://your-webhook-domain/slack/events`
  - [ ] Subscribe to: `message.channels`, `app_mention`
  - [ ] (Setup in Phase 2.3 Webhooks if async needed)

- [ ] **Environment Setup**
  ```bash
  # Add to .env in email-sync/
  SLACK_BOT_TOKEN=xoxb-your-token-here
  SLACK_WORKSPACE_ID=T00000000
  ```

#### Implementation Steps

1. **Copy Template Code** (2 mins)
   - Open: `docs/PHASE_2_IMPLEMENTATION_TEMPLATE.md`
   - Copy "Slack Integration" section
   - Paste into `src/managers/slack-manager.js` (create if needed)

2. **Setup Script** (5 mins)
   - Copy "Slack Setup Script" from template
   - Paste into `scripts/slack-setup.js`
   - Run: `node scripts/slack-setup.js`
   - This will interactively configure your Slack connection

3. **Register MCP Tools** (10 mins)
   - Copy "Slack MCP Tools" from template
   - Add to `src/index.js` server registration
   - Tools to add: `slack-send-message`, `slack-send-summary`, `slack-send-alert`

4. **Test Slack Tools** (20 mins)
   - Create `test-slack.js`:
     ```javascript
     const SlackManager = require('./src/managers/slack-manager');
     const manager = new SlackManager(process.env.SLACK_BOT_TOKEN);
     
     (async () => {
       const result = await manager.sendMessage('C1234567', 'Test from email-sync');
       console.log('✅ Slack works:', result);
     })();
     ```
   - Run: `node test-slack.js`
   - Verify message appears in Slack

5. **Add Urgent Email Trigger** (30 mins)
   - In `src/email-tools.js`, add Slack notification for high-priority emails
   - Trigger: Emails with subject contains "URGENT" or from VIP senders
   - Action: Call `slack-send-alert` MCP tool

6. **Manual Testing** (15 mins)
   - Send test email with subject "URGENT TEST"
   - Verify Slack notification arrives within 30 seconds
   - Test from Claude Code with manual MCP tool calls

**Success Criteria for Slack:**
- ✅ Bot token configured and validated
- ✅ `slack-send-message` sends to test channel
- ✅ `slack-send-summary` formats email summary
- ✅ `slack-send-alert` triggers on urgent emails
- ✅ Messages appear within 2 seconds of trigger

**Estimated Time**: 90 minutes

---

### Week 2: Todoist Integration

**Why Todoist Second?**
- Complements Slack (convert alerts to tasks)
- Medium complexity (4-5 API endpoints)
- Valuable for task management workflow
- Clear scope (create, list, close tasks)
- Reduces manual task creation by 60%

#### Pre-Implementation Checklist

- [ ] **Todoist Setup**
  - [ ] Log in to https://todoist.com
  - [ ] Go to Settings → Integrations → Developer
  - [ ] Generate API token (will start with secret key)
  - [ ] Copy API token

- [ ] **Todoist Project ID**
  - [ ] Create project named: `from-email-sync`
  - [ ] Go to project → Share → copy URL
  - [ ] Extract project ID from URL or use API to list projects
  - [ ] Example: `https://todoist.com/app/project/123456` → ID is `123456`

- [ ] **Environment Setup**
  ```bash
  # Add to .env in email-sync/
  TODOIST_API_TOKEN=your-token-here
  TODOIST_PROJECT_ID=123456
  ```

#### Implementation Steps

1. **Copy Template Code** (2 mins)
   - Open: `docs/PHASE_2_IMPLEMENTATION_TEMPLATE.md`
   - Copy "Todoist Integration" section
   - Paste into `src/managers/todoist-manager.js` (create if needed)

2. **Setup Script** (5 mins)
   - Copy "Todoist Setup Script" from template
   - Paste into `scripts/todoist-setup.js`
   - Run: `node scripts/todoist-setup.js`

3. **Register MCP Tools** (10 mins)
   - Copy "Todoist MCP Tools" from template
   - Add to `src/index.js`
   - Tools to add: `todoist-create-task`, `todoist-list-tasks`, `todoist-close-task`

4. **Integration with Slack** (20 mins)
   - When Slack receives urgent email alert, offer "Create Task" button
   - Or: Create automatic task from high-priority emails
   - Task format: `[EMAIL] Subject from sender@example.com`

5. **Manual Testing** (15 mins)
   - Call `todoist-create-task` from Claude Code MCP
   - Verify task appears in Todoist project within 5 seconds
   - Test task closure flow

**Success Criteria for Todoist:**
- ✅ API token validated
- ✅ Project ID correctly identifies target project
- ✅ `todoist-create-task` creates task with description and due date
- ✅ `todoist-list-tasks` returns all project tasks
- ✅ `todoist-close-task` marks task as complete

**Estimated Time**: 60 minutes

---

### Week 3: Webhooks Infrastructure

**Why Webhooks Third?**
- Enables real-time, bidirectional sync
- Supports future integrations (Zapier, IFTTT, custom services)
- Medium-low complexity (3 endpoints)
- Maximum flexibility for Phase 2.4+

#### Pre-Implementation Checklist

- [ ] **Deployment Decision**
  - [ ] Local testing: Use ngrok or similar for webhook tunnel
  - [ ] Production: Use serverless (Vercel, Render) for webhook endpoint
  - [ ] Option A: Deploy to Vercel (recommended for quick start)
  - [ ] Option B: Deploy to Render (recommended for always-on)
  - [ ] Option C: Use ngrok locally for testing first

- [ ] **Webhook Service Setup**
  - [ ] Choose deployment platform
  - [ ] Set up webhook listener endpoint: `POST /webhooks/email-event`
  - [ ] Set up webhook manager endpoint: `GET /webhooks/list`, `POST /webhooks/register`, `DELETE /webhooks/:id`

#### Implementation Steps

1. **Copy Template Code** (2 mins)
   - Open: `docs/PHASE_2_IMPLEMENTATION_TEMPLATE.md`
   - Copy "Webhook Integration" section
   - Paste into `src/managers/webhook-manager.js`

2. **Setup Webhook Manager** (10 mins)
   - Register webhook endpoints in MCP server
   - Tools: `webhook-register`, `webhook-trigger`, `webhook-list`, `webhook-delete`
   - Create webhook registry (in-memory or simple file-based)

3. **Test Webhook Flow** (20 mins)
   - Register test webhook to https://webhook.site (free temporary endpoint)
   - Trigger email event
   - Verify webhook.site receives the event
   - Check event contains proper payload: email_id, sender, subject, body, attachments

4. **Deploy Webhook Listener** (30 mins)
   - Choose Vercel, Render, or ngrok
   - Follow `docs/DEPLOYMENT_GUIDE.md`
   - Test endpoint availability and latency

**Success Criteria for Webhooks:**
- ✅ Webhook registration saves and retrieves webhook URLs
- ✅ Webhook triggering sends HTTP POST to registered URLs
- ✅ Event payload includes all email metadata
- ✅ Webhook delivery succeeds within 5 seconds
- ✅ Failed webhooks log errors for debugging

**Estimated Time**: 120 minutes

---

### Week 4: Integration & Refinement

#### Testing Phase (3 hours)

- [ ] **End-to-End Test Workflow**
  1. Send email to gmail (URGENT subject)
  2. Verify Slack notification arrives (< 2 sec)
  3. Click/call Todoist create task from Slack
  4. Verify task appears in Todoist (< 2 sec)
  5. Verify webhook triggers on email event
  6. Verify all logs show successful operations

- [ ] **Performance Benchmarking**
  - [ ] Email → Slack notification: measure latency
  - [ ] Email → Todoist task: measure latency
  - [ ] Webhook delivery: measure success rate
  - [ ] Log results to `docs/PHASE_2_PERFORMANCE_METRICS.md`

- [ ] **Error Handling Validation**
  - [ ] Test with invalid Slack token (should show error)
  - [ ] Test with invalid Todoist token (should show error)
  - [ ] Test webhook to dead URL (should handle gracefully)
  - [ ] Verify error messages are user-friendly

#### Refinement (1-2 hours)

- [ ] **User Experience Improvements**
  - [ ] Polish Slack message formatting (use blocks API)
  - [ ] Add emoji reactions to match email priority
  - [ ] Create task with auto-assigned due dates (1 day for normal, immediate for urgent)
  - [ ] Add dashboard widget showing Slack/Todoist stats

- [ ] **Documentation Updates**
  - [ ] Create Phase 2 User Guide
  - [ ] Record usage examples for each integration
  - [ ] Create troubleshooting guide

---

## 🚀 Daily Implementation Workflow

### Morning (Before Starting)
- [ ] Check `PHASE_2_LAUNCH_GUIDE.md` for current week's integration
- [ ] Review success criteria for that integration
- [ ] Copy relevant template code to local branch

### During Development
- [ ] Use Claude Code MCP tools to test each function
- [ ] Create `test-[integration].js` for manual testing
- [ ] Keep a running log in `PHASE_2_DEV_LOG.md`

### End of Day
- [ ] Run full test suite
- [ ] Update `PHASE_2_STATUS.md` with progress
- [ ] Commit changes to git branch `phase-2-[integration]`

---

## 📊 Success Metrics

| Metric | Target | Week |
|--------|--------|------|
| Slack integration complete | All tools working | Week 1 |
| Urgent emails → Slack alerts | <2 sec latency | Week 1 |
| Todoist integration complete | All tools working | Week 2 |
| Email → Task conversion | <3 sec latency | Week 2 |
| Webhook infrastructure deployed | Endpoint accessible | Week 3 |
| End-to-end workflow | All 3 tools working together | Week 4 |
| Performance metrics documented | All latencies < 5 sec | Week 4 |
| User satisfaction | All features working as expected | Week 4 |

---

## 🆘 Troubleshooting Quick Links

- **npm install fails**: See section "Restore Dependencies" above
- **Slack token invalid**: Regenerate from https://api.slack.com/apps → Bot User OAuth Token
- **Todoist API errors**: Check API token and project ID in `.env`
- **Webhook not delivering**: Check webhook URL is publicly accessible, logs for errors
- **MCP tools not available**: Restart Claude Code, check `.mcp.json` configuration

---

## 📚 Supporting Documentation

| Document | Purpose | Read When |
|----------|---------|-----------|
| `PHASE_2_LAUNCH_GUIDE.md` | Strategic overview & decision framework | Before starting Phase 2 |
| `PHASE_2_IMPLEMENTATION_TEMPLATE.md` | Ready-to-use code templates | When implementing each integration |
| `PHASE_2_STATUS.md` | Project status dashboard | Daily progress check |
| `INTEGRATIONS_ROADMAP.md` | All integration options for Phase 2-4 | When planning future work |
| `DEPLOYMENT_GUIDE.md` | Deployment to production | Before Week 3 webhooks |
| `OAUTH_SETUP_GUIDE.md` | OAuth token management | Reference for credential setup |
| `MCP_INTEGRATION.md` | MCP server details | If debugging MCP issues |

---

## ✨ Phase 2 Complete Success

When all items below are checked, Phase 2 is complete:

- [ ] Slack integration deployed and working
- [ ] Todoist integration deployed and working
- [ ] Webhook infrastructure deployed and working
- [ ] All MCP tools callable from Claude Code
- [ ] End-to-end workflow tested and documented
- [ ] Performance metrics documented
- [ ] User guide and troubleshooting guide created
- [ ] Git history clean with clear commit messages
- [ ] Ready for Phase 3: Advanced Multi-Platform Sync

---

**Next Step**: Run `npm install --legacy-peer-deps` to restore dependencies, then begin Week 1 Slack Implementation.

**Questions?** Reference the supporting documentation above or run:
```bash
grep -r "Slack" docs/ | grep -i "error\|troubleshoot"
```

