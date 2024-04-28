from pydantic import BaseModel, Field


class ResetPasswordRequest(BaseModel):
    token: str = Field(title="パスワードリセットトークン")
    password: str = Field(title="パスワード")
