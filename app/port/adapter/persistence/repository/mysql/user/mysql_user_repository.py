from __future__ import annotations

from injector import inject
from typing import override

from domain.model.mail import EmailAddress
from domain.model.user import UserRepository, User
from port.adapter.persistence.repository.mysql.user import CacheLayerUser


class MySQLUserRepository(UserRepository):

    @inject
    def __init__(self, cache_layer_user: CacheLayerUser):
        self.__cache_layer_user = cache_layer_user

    @override
    def add(self, user: User) -> None:
        self.__cache_layer_user.set(user)

    @override
    def user_with_email_address(self, email_address: EmailAddress) -> User | None:
        return self.__cache_layer_user.user_or_origin(email_address)

    @override
    def user_with_token(self, value: str) -> User | None:
        return self.__cache_layer_user.user_or_origin_with_token(value)
