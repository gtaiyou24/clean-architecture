from domain.model.mail import EmailAddress
from port.adapter.service.mail.adapter import MailDeliveryAdapter


class SendGridAdapter(MailDeliveryAdapter):
    """https://sendgrid.kke.co.jp/"""
    def send(self, to: EmailAddress, subject: str, message: str) -> None:
        raise NotImplementedError()
