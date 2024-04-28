import re
from dataclasses import dataclass


@dataclass(init=False, unsafe_hash=True, eq=True, frozen=True)
class EmailAddress:
    value: str

    def __init__(self, value: str):
        assert value, "メールアドレスは必須です。"
        assert (
            0 < len(value) <= 100
        ), "メールアドレスは100文字以下である必要があります。"
        assert re.match(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value
        ), "メールアドレスが不正です。"

        super().__setattr__("value", value)

    def __str__(self):
        return self.value

    @property
    def domain(self) -> str:
        return self.value.split("@")[1]
