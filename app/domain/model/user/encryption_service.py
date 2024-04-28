import abc


class EncryptionService(abc.ABC):
    @abc.abstractmethod
    def encrypt(self, plain_value: str) -> str:
        """値を暗号化する"""
        pass

    @abc.abstractmethod
    def verify(self, plain_value: str, encrypted_value: str) -> bool:
        """プレーンな値と暗号化された値が同じか確認する"""
        pass
