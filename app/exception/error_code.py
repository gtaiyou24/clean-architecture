from __future__ import annotations

from enum import Enum

from http import HTTPStatus

from slf4py import set_logger


@set_logger
class ErrorLevel(Enum):
    WARN = 'WARN'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'

    def to_logger(self, error_code: ErrorCode, detail: str):
        msg = "[Code] {code} [Message] {message} [Detail] {detail}".format(
            code=error_code.name, message=error_code.message, detail=detail)
        if self == ErrorLevel.WARN:
            self.log.warning(msg)
        elif self == ErrorLevel.ERROR:
            self.log.error(msg)
        elif self == ErrorLevel.CRITICAL:
            self.log.critical(msg)
        else:
            self.log.info(msg)


class ErrorCode(Enum):
    LOGIN_BAD_CREDENTIALS = ('メールアドレスまたはパスワードが間違っています', ErrorLevel.WARN, HTTPStatus.UNAUTHORIZED)
    USER_DOES_NOT_EXISTS = ('該当ユーザーが見つかりません。', ErrorLevel.WARN, HTTPStatus.NOT_FOUND)
    REGISTER_USER_ALREADY_EXISTS = ('該当メールアドレスですでにユーザー登録されています', ErrorLevel.WARN, HTTPStatus.BAD_REQUEST)
    VALID_TOKEN_DOES_NOT_EXISTS = ('トークンが見つからない、もしくはすでに有効期限を過ぎています', ErrorLevel.ERROR, HTTPStatus.BAD_REQUEST)
    COMMON_2001 = ('アクセス拒否', ErrorLevel.WARN, HTTPStatus.FORBIDDEN)
    COMMON_2011 = ('該当ユーザーが見つかりません', ErrorLevel.WARN, HTTPStatus.NOT_FOUND)

    def __init__(self, message: str, error_level: ErrorLevel, http_status: HTTPStatus):
        self.message = message
        self.error_level = error_level
        self.http_status = http_status

    def log(self, detail: str):
        self.error_level.to_logger(self, detail)
