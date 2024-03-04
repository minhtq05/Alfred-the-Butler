import os
import os.path
import telebot
import requests
import base64
from linkedin_scrapper import linkedin_job_alert, linkedin_list_jobs
from codeforces_scrapper import list_contests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def debug(*args, **kwargs):
    print('+' + '-' * 20 + '+')
    print(*args, **kwargs)
    print('+' + '-' * 20 + '+')


class TelegramBot():

    def __init__(self):

        self.bot = telebot.TeleBot(BOT_TOKEN)
        self.gmail_service = self.gmail_init()
        if self.gmail_service == None:
            print(
                'Gmail API is not initialized correctly. Please check your credentials.')
            return
        print('Telegram bot started. Type /start or /hello to start a conversation.')

        @self.bot.message_handler(commands=['start', 'hello'])
        def greeting(message):
            self.bot.reply_to(message, 'Hello, how are you?')

        @self.bot.message_handler(commands=['gmail'])
        def gmail_handler(message):
            print('Doing Gmail stuff...')
            args = message.text.lower().split(' ')[1:]
            if len(args) < 1:
                self.bot.reply_to(
                    message, 'I have integrated your Gmail to this chat, sir. Please tell me what you want to do with your mails.')
            else:
                match args[0]:
                    case 'check':
                        self.labels = self.gmail_service.users().labels().list(
                            userId='me').execute().get('labels', [])
                        self.labels = [label['name'] for label in self.labels]
                        self.bot.reply_to(
                            message, 'Here is the list of your labels, sir.\n' + '\n'.join(self.labels))
                    case 'jobs' | 'j' | 'ja':
                        jobs = self.gmail_service.users().messages().list(userId='me',
                                                                          q='is:unread from:jobalerts-noreply@linkedin.com').execute().get('messages', [])
                        job_items = []
                        for jbs in jobs:
                            job_items.extend(linkedin_job_alert(
                                self.gmail_service, jbs))

                        if (num_jobs := len(job_items)) > 0:
                            self.bot.reply_to(
                                message, f'You have <strong>{num_jobs}</strong> unread jobs, sir.\nHere are all the jobs that you didn\'t read yet.\n', parse_mode='HTML')
                        else:
                            self.bot.reply_to(
                                message, 'You have no unread jobs, sir.')

                        linkedin_list_jobs(self.bot, message, job_items)
                    case _:
                        self.bot.reply_to(
                            message, 'Sorry sir, I don\'t know that command is. Please try again, sir.')

        @self.bot.message_handler(commands=['cf', 'codeforces'])
        def codeforces_handler(message):
            args = message.text.lower().split(' ')[1:]
            if len(args) < 1:
                self.bot.reply_to(
                    message, 'I have integrated CodeForces to this chat, sir. Please tell me what to do.')
            else:
                match args[0]:
                    case 'list' | 'l':
                        list_contests(
                            message, self.bot, ended='ended' in args, gym='gym' in args)
                    case 'p' | 'profile':
                        pass
                    case _:
                        self.bot.reply_to(
                            message, 'Sorry sir, I don\'t know that command is. Please try again, sir.')

        @self.bot.message_handler(commands=['test'])
        def test(message):
            pass

    def gmail_init(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file(
                'token.json', GMAIL_SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', GMAIL_SCOPES
                )
                creds = self.flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('credentials.json', 'w') as token:
                    token.write(creds.to_json())

        try:
            # Call the GMAIL API
            service = build("gmail", "v1", credentials=creds)
            # api = service.users().labels().list(userId='me').execute()
            print('Gmail API is initialized successfully.')
            return service
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None


if __name__ == '__main__':
    telegram_bot = TelegramBot()
    telegram_bot.bot.infinity_polling()
