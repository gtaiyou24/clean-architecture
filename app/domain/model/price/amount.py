from dataclasses import dataclass
from decimal import Decimal
from typing import Self


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Amount:
    """通貨の量"""

    value: Decimal

    def add(self, other: Self) -> Self:
        """足す"""
        return Amount(self.value + other.value)

    def sub(self, other: Self) -> Self:
        """引く"""
        return Amount(self.value - other.value)
