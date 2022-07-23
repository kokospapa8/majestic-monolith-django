# -*- coding: utf-8 -*-
import copy
from logging import CRITICAL, DEBUG, ERROR, FATAL, INFO, NOTSET, WARNING, Formatter

from django.conf import settings
from django.views.debug import ExceptionReporter
from django_slack.log import SlackExceptionHandler

ERROR_COLOR = "danger"  # color name is built in to Slack API
WARNING_COLOR = "warning"  # color name is built in to Slack API
INFO_COLOR = "#439FE0"

COLORS = {
    CRITICAL: ERROR_COLOR,
    FATAL: ERROR_COLOR,
    ERROR: ERROR_COLOR,
    WARNING: WARNING_COLOR,
    INFO: INFO_COLOR,
    DEBUG: INFO_COLOR,
    NOTSET: INFO_COLOR,
}

DEFAULT_EMOJI = ":heavy_exclamation_mark:"


class NoStacktraceFormatter(Formatter):
    """
    By default the stacktrace will be formatted as part of the message.SlackerLogHandler
    Since we want the stacktrace to be in the attachment of the Slack message,
     we need a custom formatter to leave it out of the message
    """

    def formatException(self, ei):
        return None


class DmmSlackExceptionHandler(SlackExceptionHandler):
    def emit(self, record):
        try:
            request = record.request

            internal = (
                "internal"
                if request.META.get("REMOTE_ADDR") in settings.INTERNAL_IPS
                else "EXTERNAL"
            )

            subject = "[{}]{} ({} IP): {}".format(
                settings.ENV_ALIAS,
                record.levelname,
                internal,
                record.getMessage(),
            )
        except Exception:
            subject = "[{}]{}: {}".format(
                settings.ENV_ALIAS,
                record.levelname,
                record.getMessage(),
            )
            request = None
        subject = self.format_subject(subject)

        # Since we add a nicely formatted traceback on our own, create a copy
        # of the log record without the exception data.
        no_exc_record = copy.copy(record)
        no_exc_record.exc_info = None
        no_exc_record.exc_text = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = ExceptionReporter(request, is_email=True, *exc_info)

        try:
            tb = reporter.get_traceback_text()
        except:
            tb = "(An exception occured when getting the traceback text)"

            if reporter.exc_type:
                tb = "{} (An exception occured when rendering the " "traceback)".format(
                    reporter.exc_type.__name__
                )

        message = "{}\n\n{}".format(self.format(no_exc_record), tb)

        colors = {
            "ERROR": "danger",
            "WARNING": "warning",
            "INFO": "good",
        }

        attachments = {
            "title": subject,
            "text": message,
            "color": colors.get(record.levelname, "#AAAAAA"),
        }

        attachments.update(self.kwargs)
        self.send_message(
            self.template,
            {"text": subject, "channel": settings.SLACK_ERROR_CHANNEL},
            self.generate_attachments(**attachments),
        )
