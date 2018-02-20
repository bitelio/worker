from contextlib import contextmanager
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers import mail

from . import env


@contextmanager
def lock(name: str, *args, **kwargs):
    lock = env.cache.lock(name, *args, **kwargs)
    if lock.acquire():
        try:
            yield
        finally:
            lock.release()
    else:
        print(f"Couldn't acquire lock '{name}'")
        exit(1)


# def alert(error, traceback):
    # if env.sg:
        # sender = mail.Email(env.sender)
        # to = mail.Email(env.receiver)
        # subject = f"Bitelio: {error}"
        # content = mail.Content("text/plain", traceback)
        # email = mail.Mail(sender, subject, to, content)
        # response = env.sg.client.mail.send.post(request_body=email.get())
        # if response.status_code == 200:
            # env.log.info(f"Sent email alert to {env.receiver}")
        # else:
            # env.log.error(f"Error sending email: {response.status_code}")
