from sqlalchemy.orm import declarative_base

# TODO : use sqlalchemy.orm.DeclarativeBase
#        see https://docs.sqlalchemy.org/en/20/orm/quickstart.html
DataBase = declarative_base()

from .enum_type import EnumType
from .mysql_unit_of_work import MySQLUnitOfWork
