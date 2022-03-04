# -*- coding: utf-8 -*-
from rest_framework.exceptions import _get_error_details
from rest_framework.exceptions import APIException


class CacheGetException(Exception):
    pass


class ModelTableNameUndefinedException(Exception):
    pass


class AppNotFoundError(Exception):
    pass


class ClassNotFoundError(Exception):
    pass


# Used in Data Migrations
class MapException(Exception):
    pass


class JoinMapException(Exception):
    pass


class HttpRedirectException(Exception):
    pass


class MMTSMSException(Exception):
    pass


class NotFoundException(APIException):
    status_code = 404
    default_detail = "Requested resource was not found."


class ParamNotGivenException(APIException):
    status_code = 400
    default_detail = "Required informations are not given."


class ConflictException(APIException):
    status_code = 409
    default_detail = "This response is sent when a request conflicts with the current state of the server"
    default_code = 'conflict'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'
