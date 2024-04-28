from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from domain.model.price import Amount


class Currency(Enum):
    """通貨"""

    YEN = "円"
    DOLLAR = "ドル"

    def of(self, amount: str) -> Price:
        return Price(Amount(Decimal(amount)), self)


@dataclass(init=True, frozen=True, unsafe_hash=True)
class Price:
    """値オブジェクト「価格」"""

    amount: Amount
    currency: Currency

    def add(self, other: Price) -> Price:
        return Price(self.amount.add(other.amount), self.currency)

    def sub(self, other: Price) -> Price:
        return Price(self.amount.sub(other.amount), self.currency)
