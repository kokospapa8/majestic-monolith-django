# -*- coding: utf-8 -*-
import json
import logging
import platform

from django_log_formatter_ecs import ECSRequestFormatter, ECSSystemFormatter
from django.conf import settings

from urllib.parse import urlparse
from kubi_ecs_logger import Logger
from kubi_ecs_logger.models import Severity

from .log_schema import DaasSchema


class ECSlogger(Logger):
    def __init__(self, *args, **kwargs):
        super(ECSlogger, self).__init__(*args, **kwargs)

    def get_log_dict(self):
        return DaasSchema().dump(self._base)


class MMDECSRequestFormatter(ECSRequestFormatter):
    def _get_event_base(self, extra_labels={}):
        labels = {
            'application': getattr(settings, "DLFE_APP_NAME", None),
            'env': self._get_environment(),
        }

        logger = ECSlogger().event(
            category=self._get_event_category(),
            action=self.record.name,
            message=self.record.getMessage(),
            labels={
                **labels,
                **extra_labels,
            },
        ).host(
            architecture=platform.machine(),
        )

        return logger

    def get_event(self):
        zipkin_headers = getattr(
            settings,
            'DLFE_ZIPKIN_HEADERS',
            ("X-B3-TraceId", "X-B3-SpanId"),
        )

        extra_labels = {}

        for zipkin_header in zipkin_headers:
            if getattr(
                self.record.request.headers, zipkin_header, None,
            ):
                extra_labels[zipkin_header] = self.record.request.headers[zipkin_header]  # noqa E501

        logger_event = self._get_event_base(
            extra_labels=extra_labels,
        )

        parsed_url = urlparse(
            self.record.request.build_absolute_uri()
        )

        ip = self._get_ip_address(self.record.request)

        request_bytes = len(self.record.request.body)
        correlation_id = getattr(self.record, "correlation_id", "-")

        logger_event.url(
            path=parsed_url.path,
            domain=parsed_url.hostname,
        ).source(
            ip=self._get_ip_address(self.record.request)
        ).http_response(
            status_code=getattr(self.record, 'status_code', None)
        ).client(
            address=ip,
            bytes=request_bytes,
            domain=parsed_url.hostname,
            ip=ip,
            port=parsed_url.port,
        ).http_request(
            body_bytes=request_bytes,
            body_content=self.record.request.body,
            method=self.record.request.method,
            correlation_id=correlation_id,

        )

        user_agent_string = getattr(
            self.record.request.headers, 'user_agent', None,
        )

        if not user_agent_string and 'HTTP_USER_AGENT' in self.record.request.META:  # noqa E501
            user_agent_string = self.record.request.META['HTTP_USER_AGENT']

        # Check for use of django-user_agents
        if getattr(self.record.request, 'user_agent', None):
            logger_event.user_agent(
                device={
                    "name": self.record.request.user_agent.device.family,
                },
                name=self.record.request.user_agent.browser.family,
                original=user_agent_string,
                version=self.record.request.user_agent.browser.version_string,
            )
        elif user_agent_string:
            logger_event.user_agent(
                original=user_agent_string,
            )

        if getattr(self.record.request, 'user', None):
            try:
                uuid = self.record.request.user.uuid
            except:
                uuid = None
            if getattr(settings, 'DLFE_LOG_SENSITIVE_USER_DATA', False):
                # Defensively check for full name due to possibility of custom user app
                try:
                    full_name = self.record.request.user.get_full_name()
                except AttributeError:
                    full_name = None

                # Check user attrs to account for custom user apps
                logger_event.user(
                    email=getattr(self.record.request.user, 'email', None),
                    full_name=full_name,
                    name=getattr(self.record.request.user, 'username', None),
                    id=getattr(self.record.request.user, 'id', None),
                    uuid=uuid
                )
            else:
                logger_event.user(
                    id=getattr(self.record.request.user, 'id', None),
                    uuid=uuid,

                )

        return logger_event


class MMDECSFormatter(logging.Formatter):
    def format(self, record):
        if record.name in ECS_FORMATTERS:
            ecs_formatter = ECS_FORMATTERS[record.name]
        else:
            ecs_formatter = ECSSystemFormatter

        formatter = ecs_formatter(record=record)
        logger_event = formatter.get_event()

        logger_event.log(
            level=self._get_severity(record.levelname),
        )

        log_dict = logger_event.get_log_dict()

        return json.dumps(log_dict)

    def _get_severity(self, level):
        if level == "DEBUG":
            return Severity.DEBUG
        elif level == "INFO":
            return Severity.INFO
        elif level == "WARNING":
            return Severity.WARNING
        elif level == "ERROR":
            return Severity.ERROR
        elif level == "CRITICAL":
            return Severity.CRITICAL


ECS_FORMATTERS = {
    "root": ECSSystemFormatter,
    "django.request": MMDECSRequestFormatter,
    "django.db.backends": ECSSystemFormatter,
}
