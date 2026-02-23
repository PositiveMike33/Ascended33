import { Client } from '@microsoft/microsoft-graph-client';
import 'isomorphic-fetch';

class OutlookManager {
  constructor() {
    this.client = null;
    this.authToken = null;
  }

  async authorize() {
    if (!process.env.MICROSOFT_CLIENT_ID) {
      throw new Error(
        'MICROSOFT_CLIENT_ID not set in .env. Complete OAuth setup first.'
      );
    }

    // Note: This is a placeholder. Real implementation requires Azure SDK
    // for token acquisition with Device Flow or other OAuth flows.
    this.client = Client.init({
      authProvider: async (done) => {
        done(null, this.authToken);
      },
    });
  }

  async fetchEmails(limit = 10) {
    if (!this.client) await this.authorize();

    try {
      const response = await this.client
        .api('/me/mailFolders/inbox/messages')
        .select(['subject', 'from', 'receivedDateTime', 'bodyPreview'])
        .top(Math.min(limit, 50))
        .get();

      return response.value.map((msg) => ({
        id: msg.id,
        from: msg.from.emailAddress.address,
        subject: msg.subject,
        date: msg.receivedDateTime,
        snippet: msg.bodyPreview,
      }));
    } catch (error) {
      console.error('Error fetching Outlook emails:', error);
      throw error;
    }
  }

  async sendEmail(to, subject, body, cc = null, bcc = null) {
    if (!this.client) await this.authorize();

    try {
      const message = {
        subject,
        body: {
          contentType: 'HTML',
          content: body,
        },
        toRecipients: [
          {
            emailAddress: {
              address: to,
            },
          },
        ],
      };

      if (cc) {
        message.ccRecipients = [
          {
            emailAddress: {
              address: cc,
            },
          },
        ];
      }

      if (bcc) {
        message.bccRecipients = [
          {
            emailAddress: {
              address: bcc,
            },
          },
        ];
      }

      await this.client.api('/me/sendMail').post({
        message,
      });

      return { success: true };
    } catch (error) {
      console.error('Error sending Outlook email:', error);
      throw error;
    }
  }

  async searchEmails(query, limit = 5) {
    if (!this.client) await this.authorize();

    try {
      const response = await this.client
        .api('/me/mailFolders/inbox/messages')
        .select(['subject', 'from', 'receivedDateTime', 'bodyPreview'])
        .search(query)
        .top(Math.min(limit, 50))
        .get();

      return response.value.map((msg) => ({
        id: msg.id,
        from: msg.from.emailAddress.address,
        subject: msg.subject,
        date: msg.receivedDateTime,
        snippet: msg.bodyPreview,
      }));
    } catch (error) {
      console.error('Error searching Outlook emails:', error);
      throw error;
    }
  }
}

export default OutlookManager;
