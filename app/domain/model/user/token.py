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
        ACCESS = ("アクセストークン", 60)
        REFRESH = ("リフレッシュトークン", 60 * 24 * 7)

        def __init__(self, ja: str, expiration_minutes: int):
            self.ja = ja
            self.expiration_minutes = expiration_minutes

        def generate(self) -> Token:
            """トークンを生成します。
            このメソッドでは、各トークンの生成ロジックを記述しています。
            今後トークンの生成ロジックが複雑になってきたら、ファクトリクラスなどに切り出すこと。
            """
            expires_at = datetime.datetime.now() + datetime.timedelta(minutes=self.expiration_minutes)
            return Token(self, str(uuid.uuid4()), expires_at)

    type: Type
    value: str
    expires_at: datetime.datetime

    def is_(self, type: Type) -> bool:
        return self.type == type

    def has_expired(self) -> bool:
        return self.expires_at < datetime.datetime.now()
