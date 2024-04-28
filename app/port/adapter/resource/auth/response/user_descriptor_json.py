from __future__ import annotations

from pydantic import BaseModel, Field

from application.identity.dpo import UserDpo


class UserDescriptorJson(BaseModel):
    email_address: str = Field(title='メールアドレス')

    @staticmethod
    def from_(dpo: UserDpo) -> UserDescriptorJson:
        return UserDescriptorJson(
            email_address=dpo.user.email_address.address
        )
