from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.model import DomainRegistry
from domain.model.mail import EmailAddress
from domain.model.user import Token, EncryptionService


@dataclass(init=False, eq=False)
class User:
    _email_address: EmailAddress
    _encrypted_password: str | None
    _tokens: set[Token]
    _enable: bool
    _verified_at: datetime | None

    def __init__(self,
                 email_address: EmailAddress,
                 encrypted_password: str | None,
                 tokens: set[Token],
                 verified_at: datetime | None,
                 enable: bool):
        """
        :param email_address:
        :param encrypted_password: 暗号化されたパスワード。OAuth2認証で登録されたユーザーは None になる。
        :param tokens:
        :param verified_at:
        :param enable:
        """
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
    def registered(email_address: EmailAddress, plain_password: str | None) -> User:
        return User(
            email_address,
            DomainRegistry.resolve(EncryptionService).encrypt(plain_password) if plain_password else None,
            set(),
            None,
            False
        )

    @property
    def email_address(self) -> EmailAddress:
        return self._email_address

    @property
    def encrypted_password(self) -> str | None:
        return self._encrypted_password

    @property
    def disabled(self) -> bool:
        return self._enable is False

    @email_address.setter
    def email_address(self, value: EmailAddress) -> None:
        self._email_address = value

    def verify_password(self, plain_password: str) -> bool:
        if self.encrypted_password is None:
            return False
        return DomainRegistry.resolve(EncryptionService).verify(plain_password, self.encrypted_password)

    def protect_password(self, plain_password) -> None:
        self._encrypted_password = DomainRegistry.resolve(EncryptionService).encrypt(plain_password)

    def reset_password(self, new_plain_password: str, reset_token: str) -> None:
        assert self.token_with(reset_token), 'パスワードのリセットトークンが不正です。'

        self.protect_password(new_plain_password)
        for token in self.tokens_of(Token.Name.PASSWORD_RESET):
            self._tokens.remove(token)

    def token_with(self, value: str) -> Token | None:
        """トークンの値指定で該当トークンを取得できる"""
        for e in self._tokens:
            if e.value == value:
                return e
        return None

    def tokens_of(self, name: Token.Name) -> set[Token]:
        """トークン名指定で全ての該当トークンを取得できる"""
        return {e for e in self._tokens if e.is_(name)}

    def generate_verification_token(self) -> Token:
        """ユーザー確認トークンを発行する"""
        token = Token.Name.VERIFICATION.generate()
        self._tokens.add(token)
        return token

    def generate_password_reset_token(self) -> Token:
        """パスワードリセットトークンを発行する"""
        token = Token.Name.PASSWORD_RESET.generate()
        self._tokens.add(token)
        return token

    def verified(self) -> None:
        """ユーザー確認を完了できる"""
        self._enable = True
        self._verified_at = datetime.now()
        for token in self.tokens_of(Token.Name.VERIFICATION):
            self._tokens.remove(token)

    def is_verified(self) -> bool:
        """ユーザー確認が完了されているか判定できる"""
        return self._verified_at is not None
