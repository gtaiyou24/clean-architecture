from __future__ import annotations

from injector import singleton, inject

from domain.model.mail import EmailAddress
from domain.model.user import User
from port.adapter.persistence.repository.mysql.user import DriverManagerUser


@singleton
class CacheLayerUser:
    """キャッシュを保持するクラス"""
    values = dict()

    # 60秒 × 15分
    __TTL = 60 * 15

    @inject
    def __init__(self, driver_manager_user: DriverManagerUser):
        self.__driver_manager_user = driver_manager_user

    def user_or_origin(self, email_address: EmailAddress) -> User | None:
        key = f'email_address-{email_address.value}'
        if key in self.values.keys():
            return self.values[key]

        optional = self.__driver_manager_user.find_by_email_address(email_address)
        self.values[key] = optional
        return self.values[key]

    def user_or_origin_with_token(self, token: str) -> User | None:
        key = f'token-{token}'
        if key in self.values.keys():
            return self.values[key]

        optional = self.__driver_manager_user.find_by_token(token)
        self.values[key] = optional
        return self.values[key]

    def set(self, user: User) -> None:
        self.__driver_manager_user.upsert(user)
        # キャッシュを更新する
        self.values[f'email_address-{user.email_address.value}'] = user
        for token in user.tokens:
            self.values[f'token-{token.value}'] = user

    def delete(self, user: User) -> None:
        self.__driver_manager_user.delete(user)
        # キャッシュを更新する
        self.values[f'email_address-{user.email_address.value}'] = None
        for token in user.tokens:
            self.values[f'token-{token.value}'] = None
