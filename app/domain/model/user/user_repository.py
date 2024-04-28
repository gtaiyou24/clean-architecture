from __future__ import annotations

import abc

from domain.model.mail import EmailAddress
from domain.model.user import User


class UserRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, user: User) -> None:
        pass

    @abc.abstractmethod
    def user_with_email_address(self, email_address: EmailAddress) -> User | None:
        pass

    @abc.abstractmethod
    def user_with_token(self, value: str) -> User | None:
        pass
