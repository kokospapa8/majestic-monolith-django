import logging

from django.conf import settings


class RequireTestingFalse(logging.Filter):
    def filter(self, record):
        return not settings.TESTING


class RequireTestingTrue(logging.Filter):
    def filter(self, record):
        return settings.TESTING


class RequireLocalTrue(logging.Filter):
    def filter(self, record):
        return settings.ENV in ["local", "test"]


class RequireLocalFalse(logging.Filter):
    def filter(self, record):
        return settings.ENV not in ["local", "test"]


class RequireDevTrue(logging.Filter):
    def filter(self, record):
        return settings.ENV in ["dev", "stage"]


class RequireDevFalse(logging.Filter):
    def filter(self, record):
        return settings.ENV not in ["dev", "stage"]


class RequireBetaTrue(logging.Filter):
    def filter(self, record):
        return settings.ENV == "beta"


class RequireProdTrue(logging.Filter):
    def filter(self, record):
        return settings.ENV == "prod"


class BetaProdFilter(logging.Filter):
    def filter(self, record):
        return settings.ENV in ["beta", "prod"]


class SkipLoggingPath(logging.Filter):
    def filter(self, record):
        # print(record)
        # print(dir(record.request))
        # print(record.request.path)
        if not hasattr(record, "request"):
            return True
        if record.request.path in settings.SKIP_LOGGING_PATH:
            return False
        return True
