from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Amount:
    """通貨の量"""
    value: Decimal

    def add(self, other: Amount) -> Amount:
        """足す"""
        return Amount(self.value + other.value)

    def sub(self, other: Amount) -> Amount:
        """引く"""
        return Amount(self.value - other.value)
