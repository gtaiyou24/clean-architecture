from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.model import DomainRegistry
from domain.model.mail import EmailAddress
from domain.model.user import Token, EncryptionService, UserId


@dataclass(init=False, eq=False)
class User:
    _id: UserId
    _email_address: EmailAddress
    _encrypted_password: str | None
    _tokens: set[Token]
    _enable: bool
    _verified_at: datetime | None

    def __init__(
        self,
        id: UserId,
        email_address: EmailAddress,
        encrypted_password: str | None,
        tokens: set[Token],
        verified_at: datetime | None,
        enable: bool,
    ):
        """
        :param id:
        :param email_address:
        :param encrypted_password: 暗号化されたパスワード。OAuth2認証で登録されたユーザーは None になる。
        :param tokens:
        :param verified_at:
        :param enable:
        """
        super().__setattr__("_id", id)
        super().__setattr__("_email_address", email_address)
        super().__setattr__("_encrypted_password", encrypted_password)
        super().__setattr__("_tokens", tokens)
        super().__setattr__("_enable", enable)
        super().__setattr__("_verified_at", verified_at)

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.email_address == other.email_address

    def __hash__(self):
        return hash(self.email_address)

    @staticmethod
    def provision(id: UserId, email_address: EmailAddress, plain_password: str | None) -> User:
        """ユーザーを作成する"""
        return User(
            id,
            email_address,
            (
                DomainRegistry.resolve(EncryptionService).encrypt(plain_password)
                if plain_password
                else None
            ),
            set(),
            None,
            False,
        )

    @property
    def id(self) -> UserId:
        return self._id

    @property
    def email_address(self) -> EmailAddress:
        return self._email_address

    @property
    def encrypted_password(self) -> str | None:
        return self._encrypted_password

    @property
    def tokens(self) -> set[Token]:
        return self._tokens

    @property
    def enable(self) -> bool:
        return self._enable

    @property
    def disabled(self) -> bool:
        return self._enable is False

    @property
    def verified_at(self) -> datetime:
        return self._verified_at

    @email_address.setter
    def email_address(self, value: EmailAddress) -> None:
        self._email_address = value

    def verify_password(self, plain_password: str) -> bool:
        if self.encrypted_password is None:
            return False
        return DomainRegistry.resolve(EncryptionService).verify(
            plain_password, self.encrypted_password
        )

    def protect_password(self, plain_password) -> None:
        self._encrypted_password = DomainRegistry.resolve(EncryptionService).encrypt(
            plain_password
        )

    def reset_password(self, new_plain_password: str, reset_token: str) -> None:
        assert self.token_with(reset_token), "パスワードのリセットトークンが不正です。"

        self.protect_password(new_plain_password)
        for token in self.tokens_of(Token.Type.PASSWORD_RESET):
            self._tokens.remove(token)

    def token_with(self, value: str) -> Token | None:
        """トークンの値指定で該当トークンを取得できる"""
        for e in self._tokens:
            if e.value == value:
                return e
        return None

    def latest_token_of(self, type: Token.Type) -> Token | None:
        """最新トークンを取得する"""
        latest_token = None
        for e in self._tokens:
            if not e.is_(type):
                continue

            if latest_token is None or latest_token.expires_at < e.expires_at:
                latest_token = e

        return latest_token

    def tokens_of(self, type: Token.Type) -> set[Token]:
        """トークン名指定で全ての該当トークンを取得できる"""
        return {e for e in self._tokens if e.is_(type)}

    def generate(self, type: Token.Type) -> Token:
        """トークンを発行する"""
        token = type.generate()
        self._tokens.add(token)
        return token

    def login(self) -> None:
        """アクセストークンとリフレッシュトークンを発行してログインする"""
        if not self.is_verified():
            raise PermissionError("ユーザー認証が完了していないため、ログインできません。")
        # 前回のトークンが残っていたら削除する。
        # TODO : 複数のデバイスでログインするユーザーの場合、全てのデバイスのトークンが削除されるが問題ないのか？
        self.logout()
        self.generate(Token.Type.ACCESS)
        self.generate(Token.Type.REFRESH)

    def logout(self) -> None:
        for token in self.tokens_of(Token.Type.ACCESS):
            self._tokens.remove(token)
        for token in self.tokens_of(Token.Type.REFRESH):
            self._tokens.remove(token)

    def verified(self) -> None:
        """ユーザー確認を完了できる"""
        self._enable = True
        self._verified_at = datetime.now()
        for token in self.tokens_of(Token.Type.VERIFICATION):
            self._tokens.remove(token)

    def is_verified(self) -> bool:
        """ユーザー確認が完了されているか判定できる"""
        return self._verified_at is not None
