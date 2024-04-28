from pydantic import BaseModel, Field


class RegisterUserRequest(BaseModel):
    email_address: str = Field(title='メールアドレス')
    password: str = Field(title='パスワード')
