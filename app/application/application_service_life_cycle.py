from __future__ import annotations

from functools import wraps
from typing import override, Callable

from di import DIContainer
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


def transactional[T](method: Callable[..., T], is_listening: bool = True):
    """AOPによるトランザクション管理を行うためのデコーダー"""
    @wraps(method)
    def handle_transaction(*args, **kwargs) -> T:
        application_life_cycle = DIContainer.instance().resolve(ApplicationServiceLifeCycle)

        application_life_cycle.begin(is_listening)
        try:
            _return = method(*args, **kwargs)
            application_life_cycle.success()
            return _return
        except Exception as e:
            application_life_cycle.fail(e)

    return handle_transaction
