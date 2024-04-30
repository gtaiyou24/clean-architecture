from domain.model.mail import EmailAddress
from port.adapter.service.mail.adapter import MailDeliveryAdapter


class MailDeliveryAdapterStub(MailDeliveryAdapter):
    def send(self, to: EmailAddress, subject: str, message: str) -> None:
        print(f'send "{subject}" to {to.value}')
