from injector import inject
from sqlalchemy.orm import Query

from application import UnitOfWork
from domain.model.mail import EmailAddress
from domain.model.user import User
from port.adapter.persistence.repository.mysql import MySQLUnitOfWork
from port.adapter.persistence.repository.mysql.user.driver import UsersTableRow, TokensTableRow


class DriverManagerUser:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work: MySQLUnitOfWork = unit_of_work

    def find_by_email_address(self, email_address: EmailAddress) -> User | None:
        query: Query[type[UsersTableRow]] = self.__unit_of_work.session().query(UsersTableRow)
        optional: UsersTableRow | None = query.filter_by(email_address=email_address.value, deleted=False).one_or_none()
        return optional.to_entity() if optional else None

    def find_by_token(self, value: str) -> User | None:
        query: Query[type[TokensTableRow]] = self.__unit_of_work.session().query(TokensTableRow)
        optional: TokensTableRow | None = query.filter_by(value=value, deleted=False).one_or_none()
        return optional.user.to_entity() if optional else None

    def upsert(self, user: User) -> None:
        query: Query[type[UsersTableRow]] = self.__unit_of_work.session().query(UsersTableRow)
        exists = query.filter_by(id=user.id.value).exists()
        if self.__unit_of_work.session().query(exists).scalar():
            self.update(user)
        else:
            self.insert(user)

    def insert(self, user: User) -> None:
        self.__unit_of_work.persist(UsersTableRow.create(user))

    def update(self, user: User) -> None:
        optional: UsersTableRow | None = self.__unit_of_work.session().query(UsersTableRow).get(user.id.value)
        if optional is None:
            raise Exception(f'{UsersTableRow.__tablename__}.{user.id.value} が存在しないため、更新できません。')

        self.__unit_of_work.delete(*optional.tokens)
        self.__unit_of_work.flush()

        optional.update(user)

    def delete(self, user: User) -> None:
        optional: UsersTableRow | None = self.__unit_of_work.session().query(UsersTableRow).get(user.id.value)
        if optional is None:
            return None

        self.__unit_of_work.delete(*optional.tokens)
        self.__unit_of_work.flush()

        optional.deleted = True
