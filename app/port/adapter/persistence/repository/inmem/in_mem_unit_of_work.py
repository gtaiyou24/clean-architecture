from typing import override

from application import UnitOfWork


class InMemUnitOfWork(UnitOfWork):
    @override
    def start(self) -> None:
        pass

    @override
    def rollback(self) -> None:
        pass

    @override
    def commit(self) -> None:
        pass
