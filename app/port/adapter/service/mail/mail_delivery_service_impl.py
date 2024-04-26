from injector import inject

from domain.model.mail import MailDeliveryService, EmailAddress
from port.adapter.service.mail.adapter import MailDeliveryAdapter


class MailDeliveryServiceImpl(MailDeliveryService):
    @inject
    def __init__(self, mail_delivery_adapter: MailDeliveryAdapter):
        self.__mail_delivery_adapter = mail_delivery_adapter

    def send(self, to: EmailAddress, subject: str, html: str) -> None:
        self.__mail_delivery_adapter.send(to, subject, html)
