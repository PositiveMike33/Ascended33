import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';

class GmailManager {
  constructor() {
    this.oauth2Client = null;
    this.gmail = null;
    this.credentialsPath = path.join(process.cwd(), 'config', 'credentials.json');
    this.tokenPath = path.join(process.cwd(), 'config', 'token.json');
  }

  async authorize() {
    if (!fs.existsSync(this.credentialsPath)) {
      throw new Error(
        `Google OAuth credentials not found at ${this.credentialsPath}. Run "npm run setup" first.`
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

      // Refresh token if expired
      if (token.expiry_date && token.expiry_date < Date.now()) {
        const { credentials } = await this.oauth2Client.refreshAccessToken();
        this.oauth2Client.setCredentials(credentials);
        fs.writeFileSync(
          this.tokenPath,
          JSON.stringify(credentials, null, 2)
        );
      }
    } else {
      throw new Error(
        `Google OAuth token not found at ${this.tokenPath}. Complete OAuth flow first.`
      );
    }

    this.gmail = google.gmail({ version: 'v1', auth: this.oauth2Client });
  }

  async fetchEmails(limit = 10) {
    if (!this.gmail) await this.authorize();

    try {
      const response = await this.gmail.users.messages.list({
        userId: 'me',
        maxResults: Math.min(limit, 50),
      });

      const messageIds = response.data.messages || [];
      const emails = [];

      for (const msg of messageIds) {
        const message = await this.gmail.users.messages.get({
          userId: 'me',
          id: msg.id,
          format: 'metadata',
          metadataHeaders: ['From', 'Subject', 'Date'],
        });

        const headers = message.data.payload.headers.reduce((acc, h) => {
          acc[h.name] = h.value;
          return acc;
        }, {});

        emails.push({
          id: msg.id,
          from: headers.From,
          subject: headers.Subject,
          date: headers.Date,
          snippet: message.data.snippet,
        });
      }

      return emails;
    } catch (error) {
      console.error('Error fetching emails:', error);
      throw error;
    }
  }

  async sendEmail(to, subject, body, cc = null, bcc = null) {
    if (!this.gmail) await this.authorize();

    try {
      const email = this.createMessage(to, subject, body, cc, bcc);
      const response = await this.gmail.users.messages.send({
        userId: 'me',
        requestBody: {
          raw: email,
        },
      });

      return response.data;
    } catch (error) {
      console.error('Error sending email:', error);
      throw error;
    }
  }

  async searchEmails(query, limit = 5) {
    if (!this.gmail) await this.authorize();

    try {
      const response = await this.gmail.users.messages.list({
        userId: 'me',
        q: query,
        maxResults: Math.min(limit, 50),
      });

      const messageIds = response.data.messages || [];
      const emails = [];

      for (const msg of messageIds) {
        const message = await this.gmail.users.messages.get({
          userId: 'me',
          id: msg.id,
          format: 'metadata',
          metadataHeaders: ['From', 'Subject', 'Date'],
        });

        const headers = message.data.payload.headers.reduce((acc, h) => {
          acc[h.name] = h.value;
          return acc;
        }, {});

        emails.push({
          id: msg.id,
          from: headers.From,
          subject: headers.Subject,
          date: headers.Date,
          snippet: message.data.snippet,
        });
      }

      return emails;
    } catch (error) {
      console.error('Error searching emails:', error);
      throw error;
    }
  }

  createMessage(to, subject, body, cc = null, bcc = null) {
    let headers = `To: ${to}\r\nSubject: ${subject}\r\n`;
    if (cc) headers += `Cc: ${cc}\r\n`;
    if (bcc) headers += `Bcc: ${bcc}\r\n`;

    const message =
      headers + `Content-Type: text/html; charset="UTF-8"\r\n\r\n` + body;
    const encodedMessage = Buffer.from(message)
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');

    return encodedMessage;
  }
}

export default GmailManager;
