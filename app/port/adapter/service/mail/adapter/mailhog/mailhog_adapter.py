import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from html2text import html2text
from injector import inject

from domain.model.mail import EmailAddress
from port.adapter.service.mail.adapter import MailDeliveryAdapter
from settings import AppSettings


class MailHogAdapter(MailDeliveryAdapter):
    @inject
    def __init__(self, settings: AppSettings):
        self.__smtp = smtplib.SMTP(host="mailhog", port=1025)
        self.__from = settings.FROM_MAIL_ADDRESS

    def send(self, to: EmailAddress, subject: str, html: str) -> None:
        mail = MIMEMultipart("alternative")
        mail["Subject"] = subject
        mail["From"] = self.__from
        mail["To"] = to.value

        mail.attach(MIMEText(html2text(html), "plain"))
        mail.attach(MIMEText(html, "html"))

        self.__smtp.sendmail(self.__from, to.value, mail.as_string())
