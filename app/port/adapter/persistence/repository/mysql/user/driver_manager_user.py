from injector import inject

from application import UnitOfWork
from port.adapter.persistence.repository.mysql import MySQLUnitOfWork


class DriverManagerUser:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work: MySQLUnitOfWork = unit_of_work
