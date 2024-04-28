from __future__ import annotations

from dataclasses import dataclass


@dataclass(init=True, unsafe_hash=True, frozen=True)
class AuthenticateUserCommand:
    email_address: str
    password: str | None

    @staticmethod
    def email(email_address: str, password: str) -> AuthenticateUserCommand:
        return AuthenticateUserCommand(email_address=email_address, password=password)

    @staticmethod
    def github(user: dict, emails: list[dict]) -> AuthenticateUserCommand:
        default_email = user["email"] or emails[0]["email"]
        primary_email = None
        for e in emails:
            if e["primary"]:
                primary_email = e["email"]
        return AuthenticateUserCommand(
            email_address=primary_email or default_email, password=None
        )
