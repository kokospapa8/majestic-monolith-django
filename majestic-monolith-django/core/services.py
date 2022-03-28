import abc

from typing import Any

from django.db import transaction

'''
DomainService: services used within same module
ApplicationService: cross module services (uses uow for aotmic transaction)

'''

# https://www.cosmicpython.com/book/appendix_django.html


class AbstractUnitOfWork(abc.ABC):
    # Abstract repository
    repository: None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class DjangoUnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        # self.repository = repository.DjangoRepository()
        transaction.set_autocommit(False)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        transaction.set_autocommit(True)

    def commit(self):
        transaction.commit()

    def rollback(self):
        transaction.rollback()


class Service:
    def __init__(self, dto: Any = None):
        self.dto = dto


class DomainService(Service):
    pass


class ApplicationService(Service):
    def __init__(self, dto: Any = None, uow: Any = None):
        super().__init__()
        self.dto = dto
        self.uow = uow

    def sample_service_method(self):
        dto = self.dto
        uow = self.uow
        with uow:
            pass  # do something()
            uow.commit()
