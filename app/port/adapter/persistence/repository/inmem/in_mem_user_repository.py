from __future__ import annotations

from typing import override

from domain.model.mail import EmailAddress
from domain.model.user import UserRepository, User


class InMemUserRepository(UserRepository):
    def __init__(self):
        self.users: set[User] = set()

    @override
    def add(self, user: User) -> None:
        self.users.add(user)

    @override
    def remove(self, user: User) -> None:
        self.users.remove(user)

    @override
    def user_with_email_address(self, email_address: EmailAddress) -> User | None:
        for user in self.users:
            if user.email_address == email_address:
                return user
        return None

    @override
    def user_with_token(self, value: str) -> User | None:
        for user in self.users:
            if user.token_with(value) is not None:
                return user
        return None
