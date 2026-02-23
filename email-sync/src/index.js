import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import GmailManager from './managers/gmail-manager.js';
import OutlookManager from './managers/outlook-manager.js';
import CalendarManager from './managers/calendar-manager.js';
import { emailTools } from './email-tools.js';
import { calendarTools } from './calendar-tools.js';

const server = new Server(
  {
    name: 'email-sync-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Initialize managers
const gmail = new GmailManager();
const outlook = new OutlookManager();
const calendar = new CalendarManager();

// Tool listing
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [...emailTools, ...calendarTools],
  };
});

// Tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request;

  try {
    switch (name) {
      // Gmail operations
      case 'gmail-fetch-emails':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await gmail.fetchEmails(args.limit || 10),
                null,
                2
              ),
            },
          ],
        };

      case 'gmail-send-email':
        await gmail.sendEmail(args.to, args.subject, args.body);
        return {
          content: [{ type: 'text', text: 'Email sent successfully' }],
        };

      case 'gmail-search-emails':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await gmail.searchEmails(args.query, args.limit || 5),
                null,
                2
              ),
            },
          ],
        };

      // Outlook operations
      case 'outlook-fetch-emails':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await outlook.fetchEmails(args.limit || 10),
                null,
                2
              ),
            },
          ],
        };

      case 'outlook-send-email':
        await outlook.sendEmail(args.to, args.subject, args.body);
        return {
          content: [{ type: 'text', text: 'Email sent successfully' }],
        };

      // Calendar operations
      case 'calendar-get-events':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await calendar.getUpcomingEvents(
                  args.days || 7,
                  args.account || 'default'
                ),
                null,
                2
              ),
            },
          ],
        };

      case 'calendar-create-daily-note':
        const dailyResult = await calendar.createDailyNote(
          args.date,
          args.account || 'default'
        );
        return {
          content: [{ type: 'text', text: `Daily note created: ${dailyResult}` }],
        };

      case 'calendar-create-weekly-note':
        const weeklyResult = await calendar.createWeeklyNote(
          args.weekStart,
          args.account || 'default'
        );
        return {
          content: [
            { type: 'text', text: `Weekly note created: ${weeklyResult}` },
          ],
        };

      default:
        return {
          content: [
            {
              type: 'text',
              text: `Unknown tool: ${name}`,
            },
          ],
          isError: true,
        };
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error executing tool ${name}: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Email Sync MCP Server running on stdio');
}

main().catch(console.error);
