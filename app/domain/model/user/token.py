from __future__ import annotations

import datetime
import enum
import uuid
from dataclasses import dataclass


@dataclass(init=True, frozen=True)
class Token:
    """トークン
    このクラスは JWT などのトークンとは違い、ユーザ確認やパスワードリセットのために一時的に発行された値を表す値オブジェクトです。
    """

    class Type(enum.Enum):
        VERIFICATION = ("検証トークン", 30)
        PASSWORD_RESET = ("パスワードリセットトークン", 10)

        def __init__(self, ja: str, expiration_minutes: int):
            self.ja = ja
            self.expiration_minutes = expiration_minutes

        def generate(self) -> Token:
            return Token(
                self,
                str(uuid.uuid4()),
                datetime.datetime.now() + datetime.timedelta(minutes=self.expiration_minutes),
            )

    type: Type
    value: str
    expires_at: datetime.datetime

    def __hash__(self):
        return hash(self.type)

    def is_(self, type: Type) -> bool:
        return self.type == type

    def has_expired(self) -> bool:
        return self.expires_at < datetime.datetime.now()
