from __future__ import annotations

import abc
import uuid

from domain.model.mail import EmailAddress
from domain.model.user import User, UserId


class UserRepository(abc.ABC):
    def next_identity(self) -> UserId:
        return UserId(str(uuid.uuid4()))

    @abc.abstractmethod
    def add(self, user: User) -> None:
        pass

    @abc.abstractmethod
    def user_with_email_address(self, email_address: EmailAddress) -> User | None:
        pass

    @abc.abstractmethod
    def user_with_token(self, value: str) -> User | None:
        pass
