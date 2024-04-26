from application import UnitOfWork


class InMemUnitOfWork(UnitOfWork):
    def start(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def commit(self) -> None:
        pass
