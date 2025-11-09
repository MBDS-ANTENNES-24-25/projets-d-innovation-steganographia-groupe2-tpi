import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.core.config import settings


def send_mail(to_emails: list[str], subject: str, body: str, html: bool = True):
    msg = MIMEMultipart()
    if hasattr(settings, "SMTP_FROM_NAME") and settings.SMTP_FROM_NAME:
        msg['From'] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_USER}>"
    else:
        msg['From'] = settings.SMTP_USER
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    if html:
        msg.attach(MIMEText(body, 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
