from __future__ import annotations

import abc


class UnitOfWork(abc.ABC):
    @abc.abstractmethod
    def start(self) -> None:
        """トランザクションを開始する"""
        pass

    @abc.abstractmethod
    def rollback(self) -> None:
        """ロールバックする"""
        pass

    @abc.abstractmethod
    def commit(self) -> None:
        """トランザクションをコミットする"""
        pass
