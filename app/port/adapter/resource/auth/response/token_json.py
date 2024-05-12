from __future__ import annotations

from pydantic import BaseModel, Field

from application.identity.dpo import UserDpo
from domain.model.user import Token


class TokenJson(BaseModel):
    access_token: str = Field(title="アクセストークン")
    refresh_token: str = Field(title="リフレッシュトークン")
    token_type: str = Field(title="トークンタイプ", default="bearer")
    expires_at: float = Field(title="アクセストークンの有効期間タイムスタンプ")

    @staticmethod
    def generate(dpo: UserDpo) -> TokenJson:
        access_token = dpo.user.latest_token_of(Token.Type.ACCESS)
        refresh_token = dpo.user.latest_token_of(Token.Type.REFRESH)
        if access_token is None or refresh_token is None:
            raise ValueError("アクセストークン、リフレッシュトークンの生成に失敗しました")
        return TokenJson(
            access_token=access_token.value,
            refresh_token=refresh_token.value,
            token_type="bearer",
            expires_at=access_token.expires_at.timestamp(),
        )
