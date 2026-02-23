# Phase 2 Implementation Template

Complete code templates for each Phase 2 integration. Copy these as starting points.

---

## 🟦 Slack Integration Template

### 1. Setup Script (`scripts/slack-setup.js`)

```javascript
import inquirer from 'inquirer';
import fs from 'fs';

export async function setupSlack() {
  console.log('\n🟦 Slack Integration Setup\n');

  const answers = await inquirer.prompt([
    {
      type: 'password',
      name: 'botToken',
      message: 'Enter your Slack Bot Token (from https://api.slack.com/apps):',
      validate: (val) => val.startsWith('xoxb-') || 'Must be a valid bot token (starts with xoxb-)'
    },
    {
      type: 'input',
      name: 'channelId',
      message: 'Enter default Slack channel ID (e.g., C123456789):',
      validate: (val) => val.match(/^C[A-Z0-9]+$/) || 'Invalid channel ID format'
    },
    {
      type: 'input',
      name: 'summaryTime',
      message: 'Daily summary time (HH:MM in UTC, default 09:00):',
      default: '09:00'
    }
  ]);

  // Read current .env
  let envContent = fs.readFileSync('.env', 'utf8');
  
  // Add/update Slack variables
  const slackVars = [
    `SLACK_BOT_TOKEN=${answers.botToken}`,
    `SLACK_CHANNEL_ID=${answers.channelId}`,
    `SLACK_SUMMARY_TIME=${answers.summaryTime}`
  ];

  slackVars.forEach(varLine => {
    const key = varLine.split('=')[0];
    const pattern = new RegExp(`^${key}=.*$`, 'm');
    if (pattern.test(envContent)) {
      envContent = envContent.replace(pattern, varLine);
    } else {
      envContent += `\n${varLine}`;
    }
  });

  fs.writeFileSync('.env', envContent);
  console.log('✅ Slack credentials saved to .env');
}
```

### 2. Tools File (`src/tools/slack.js`)

```javascript
import fetch from 'node-fetch';
import { logError, logSuccess } from '../config/logger.js';

const SLACK_API_BASE = 'https://slack.com/api';

class SlackManager {
  constructor(botToken) {
    this.botToken = botToken;
    this.headers = {
      'Authorization': `Bearer ${botToken}`,
      'Content-Type': 'application/json'
    };
  }

  async sendMessage(channelId, text, blocks = null) {
    try {
      const payload = {
        channel: channelId,
        text: text,
        ...(blocks && { blocks })
      };

      const response = await fetch(`${SLACK_API_BASE}/chat.postMessage`, {
        method: 'POST',
        headers: this.headers,
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (!data.ok) {
        throw new Error(data.error);
      }

      logSuccess(`Message sent to Slack channel ${channelId}`);
      return { success: true, messageTs: data.ts };
    } catch (error) {
      logError('Slack send failed', error);
      return { success: false, error: error.message };
    }
  }

  async sendEmailSummary(channelId, emails) {
    // Format emails into Slack blocks
    const blocks = [
      {
        type: 'header',
        text: {
          type: 'plain_text',
          text: `📧 Daily Email Summary (${emails.length} unread)`
        }
      }
    ];

    emails.slice(0, 5).forEach((email, i) => {
      blocks.push({
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*${i + 1}. ${email.from}*\n_${email.subject}_`
        }
      });
    });

    return this.sendMessage(channelId, 'Daily email summary', blocks);
  }

  async sendUrgentNotification(channelId, email) {
    const text = `🚨 *URGENT*\nFrom: ${email.from}\nSubject: ${email.subject}`;
    return this.sendMessage(channelId, text);
  }
}

export default SlackManager;
```

### 3. Tool Registration (Add to `src/index.js`)

```javascript
// In tools definition, add these:
{
  name: 'slack-send-summary',
  description: 'Send daily email summary to Slack',
  inputSchema: {
    type: 'object',
    properties: {
      channelId: {
        type: 'string',
        description: 'Slack channel ID (e.g., C123456789)'
      },
      summaryText: {
        type: 'string',
        description: 'Summary text to send'
      }
    },
    required: ['channelId', 'summaryText']
  }
},
{
  name: 'slack-notify-urgent',
  description: 'Send urgent email notification to Slack',
  inputSchema: {
    type: 'object',
    properties: {
      channelId: { type: 'string' },
      emailSubject: { type: 'string' },
      emailFrom: { type: 'string' }
    },
    required: ['channelId', 'emailSubject', 'emailFrom']
  }
},
{
  name: 'slack-sync-calendar',
  description: 'Post today\'s calendar events to Slack',
  inputSchema: {
    type: 'object',
    properties: {
      channelId: { type: 'string' }
    },
    required: ['channelId']
  }
}
```

---

## 🟦 Todoist Integration Template

### 1. Setup Script (`scripts/todoist-setup.js`)

```javascript
import inquirer from 'inquirer';
import fs from 'fs';

export async function setupTodoist() {
  console.log('\n📋 Todoist Integration Setup\n');

  const answers = await inquirer.prompt([
    {
      type: 'password',
      name: 'apiToken',
      message: 'Enter your Todoist API token (from https://todoist.com/app/settings/integrations/api):',
      validate: (val) => val.length > 20 || 'Invalid API token'
    },
    {
      type: 'input',
      name: 'inboxProjectId',
      message: 'Enter Inbox Project ID:',
      validate: (val) => !isNaN(val) || 'Must be a number'
    }
  ]);

  let envContent = fs.readFileSync('.env', 'utf8');
  
  const todoistVars = [
    `TODOIST_API_TOKEN=${answers.apiToken}`,
    `TODOIST_INBOX_PROJECT=${answers.inboxProjectId}`
  ];

  todoistVars.forEach(varLine => {
    const key = varLine.split('=')[0];
    const pattern = new RegExp(`^${key}=.*$`, 'm');
    if (pattern.test(envContent)) {
      envContent = envContent.replace(pattern, varLine);
    } else {
      envContent += `\n${varLine}`;
    }
  });

  fs.writeFileSync('.env', envContent);
  console.log('✅ Todoist credentials saved');
}
```

### 2. Tools File (`src/tools/todoist.js`)

```javascript
import fetch from 'node-fetch';

const TODOIST_API_BASE = 'https://api.todoist.com/rest/v2';

class TodoistManager {
  constructor(apiToken) {
    this.apiToken = apiToken;
    this.headers = {
      'Authorization': `Bearer ${apiToken}`,
      'Content-Type': 'application/json'
    };
  }

  async createTask(projectId, content, description = '', dueDateUtc = null) {
    try {
      const payload = {
        content,
        description,
        project_id: parseInt(projectId),
        ...(dueDateUtc && { due_date: dueDateUtc })
      };

      const response = await fetch(`${TODOIST_API_BASE}/tasks`, {
        method: 'POST',
        headers: this.headers,
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const task = await response.json();
      return { success: true, taskId: task.id, taskUrl: task.url };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  async createTaskFromEmail(projectId, email) {
    // Extract action items from email subject/body
    const content = `[${email.from}] ${email.subject}`;
    const description = email.body?.substring(0, 500) || '';

    // Parse due date if mentioned
    const dueDateMatch = email.body?.match(/due[:\s]+(\d{1,2}\/\d{1,2})/i);
    let dueDate = null;
    if (dueDateMatch) {
      // Parse and format date
      dueDate = dueDateMatch[1]; // You'd normally parse this properly
    }

    return this.createTask(projectId, content, description, dueDate);
  }

  async getProjects() {
    try {
      const response = await fetch(`${TODOIST_API_BASE}/projects`, {
        headers: this.headers
      });

      const projects = await response.json();
      return { success: true, projects };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}

export default TodoistManager;
```

---

## 🟦 Webhook Integration Template

### 1. Webhook Manager (`src/tools/webhooks.js`)

```javascript
import fetch from 'node-fetch';
import { v4 as uuidv4 } from 'uuid';

class WebhookManager {
  constructor() {
    this.webhooks = new Map(); // In-memory store, use DB in production
  }

  registerWebhook(url, events = ['email.received', 'email.urgent'], label = '') {
    const webhookId = uuidv4();
    
    this.webhooks.set(webhookId, {
      id: webhookId,
      url,
      events,
      label,
      createdAt: new Date(),
      lastTriggered: null,
      failureCount: 0
    });

    return {
      success: true,
      webhookId,
      message: `Webhook registered for events: ${events.join(', ')}`
    };
  }

  async triggerWebhook(webhookId, event, payload) {
    const webhook = this.webhooks.get(webhookId);
    if (!webhook) {
      return { success: false, error: 'Webhook not found' };
    }

    if (!webhook.events.includes(event)) {
      return { success: false, error: 'Event not subscribed' };
    }

    try {
      const response = await fetch(webhook.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Webhook-ID': webhookId,
          'X-Webhook-Event': event
        },
        body: JSON.stringify({
          event,
          timestamp: new Date().toISOString(),
          data: payload
        }),
        timeout: 5000
      });

      webhook.lastTriggered = new Date();

      if (!response.ok) {
        webhook.failureCount++;
        return { success: false, error: `HTTP ${response.status}` };
      }

      webhook.failureCount = 0;
      return { success: true };
    } catch (error) {
      webhook.failureCount++;
      return { success: false, error: error.message };
    }
  }

  listWebhooks() {
    return Array.from(this.webhooks.values()).map(w => ({
      id: w.id,
      url: w.url,
      events: w.events,
      label: w.label,
      lastTriggered: w.lastTriggered,
      status: w.failureCount > 3 ? 'failing' : 'active'
    }));
  }

  deleteWebhook(webhookId) {
    if (this.webhooks.delete(webhookId)) {
      return { success: true };
    }
    return { success: false, error: 'Webhook not found' };
  }
}

export default WebhookManager;
```

---

## 📋 .env Example for Phase 2

Add these to your `.env` file:

```bash
# Phase 1 (existing)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
MICROSOFT_CLIENT_ID=...
MICROSOFT_CLIENT_SECRET=...

# Phase 2 - Slack
SLACK_BOT_TOKEN=xoxb-...
SLACK_CHANNEL_ID=C123456789
SLACK_SUMMARY_TIME=09:00

# Phase 2 - Todoist
TODOIST_API_TOKEN=...
TODOIST_INBOX_PROJECT=123456789

# Phase 2 - Webhooks (optional)
WEBHOOK_PORT=3001
WEBHOOK_TIMEOUT=5000
```

---

## 📝 Testing Template

Create `scripts/test-integration.js`:

```javascript
async function testSlack() {
  const slack = new SlackManager(process.env.SLACK_BOT_TOKEN);
  
  const result = await slack.sendMessage(
    process.env.SLACK_CHANNEL_ID,
    '✅ Test message from email-sync MCP'
  );
  
  console.log(result.success ? 'Slack test passed' : 'Slack test failed');
}

async function testTodoist() {
  const todoist = new TodoistManager(process.env.TODOIST_API_TOKEN);
  
  const result = await todoist.createTask(
    process.env.TODOIST_INBOX_PROJECT,
    '✅ Test task from email-sync MCP'
  );
  
  console.log(result.success ? 'Todoist test passed' : 'Todoist test failed');
}

export { testSlack, testTodoist };
```

---

## ✅ Integration Checklist

After implementing each integration:

- [ ] Tool functions implemented and tested locally
- [ ] Error handling for API failures
- [ ] Rate limiting respected (check API docs)
- [ ] Credentials stored in `.env` (not hardcoded)
- [ ] MCP tools registered in `index.js`
- [ ] Tool schemas match API requirements
- [ ] Real-world test with actual emails
- [ ] Works in Claude Code MCP list
- [ ] Documentation updated with examples
- [ ] Git commit with clear message

---

Use these templates to build Phase 2! 🚀
