from __future__ import annotations

from dataclasses import dataclass

from application.identity.dpo import UserDpo


@dataclass(init=True, unsafe_hash=True, frozen=True)
class RevokeCommand:
    email_address: str

    @staticmethod
    def from_(dpo: UserDpo) -> RevokeCommand:
        return RevokeCommand(dpo.user.email_address.value)
