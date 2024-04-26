from __future__ import annotations

import abc
import threading
from datetime import date
from typing import Generic, TypeVar, List

T = TypeVar('T')


class DomainEvent(abc.ABC):
    """ドメインイベント"""

    @abc.abstractmethod
    def event_version(self) -> int:
        pass

    @abc.abstractmethod
    def occurred_on(self) -> date:
        pass


class DomainEventPublisher(threading.Thread):
    """パブリッシャー"""
    instance = threading.local()

    def __init__(self, subscribers: List[DomainEventSubscriber], is_publishing: bool):
        super().__init__()
        self.__subscribers = subscribers
        self.__is_publishing = is_publishing
        self.__instance = DomainEventPublisher.instance

    @staticmethod
    def shared() -> DomainEventPublisher:
        return DomainEventPublisher([], False)

    def reset(self):
        self.__subscribers = []

    def publish(self, domain_event: T):
        if self.__is_publishing or not self.__subscribers:
            return

        try:
            self.__is_publishing = True
            for subscriber in self.__subscribers:
                # サブスクライブするクラスタイプを取得し、型をチェックする
                if isinstance(domain_event, subscriber.subscribed_to_event_type()):
                    subscriber.handle_event(domain_event)
        finally:
            self.__is_publishing = False

    def subscribe(self, subscriber: DomainEventSubscriber):
        self.__subscribers.append(subscriber)


class DomainEventSubscriber(abc.ABC, Generic[T]):
    """サブスクライバー"""
    @abc.abstractmethod
    def handle_event(self, domain_event: T):
        pass

    @abc.abstractmethod
    def subscribed_to_event_type(self) -> type:
        pass
