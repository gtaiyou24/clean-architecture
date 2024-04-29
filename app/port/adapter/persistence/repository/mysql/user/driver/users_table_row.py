from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, func, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from domain.model.mail import EmailAddress
from domain.model.user import User, UserId
from port.adapter.persistence.repository.mysql import DataBase
from port.adapter.persistence.repository.mysql.user.driver import TokensTableRow


class UsersTableRow(DataBase):
    __tablename__ = "users"
    __table_args__ = ({"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"})

    id: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False)
    email_address: Mapped[str] = mapped_column(String(255),
                                               unique=True,
                                               nullable=False,
                                               index=True,
                                               comment='メールアドレス')
    password: Mapped[str | None] = mapped_column(String(255),
                                                 nullable=True,
                                                 comment='セキュアなパスワード。OAuth2 でサービス登録している場合は NULL になる。')
    enable: Mapped[bool] = mapped_column(Boolean,
                                         default=False,
                                         nullable=False,
                                         comment='有効化されているかどうか')
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),
                                                         nullable=True,
                                                         comment='本人確認が完了した日時')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now(),
                                                 onupdate=func.now())
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    tokens: Mapped[list[TokensTableRow]] = relationship(
        'TokensTableRow',
        primaryjoin='UsersTableRow.id == TokensTableRow.user_id',
        lazy='joined',  # NOTE: SELECT 時に JOIN させる
        foreign_keys='TokensTableRow.user_id'
    )

    @staticmethod
    def create(user: User) -> UsersTableRow:
        return UsersTableRow(
            id=user.id.value,
            email_address=user.email_address.value,
            password=user.encrypted_password,
            enable=user.enable,
            verified_at=user.verified_at,
            tokens=[tr for tr in TokensTableRow.create(user)]
        )

    def update(self, user: User) -> None:
        self.email_address = user.email_address.value
        self.password = user.encrypted_password
        self.enable = user.enable
        self.verified_at = user.verified_at
        self.tokens = TokensTableRow.create(user)

    def to_entity(self) -> User:
        return User(
            id=UserId(self.id),
            email_address=EmailAddress(self.email_address),
            encrypted_password=self.password,
            tokens=set([tr.to_value() for tr in self.tokens]),
            verified_at=self.verified_at,
            enable=self.enable
        )
