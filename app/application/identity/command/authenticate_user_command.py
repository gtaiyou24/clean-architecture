from __future__ import annotations

import enum
from dataclasses import dataclass


@dataclass(init=True, unsafe_hash=True, frozen=True)
class AuthenticateUserCommand:
    class Provider(enum.Enum):
        EMAIL = lambda email_address, password: AuthenticateUserCommand(email_address, password)
        GITHUB = lambda email_address: AuthenticateUserCommand(email_address, None)
        GOOGLE = lambda email_address: AuthenticateUserCommand(email_address, None)

    email_address: str
    password: str | None

    @staticmethod
    def email(email_address: str, password: str) -> AuthenticateUserCommand:
        return AuthenticateUserCommand.Provider.EMAIL(email_address=email_address, password=password)

    @staticmethod
    def github(user: dict, emails: list[dict]) -> AuthenticateUserCommand:
        default_email = user['email'] or emails[0]['email']
        primary_email = None
        for e in emails:
            if e['primary']:
                primary_email = e['email']
        return AuthenticateUserCommand.Provider.GITHUB(email_address=primary_email or default_email)
