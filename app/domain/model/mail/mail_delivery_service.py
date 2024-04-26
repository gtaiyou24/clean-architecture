import abc

from domain.model.mail import EmailAddress


class MailDeliveryService(abc.ABC):
    @abc.abstractmethod
    def send(self, to: EmailAddress, subject: str, html: str) -> None:
        pass
