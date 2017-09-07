import sendgrid

from . import config


class SendGrid:
    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(apikey=config.SENDGRID['APIKEY'])
        self.sender = config.SENDGRID['SENDER']
        self.receiver = config.SENDGRID['RECEIVER']

    def send(self, error, traceback):
        if all((self.client, self.sender, self.receiver)):
            sender = sendgrid.helpers.mail.Email(self.sender)
            to = sendgrid.helpers.mail.Email(self.receiver)
            subject = f'Worker: {error}'
            content = Content("text/plain", traceback)
            mail = sendgrid.helpers.mail.Mail(sender, subject, to, content)
            response = self.sg.client.mail.send.post(request_body=mail.get())
            if response.status_code == 200:
                log.info(f'Sent email alert to {receiver}')
            else:
                log.error(f'Error sending email: {response.status_code}')
