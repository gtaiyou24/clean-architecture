from __future__ import annotations

import abc
import threading
from datetime import datetime
from typing import Self


class DomainEvent(abc.ABC):
    """ドメインイベント"""
    event_version: int
    occurred_on: datetime


class DomainEventPublisher(threading.local):
    """パブリッシャー"""
    __instance: DomainEventPublisher | None = None

    def __init__(self):
        self.__subscribers: set[DomainEventSubscriber] = set()

    @classmethod
    def shared(cls) -> DomainEventPublisher:
        if cls.__instance:
            return cls.__instance

        cls.__instance = DomainEventPublisher()
        return cls.__instance

    def reset(self) -> Self:
        self.__subscribers = set()
        return self

    def publish(self, domain_event: DomainEvent) -> None:
        for subscriber in self.__subscribers:
            # サブスクライブするクラスタイプを取得し、型をチェックする
            if isinstance(domain_event, subscriber.subscribed_to_event_type()):
                subscriber.handle_event(domain_event)

    def subscribe(self, subscriber: DomainEventSubscriber) -> None:
        self.__subscribers.add(subscriber)


class DomainEventSubscriber[T](abc.ABC):
    """サブスクライバー"""

    @abc.abstractmethod
    def handle_event(self, domain_event: T) -> None:
        pass

    def subscribed_to_event_type(self) -> type[T]:
        return T.__class__
