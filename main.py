import os
import inspect, jinja2
from datetime import datetime, timedelta 

import smtplib, ssl
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import pinboard as pb

def load_env(path):
    if os.path.exists(path):
        for line in open(path):
            var = line.strip().split('=')
            if len(var) == 2:
                os.environ[var[0]] = var[1]

if __name__ == '__main__':
    load_env('.env')

    token = os.environ['PINBOARD_API_TOKEN']
    days = int(os.environ['PINBOARD_DIGEST_DAYS'])

    smtp_from_name = os.environ['PINBOARD_DIGEST_SMTP_FROM_NAME']
    smtp_from_email = os.environ['PINBOARD_DIGEST_SMTP_FROM_EMAIL']
    smtp_to = os.environ['PINBOARD_DIGEST_SMTP_TO']
    smtp_server = os.environ['PINBOARD_DIGEST_SMTP_SERVER']
    smtp_port = os.environ['PINBOARD_DIGEST_SMTP_PORT']
    smtp_login = os.environ['PINBOARD_DIGEST_SMTP_LOGIN']
    smtp_password = os.environ['PINBOARD_DIGEST_SMTP_PASSWORD']

    pinboard = pb.Pinboard(token)
    fromdt = datetime.today() - timedelta(days=days)
    bookmarks = pinboard.posts.all(fromdt=fromdt)

    if len(bookmarks) <= 0:
        print('No bookmarks saved during the given time period.')
        print('Pinboard Digest will not be sent.')
        exit()

    if days == 1:
        description = 'today'
    else:
        description = f'the last {days} days'

    subject = f'Pinboard Digest for {description}'
    html = jinja2.Template(inspect.cleandoc("""
    <html>
    <head></head>
    <body>
    {% for bookmark in bookmarks %}
        <a href="{{ bookmark.url }}">{{ bookmark.description }}</a><br>
    {% endfor %}
    </body>
    </html>
    """
    )).render(bookmarks=bookmarks)

    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = str(Header(f'{smtp_from_name} <{smtp_from_email}>'))
    message['To'] = smtp_to
    message.attach(MIMEText(html, 'plain'))
    message.attach(MIMEText(html, 'html'))

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        server.login(smtp_login, smtp_password)
        server.sendmail(smtp_from_email, smtp_to, message.as_string())
