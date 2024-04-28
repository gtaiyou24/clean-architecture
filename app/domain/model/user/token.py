from __future__ import annotations

import enum
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(init=True, frozen=True)
class Token:
    """トークン
    このクラスは JWT などのトークンとは違い、ユーザ確認やパスワードリセットのために一時的に発行された値を表す値オブジェクトです。
    """
    class Name(enum.Enum):
        VERIFICATION = ('検証トークン', 30)
        PASSWORD_RESET = ('パスワードリセットトークン', 10)

        def __init__(self, type: str, expiration_minutes: int):
            self.type = type
            self.expiration_minutes = expiration_minutes

        def generate(self) -> Token:
            return Token(self, str(uuid.uuid4()), datetime.utcnow() + timedelta(minutes=self.expiration_minutes))

    name: Name
    value: str
    expires_at: datetime

    def __hash__(self):
        return hash(self.name)

    def is_(self, name: Name) -> bool:
        return self.name == name

    def has_expired(self) -> bool:
        return self.expires_at < datetime.utcnow()
