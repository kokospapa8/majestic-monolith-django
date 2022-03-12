from typing import Any

'''
DomainService: services used within same module
ApplicationService: cross module services

'''

class Service:
    def __init__(self, dto: Any = None):
        self.dto = dto


class DomainService(Service):
    def __init__(self, dto: Any = None):
        self.dto = dto


class ApplicationService(Service):
    def __init__(self, dto: Any = None):
        self.dto = dto
