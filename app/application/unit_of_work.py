from __future__ import annotations

import abc


class UnitOfWork(abc.ABC):
    """UnitOfWorkの抽象クラス。

    UnitOfWork の詳細は以下をご確認ください。
    https://bliki-ja.github.io/pofeaa/UnitofWork
    https://learn.microsoft.com/ja-jp/archive/msdn-magazine/2009/june/the-unit-of-work-pattern-and-persistence-ignorance

    UnitOfWork はいくつかの課題を解決します。
    * 最小の DB トランザクション実行, SQL クエリ発行をすることで、パフォーマンス問題を解決する
    * DDD において、ドメインオブジェクトの制御と永続化処理を分離させられる
    * 異なる DB コネクション、異なる Redis コネクション全てを単一の論理的なトランザクションにまとめられる
    """

    @abc.abstractmethod
    def mark(self, instance: object) -> None:
        """UnitOfWorkの追跡対象に追加

        self.mark() に指定されたインスタンスは self.persist() にて、更新するインスタンスか新規作成するインスタンスかどうかの判定に用いる。
        """

    @abc.abstractmethod
    def persist(self, instance: object) -> None:
        """永続化対象としてインスタンスを追跡する"""
        pass

    @abc.abstractmethod
    def delete(self, *instances: object) -> None:
        """削除対象としてインスタンスを追跡する"""
        pass

    @abc.abstractmethod
    def start(self) -> None:
        """トランザクションを開始する"""
        pass

    @abc.abstractmethod
    def flush(self) -> None:
        """永続化処理を途中実行する。

        self.commit() とは異なりトランザクションの完了までは行わない。
        DB から ID が採番される関係上、一度 DB を反映して ID を取得したい場合などに使用する。
        """

    @abc.abstractmethod
    def rollback(self) -> None:
        """ロールバックする"""
        pass

    @abc.abstractmethod
    def commit(self) -> None:
        """トランザクションをコミットする"""
        pass
