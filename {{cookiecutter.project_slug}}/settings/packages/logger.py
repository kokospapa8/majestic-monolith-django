# -*- coding: utf-8 -*-
import logging
import os
from core.log_formatter import MMDECSFormatter

FILE_LOGGER = os.environ.get("FILE_LOGGER", False)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "ecs_formatter": {
            "()": MMDECSFormatter
        },
        'plaintext': {
            'format': '%(levelname)s %(asctime)s [%(correlation_id)s] %(name)s %(message)s'
        }
    },
    "filters": {
        "require_local_false": {
            "()": "core.log_filter.RequireLocalFalse"
        },
        "require_local_true": {
            "()": "core.log_filter.RequireLocalTrue"
        },
        "require_dev_false": {
            "()": "core.log_filter.RequireDevFalse"
        },
        "require_dev_true": {
            "()": "core.log_filter.RequireDevTrue"
        },
        "require_beta_true": {
            "()": "core.log_filter.RequireBetaTrue"
        },
        "require_prod_true": {
            "()": "core.log_filter.RequireProdTrue"
        },
        "require_test_false": {
            "()": "core.log_filter.RequireTestingFalse"
        },
        "require_test_true": {
            "()": "core.log_filter.RequireTestingTrue"
        },
        'correlation_id': {
            '()': 'django_guid.log_filters.CorrelationId'
        },
        'skip_logging_path': {
            '()': 'core.log_filter.SkipLoggingPath'
        }

    },
    "handlers": {
        "null": {
            "class": "logging.NullHandler"
        },

        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "ecs_formatter",
            'filters': ['correlation_id', 'require_local_false', 'skip_logging_path'],

        },
        "console_local": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "plaintext",
            'filters': ['correlation_id', 'require_local_true'],
        },
        "slack_report": {
            "level": "ERROR",
            'class': 'core.log.DmmSlackExceptionHandler',
            'filters': ['require_local_false']
        }

    },

    "loggers": {
        "django.request": {
            "handlers": [
                "console",
                "console_local",
                'slack_report',

            ],
            "propagate": False,
        },
        "django.debuglogger": {
            "handlers": ["console_local"],
            "level": "DEBUG",
            "propagate": False
        },
        "django.eventlogger": {
            "handlers": ["console", "console_local"],
            "level": "INFO",
            "propagate": False
        },
        "django.criticallogger": {
            "handlers": ["console"],
            "level": "CRITICAL",
            "propagate": False
        },

    },
}

# Thid is purely for EKS fargate where we need to collect file log for fluentd
if FILE_LOGGER:
    from pathlib import Path
    p = Path('/var', '/log', '/contaniers')
    p.mkdir(exist_ok=True)

    LOGGING['handlers'].update(
        {
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "formatter": "ecs_formatter",
                "filename": "/var/log/containers/request.log"
            }
        }
    )
    LOGGING['loggers']['django.request']['handlers'] = [
        "console", 'mail_admins', 'slack_report', "file"
    ]

REQUEST_LOGGING_HTTP_4XX_LOG_LEVEL = logging.WARNING

DJANGO_GUID = {
    'GUID_HEADER_NAME': 'Correlation-ID',
    'VALIDATE_GUID': True,
    'RETURN_HEADER': True,
    'EXPOSE_HEADER': True,
    'INTEGRATIONS': [],
    'IGNORE_URLS': ['/api/healthcheck/'],
    'UUID_LENGTH': 32,
}
