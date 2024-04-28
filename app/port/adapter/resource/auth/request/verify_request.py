from pydantic import BaseModel, Field


class VerifyRequest(BaseModel):
    access_token: str = Field(title='アクセストークン')
