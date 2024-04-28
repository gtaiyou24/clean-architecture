from __future__ import annotations

from pydantic import BaseModel, Field

from application.identity.dpo import UserDpo


class UserJson(BaseModel):
    email_address: str = Field(title="メールアドレス")

    @staticmethod
    def from_(dpo: UserDpo) -> UserJson:
        return UserJson(email_address=dpo.user.email_address.value)
