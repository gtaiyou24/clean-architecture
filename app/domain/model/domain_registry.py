from typing import Type

from di import DIContainer
from injector import T


class DomainRegistry:
    @staticmethod
    def resolve(interface: Type[T]) -> T:
        return DIContainer.instance().resolve(interface)
