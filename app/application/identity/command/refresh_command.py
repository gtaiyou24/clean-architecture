from __future__ import annotations

from dataclasses import dataclass

from application.identity.dpo import UserDpo


@dataclass(init=True, unsafe_hash=True, frozen=True)
class RefreshCommand:
    email_address: str

    @staticmethod
    def from_(dpo: UserDpo) -> RefreshCommand:
        return RefreshCommand(dpo.user.email_address.value)
