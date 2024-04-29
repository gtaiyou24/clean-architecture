from __future__ import annotations

from pydantic import BaseModel, Field

from application.identity.dpo import UserDpo


class UserJson(BaseModel):
    id: str = Field(title='id')
    email_address: str = Field(title="メールアドレス")

    @staticmethod
    def from_(dpo: UserDpo) -> UserJson:
        return UserJson(id=dpo.user.id.value, email_address=dpo.user.email_address.value)
