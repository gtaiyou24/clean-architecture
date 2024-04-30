from typing import override

from application import UnitOfWork


class InMemUnitOfWork(UnitOfWork):
    @override
    def mark(self, instance: object) -> None:
        pass

    @override
    def persist(self, instance: object) -> None:
        pass

    @override
    def delete(self, *instances: object) -> None:
        pass

    @override
    def start(self) -> None:
        pass

    @override
    def flush(self) -> None:
        pass

    @override
    def rollback(self) -> None:
        pass

    @override
    def commit(self) -> None:
        pass
