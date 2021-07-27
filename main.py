import os
import pinboard as pb
import inspect, jinja2
from datetime import datetime, timedelta 

import smtplib, ssl
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from utilities import loadenv, getenv, info

if __name__ == '__main__':
    loadenv('.env')

    token = getenv('PINBOARD_API_TOKEN')
    days = int(getenv('PINBOARD_DIGEST_DAYS'))

    smtp_from_name = getenv('PINBOARD_DIGEST_SMTP_FROM_NAME')
    smtp_from_email = getenv('PINBOARD_DIGEST_SMTP_FROM_EMAIL')
    smtp_to = getenv('PINBOARD_DIGEST_SMTP_TO')
    smtp_server = getenv('PINBOARD_DIGEST_SMTP_SERVER')
    smtp_port = getenv('PINBOARD_DIGEST_SMTP_PORT')
    smtp_login = getenv('PINBOARD_DIGEST_SMTP_LOGIN')
    smtp_password = getenv('PINBOARD_DIGEST_SMTP_PASSWORD')

    pinboard = pb.Pinboard(token)
    fromdt = datetime.today() - timedelta(days=days)
    bookmarks = pinboard.posts.all(fromdt=fromdt)

    if len(bookmarks) <= 0:
        info('No bookmarks for the given time period. Nothing will be sent.')
        exit(0)

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
