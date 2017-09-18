import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers import mail
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging

from . import config


class SendGrid:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__qualname__)
        self.sg = SendGridAPIClient(apikey=config.SENDGRID['APIKEY'])
        self.sender = config.SENDGRID['SENDER']
        self.receiver = config.SENDGRID['RECEIVER']

    def send(self, error, traceback):
        if all((self.sg, self.sender, self.receiver)):
            sender = mail.Email(self.sender)
            to = mail.Email(self.receiver)
            subject = f'Worker: {error}'
            content = mail.Content("text/plain", traceback)
            email = mail.Mail(sender, subject, to, content)
            response = self.post(email.get())
            if response.status_code == 200:
                self.log.info(f'Sent email alert to {self.receiver}')
            else:
                self.log.error(f'Error sending email: {response.status_code}')

    def post(self, body):
        return self.sg.client.mail.send.post(request_body=body)


sentry_handler = SentryHandler(config.SENTRY)
sentry_handler.setLevel(logging.ERROR)
setup_logging(sentry_handler)
