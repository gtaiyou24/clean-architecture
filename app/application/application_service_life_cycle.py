from __future__ import annotations

from typing import override

from injector import singleton, inject

from application import UnitOfWork
from domain.model import DomainEventSubscriber, DomainEvent, DomainEventPublisher


class DomainEventSubscriberImpl(DomainEventSubscriber[DomainEvent]):
    event_store = []

    @override
    def handle_event(self, domain_event: DomainEvent):
        self.event_store.append(domain_event)


@singleton
class ApplicationServiceLifeCycle:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work = unit_of_work

    def begin(self, is_listening: bool = True) -> None:
        if is_listening:
            self.listen()
        self.__unit_of_work.start()

    def fail(self, exception: Exception | None = None) -> None:
        self.__unit_of_work.rollback()
        if exception is not None:
            raise exception

    def success(self) -> None:
        self.__unit_of_work.commit()

    def listen(self):
        DomainEventPublisher.shared().reset()
        DomainEventPublisher.shared().subscribe(DomainEventSubscriberImpl())
