from __future__ import annotations

from contextlib import contextmanager

from injector import inject
from sqlalchemy import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from application import UnitOfWork


class MySQLUnitOfWork(UnitOfWork):
    @inject
    def __init__(self, engine: Engine):
        self.__engine = engine
        self.__ScopedSession = scoped_session(sessionmaker(bind=self.__engine))
        self.__thread_local_session = None

    @contextmanager
    def query(self) -> Session:
        """
        SELECTクエリを発行する用のセッションを発行する。
        トランザクション管理対象ではないデータの取得にはこのメソッドを利用してください。
        トランザクション管理の対象となるデータ更新・新規作成・削除・更新のためのデータ取得は self.transaction() を利用してください。
        """
        session = Session(bind=self.__engine)
        try:
            yield session
        finally:
            session.close()

    def transaction(self) -> Session:
        """
        トランザクション管理をするためにスレッドローカルのセッションを発行する。
        トランザクション管理の対象となるデータ更新・新規作成・削除・更新のためのデータ取得はこのメソッドを利用してください。
        トランザクション管理対象ではないデータの取得には self.session() を利用するようにしてください。

        :example
        insert: unit_of_work.transaction().add(table_row)
        delete: unit_of_work.transaction().query(HogeTableRow).filter_by(**kwargs).delete()
        update:
            optional = unit_of_work.transaction().query(FugaTableRow).filter_by(id=id).one_or_none()
            if optional is None:
                raise Exception('Not Found')
            optional.column1 = new_column1
            optional.column2 = new_column2
        """
        if self.__thread_local_session is None:
            self.__thread_local_session = self.__ScopedSession()
        return self.__thread_local_session

    def start(self) -> None:
        self.transaction().begin()

    def rollback(self) -> None:
        self.transaction().rollback()
        self.transaction().close()
        self.transaction().bind.dispose()
        self.__thread_local_session = None

    def commit(self) -> None:
        try:
            self.transaction().commit()
            self.transaction().close()
            self.transaction().bind.dispose()
            self.__thread_local_session = None
        except Exception as e:
            self.rollback()
            self.transaction().close()
            self.transaction().bind.dispose()
            raise e
