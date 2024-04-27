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

    class Test_addメソッドについて:
        def test_価格で加算し計算結果を取得できる(self):
            price = Price(Amount(Decimal('100')), Currency.YEN)
            other = Price(Amount(Decimal('50')), Currency.YEN)

            actual = price.add(other)
            assert actual == Price(Amount(Decimal('150')), Currency.YEN)

    class Test_subメソッドについて:
        def test_価格で減算し計算結果を取得できる(self):
            price = Price(Amount(Decimal('100')), Currency.YEN)
            other = Price(Amount(Decimal('50')), Currency.YEN)

            actual = price.sub(other)
            assert actual == Price(Amount(Decimal('50')), Currency.YEN)


class TestCurrency:
    class Test_ofメソッドについて:
        def test_価格を生成できる(self):
            price = Currency.YEN.of('100')
            assert price == Price(Amount(Decimal('100')), Currency.YEN)
