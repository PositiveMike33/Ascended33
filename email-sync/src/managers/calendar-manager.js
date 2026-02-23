import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';

class CalendarManager {
  constructor() {
    this.oauth2Client = null;
    this.calendar = null;
    this.credentialsPath = path.join(process.cwd(), 'config', 'credentials.json');
    this.tokenPath = path.join(process.cwd(), 'config', 'token.json');
  }

  async authorize() {
    if (!fs.existsSync(this.credentialsPath)) {
      throw new Error(
        `Google OAuth credentials not found at ${this.credentialsPath}`
      );
    }

    const credentials = JSON.parse(fs.readFileSync(this.credentialsPath));
    const { client_id, client_secret, redirect_uris } = credentials.installed;

    this.oauth2Client = new google.auth.OAuth2(
      client_id,
      client_secret,
      redirect_uris[0]
    );

    if (fs.existsSync(this.tokenPath)) {
      const token = JSON.parse(fs.readFileSync(this.tokenPath));
      this.oauth2Client.setCredentials(token);
    }

    this.calendar = google.calendar({
      version: 'v3',
      auth: this.oauth2Client,
    });
  }

  async getUpcomingEvents(days = 7, account = 'default') {
    if (!this.calendar) await this.authorize();

    try {
      const now = new Date();
      const endDate = new Date();
      endDate.setDate(endDate.getDate() + days);

      const response = await this.calendar.events.list({
        calendarId: 'primary',
        timeMin: now.toISOString(),
        timeMax: endDate.toISOString(),
        singleEvents: true,
        orderBy: 'startTime',
      });

      return response.data.items.map((event) => ({
        id: event.id,
        summary: event.summary,
        start: event.start.dateTime || event.start.date,
        end: event.end.dateTime || event.end.date,
        description: event.description || '',
      }));
    } catch (error) {
      console.error('Error fetching calendar events:', error);
      throw error;
    }
  }

  async createDailyNote(date, account = 'default') {
    if (!this.calendar) await this.authorize();

    try {
      const startDate = new Date(date);
      const endDate = new Date(date);
      endDate.setDate(endDate.getDate() + 1);

      const response = await this.calendar.events.list({
        calendarId: 'primary',
        timeMin: startDate.toISOString(),
        timeMax: endDate.toISOString(),
        singleEvents: true,
        orderBy: 'startTime',
      });

      const events = response.data.items || [];
      const vaultPath = process.env.OBSIDIAN_VAULT_PATH || './vault';
      const dailyFolder = process.env.OBSIDIAN_DAILY_FOLDER || 'daily';

      // Format: YYYY-MM-DD - Daily Note.md
      const fileName = `${date} - Daily Note.md`;
      const filePath = path.join(vaultPath, dailyFolder, fileName);

      let content = `# ${date} - Daily Plan\n\n`;
      content += `## Calendar Events\n\n`;

      if (events.length === 0) {
        content += `No events scheduled.\n\n`;
      } else {
        events.forEach((event) => {
          const start = new Date(event.start.dateTime || event.start.date);
          const time = start.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
          });
          content += `- **${time}** - ${event.summary}\n`;
          if (event.description) {
            content += `  ${event.description}\n`;
          }
        });
      }

      content += `\n## Tasks\n\n- [ ] Task 1\n- [ ] Task 2\n\n`;
      content += `## Notes\n\n`;

      fs.mkdirSync(path.dirname(filePath), { recursive: true });
      fs.writeFileSync(filePath, content);

      return filePath;
    } catch (error) {
      console.error('Error creating daily note:', error);
      throw error;
    }
  }

  async createWeeklyNote(weekStart, account = 'default') {
    if (!this.calendar) await this.authorize();

    try {
      const start = new Date(weekStart);
      const end = new Date(weekStart);
      end.setDate(end.getDate() + 7);

      const response = await this.calendar.events.list({
        calendarId: 'primary',
        timeMin: start.toISOString(),
        timeMax: end.toISOString(),
        singleEvents: true,
        orderBy: 'startTime',
      });

      const events = response.data.items || [];
      const vaultPath = process.env.OBSIDIAN_VAULT_PATH || './vault';
      const reportFolder =
        process.env.OBSIDIAN_ARCHIVE_FOLDER || 'report/declassified';

      const fileName = `${weekStart} - Weekly Summary.md`;
      const filePath = path.join(vaultPath, reportFolder, fileName);

      let content = `# Week of ${weekStart} - Summary\n\n`;
      content += `## Events\n\n`;

      if (events.length === 0) {
        content += `No events this week.\n\n`;
      } else {
        events.forEach((event) => {
          const start = new Date(event.start.dateTime || event.start.date);
          const dateStr = start.toLocaleDateString('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
          });
          const time = start.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
          });
          content += `- **${dateStr}** at ${time} - ${event.summary}\n`;
        });
      }

      content += `\n## Accomplishments\n\n- \n\n`;
      content += `## Next Week Focus\n\n- \n\n`;

      fs.mkdirSync(path.dirname(filePath), { recursive: true });
      fs.writeFileSync(filePath, content);

      return filePath;
    } catch (error) {
      console.error('Error creating weekly note:', error);
      throw error;
    }
  }

  async syncAndNotify(account = 'default', notificationMinutes = 15) {
    // Placeholder for notification logic
    // Real implementation would use system notifications
    return { success: true, message: 'Sync completed' };
  }

  async addEventFromEmail(emailId, account = 'default') {
    // Placeholder for email-to-calendar conversion
    // Would parse email content and create calendar event
    return { success: true, eventId: 'created-event-id' };
  }
}

export default CalendarManager;
