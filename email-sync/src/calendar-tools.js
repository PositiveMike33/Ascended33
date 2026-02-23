export const calendarTools = [
  {
    name: 'calendar-get-events',
    description:
      'Get upcoming calendar events from Google Calendar. Returns events for the next N days with time, title, and description.',
    inputSchema: {
      type: 'object',
      properties: {
        days: {
          type: 'number',
          description: 'Number of days to look ahead (default: 7)',
          default: 7,
        },
        account: {
          type: 'string',
          description: 'Email account to fetch from (default: "default")',
          default: 'default',
        },
      },
    },
  },
  {
    name: 'calendar-create-daily-note',
    description:
      'Create a daily note in Obsidian vault with calendar events for a specific date. Generates structured markdown file in THIRTY3/daily folder.',
    inputSchema: {
      type: 'object',
      properties: {
        date: {
          type: 'string',
          description: 'Date in YYYY-MM-DD format (e.g., "2024-01-15")',
        },
        account: {
          type: 'string',
          description: 'Email account to fetch calendar from (default: "default")',
          default: 'default',
        },
      },
      required: ['date'],
    },
  },
  {
    name: 'calendar-create-weekly-note',
    description:
      'Create a weekly summary note in Obsidian vault with all events for the week. Generates structured markdown file in REPORT/Declassified Report folder.',
    inputSchema: {
      type: 'object',
      properties: {
        weekStart: {
          type: 'string',
          description: 'Week start date in YYYY-MM-DD format (e.g., "2024-01-15")',
        },
        account: {
          type: 'string',
          description: 'Email account to fetch calendar from (default: "default")',
          default: 'default',
        },
      },
      required: ['weekStart'],
    },
  },
  {
    name: 'calendar-sync-and-notify',
    description:
      'Sync calendar events with Obsidian and send notifications for upcoming events. Checks for events in next 24 hours.',
    inputSchema: {
      type: 'object',
      properties: {
        account: {
          type: 'string',
          description: 'Email account to sync (default: "default")',
          default: 'default',
        },
        notificationMinutes: {
          type: 'number',
          description: 'Minutes before event to trigger notification (default: 15)',
          default: 15,
        },
      },
    },
  },
  {
    name: 'calendar-add-event-from-email',
    description:
      'Extract event information from email and create Google Calendar event. Parses date/time references from email content.',
    inputSchema: {
      type: 'object',
      properties: {
        emailId: {
          type: 'string',
          description: 'Gmail message ID to extract event from',
        },
        account: {
          type: 'string',
          description: 'Email account to add event to (default: "default")',
          default: 'default',
        },
      },
      required: ['emailId'],
    },
  },
];
