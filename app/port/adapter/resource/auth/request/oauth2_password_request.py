from pydantic import BaseModel, Field


class OAuth2PasswordRequest(BaseModel):
    email_address: str = Field(title="メールアドレス")
    password: str = Field(title="パスワード")
