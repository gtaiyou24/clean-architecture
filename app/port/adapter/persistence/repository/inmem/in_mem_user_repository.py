from __future__ import annotations

from domain.model.user import UserRepository, User, EmailAddress


class InMemUserRepository(UserRepository):
    def __init__(self):
        self.users: set[User] = set()

    def add(self, user: User) -> None:
        self.users.add(user)

    def user_with_email_address(self, email_address: EmailAddress) -> User | None:
        for user in self.users:
            if user.email_address == email_address:
                return user
        return None

    def user_with_token(self, value: str) -> User | None:
        for user in self.users:
            if user.token_with(value) is not None:
                return user
        return None
