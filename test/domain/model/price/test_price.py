from decimal import Decimal

import pytest

from domain.model.price import Price, Amount, Currency


class TestPrice:
    class Test_生成について:
        def test_通貨量と通貨タイプ指定で生成できる(self):
            try:
                Price(Amount(Decimal('100')), Currency.YEN)
            except Exception as e:
                pytest.fail(e)
