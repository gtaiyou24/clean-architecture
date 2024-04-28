from __future__ import annotations

from datetime import timedelta, datetime

from pydantic import BaseModel, Field

from application.identity.dpo import UserDpo
from port.adapter.resource.jwt import JWTEncoder


class Token(BaseModel):
    access_token: str = Field(title="アクセストークン")
    refresh_token: str = Field(title="リフレッシュトークン")
    token_type: str = Field(title="トークンタイプ", default="bearer")
    expires_at: float = Field(title="アクセストークンの有効期間タイムスタンプ")

    @staticmethod
    def generate(dpo: UserDpo) -> Token:
        now = datetime.now()
        expires_at = now + timedelta(hours=1)
        access_token = JWTEncoder.encode(
            {"sub": dpo.user.email_address.value, "exp": expires_at}
        )
        refresh_token = JWTEncoder.encode(
            {"sub": dpo.user.email_address.value, "exp": now + timedelta(days=7)}
        )
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_at=expires_at.timestamp(),
        )
