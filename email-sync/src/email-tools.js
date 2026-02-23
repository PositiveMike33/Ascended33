export const emailTools = [
  {
    name: 'gmail-fetch-emails',
    description:
      'Fetch recent emails from Gmail account. Returns up to specified limit of emails with subject, sender, date, and preview.',
    inputSchema: {
      type: 'object',
      properties: {
        limit: {
          type: 'number',
          description: 'Maximum number of emails to fetch (default: 10, max: 50)',
          default: 10,
        },
      },
    },
  },
  {
    name: 'gmail-send-email',
    description:
      'Send an email via Gmail account. Supports plain text and HTML body.',
    inputSchema: {
      type: 'object',
      properties: {
        to: {
          type: 'string',
          description: 'Recipient email address (supports multiple: email1@example.com, email2@example.com)',
        },
        subject: {
          type: 'string',
          description: 'Email subject line',
        },
        body: {
          type: 'string',
          description: 'Email body (plain text or HTML)',
        },
        cc: {
          type: 'string',
          description: 'CC recipients (optional)',
        },
        bcc: {
          type: 'string',
          description: 'BCC recipients (optional)',
        },
      },
      required: ['to', 'subject', 'body'],
    },
  },
  {
    name: 'gmail-search-emails',
    description:
      'Search emails in Gmail using Gmail search syntax. Supports filters like: from:, to:, subject:, label:, is:unread, before:, after:, etc.',
    inputSchema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'Gmail search query (e.g., "from:john@example.com is:unread")',
        },
        limit: {
          type: 'number',
          description: 'Maximum number of results (default: 5, max: 50)',
          default: 5,
        },
      },
      required: ['query'],
    },
  },
  {
    name: 'outlook-fetch-emails',
    description:
      'Fetch recent emails from Outlook/Microsoft Exchange account. Returns up to specified limit of emails.',
    inputSchema: {
      type: 'object',
      properties: {
        limit: {
          type: 'number',
          description: 'Maximum number of emails to fetch (default: 10, max: 50)',
          default: 10,
        },
      },
    },
  },
  {
    name: 'outlook-send-email',
    description:
      'Send an email via Outlook/Microsoft Exchange account. Supports plain text and HTML body.',
    inputSchema: {
      type: 'object',
      properties: {
        to: {
          type: 'string',
          description: 'Recipient email address',
        },
        subject: {
          type: 'string',
          description: 'Email subject line',
        },
        body: {
          type: 'string',
          description: 'Email body (plain text or HTML)',
        },
        cc: {
          type: 'string',
          description: 'CC recipients (optional)',
        },
        bcc: {
          type: 'string',
          description: 'BCC recipients (optional)',
        },
      },
      required: ['to', 'subject', 'body'],
    },
  },
];
