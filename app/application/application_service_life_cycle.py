from typing import Optional

from injector import singleton, inject

from application import UnitOfWork
from domain.model import DomainEventSubscriber, DomainEvent, DomainEventPublisher


@singleton
class ApplicationServiceLifeCycle:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work = unit_of_work

    def begin(self, is_listening: bool = True) -> None:
        if is_listening:
            self.listen()
        self.__unit_of_work.start()

    def fail(self, exception: Optional[Exception] = None) -> None:
        self.__unit_of_work.rollback()
        if exception is not None:
            raise exception

    def success(self) -> None:
        self.__unit_of_work.commit()

    def listen(self):
        class DomainEventSubscriberImpl(DomainEventSubscriber):
            event_store = []

            def handle_event(self, domain_event: DomainEvent):
                self.event_store.append(domain_event)

            def subscribed_to_event_type(self) -> type:
                # 全てのドメインイベント
                return DomainEvent.__class__

        DomainEventPublisher.shared().reset()
        DomainEventPublisher.shared().subscribe(DomainEventSubscriberImpl[DomainEvent]())