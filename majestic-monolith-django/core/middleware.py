# -*- coding: utf-8 -*-
import sys

from django import VERSION as django_version
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.views.debug import technical_500_response
from request_logging.middleware import LoggingMiddleware

IS_DJANGO_VERSION_GTE_3_2_0 = django_version >= (3, 2, 0, "final", 0)


class HealthCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.META["PATH_INFO"] == "/healthcheck/":
            return HttpResponse({})


# Will be used on production level
class UserBasedExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())


class MMDLoggingMiddleware(LoggingMiddleware):
    def _log_request_headers(self, request, logging_context, log_level):
        if IS_DJANGO_VERSION_GTE_3_2_0:
            headers = {
                k: v if k not in self.sensitive_headers else "*****"
                for k, v in request.headers.items()
            }
        else:
            headers = {
                k: v if k not in self.sensitive_headers else "*****"
                for k, v in request.META.items()
                if k.startswith("HTTP_")
            }

        request_data = {}
        request_data["method"] = getattr(request, "method", "-")
        request_data["path_info"] = getattr(request, "path_info", "-")
        user = getattr(request, "user", None)
        if user and not user.is_anonymous:
            request_data["username"] = user.username
            request_data["uuid"] = str(user.uuid)
        else:
            request_data["username"] = "-"
            request_data["uuid"] = "-"

        data = {
            "headers": headers,
            "request": request_data,
        }

        if headers:
            self.logger.log(log_level, data, logging_context)
