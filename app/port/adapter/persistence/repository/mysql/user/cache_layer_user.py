from __future__ import annotations

from cachetools import TTLCache, cached
from injector import singleton, inject

from domain.model.mail import EmailAddress
from domain.model.user import User
from port.adapter.persistence.repository.mysql.user import DriverManagerUser


@singleton
class CacheLayerUser:
    """キャッシュを保持するクラス"""
    # 60秒 × 15分
    __TTL = 60 * 15

    @inject
    def __init__(self, driver_manager_user: DriverManagerUser):
        self.__driver_manager_user = driver_manager_user

    @cached(cache=TTLCache(maxsize=128, ttl=__TTL))
    def user_or_origin(self, email_address: EmailAddress) -> User | None:
        return self.__driver_manager_user.find_by_email_address(email_address)

    @cached(cache=TTLCache(maxsize=128, ttl=__TTL))
    def user_or_origin_with_token(self, token: str) -> User | None:
        return self.__driver_manager_user.find_by_token(token)

    def set(self, user: User) -> None:
        pass
