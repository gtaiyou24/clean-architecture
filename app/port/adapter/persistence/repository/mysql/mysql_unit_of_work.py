from typing import override

from injector import inject
from sqlalchemy import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from application import UnitOfWork


class MySQLUnitOfWork(UnitOfWork):
    @inject
    def __init__(self, engine: Engine):
        self.__engine = engine
        self.__ThreadLocalSession = scoped_session(sessionmaker(bind=self.__engine))

    def session(self) -> Session:
        """トランザクション管理をするためにスレッドローカルのセッションを発行する"""
        return self.__ThreadLocalSession()

    @override
    def mark(self, instance: object) -> None:
        """UnitOfWorkの追跡対象に追加

        self.mark() に指定されたインスタンスは self.persist() にて、更新するインスタンスか新規作成するインスタンスかどうかの判定に用いる。
        """
        pass

    @override
    def persist(self, instance: object) -> None:
        """永続化対象としてインスタンスを追跡する"""
        # NOTE : INSERT もしくは UPDATE されるオブジェクトを指定
        self.session().add(instance)

    @override
    def delete(self, *instances: object) -> None:
        """削除対象としてオブジェクトを追跡する"""
        for instance in instances:
            self.session().delete(instance)

    @override
    def start(self) -> None:
        self.session().begin()

    @override
    def flush(self) -> None:
        self.session().flush()

    @override
    def rollback(self) -> None:
        self.session().rollback()
        self.__ThreadLocalSession.remove()

    @override
    def commit(self) -> None:
        self.session().commit()
        self.__ThreadLocalSession.remove()
