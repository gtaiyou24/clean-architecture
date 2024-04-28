from pydantic import BaseModel, Field


class ForgotPasswordRequest(BaseModel):
    email_address: str = Field(title='メールアドレス')
