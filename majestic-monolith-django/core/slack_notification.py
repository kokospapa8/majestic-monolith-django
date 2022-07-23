import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django_slack import slack_message

User = get_user_model()
logger = logging.getLogger("django.eventlogger")


class BaseSlackNotification:
    def send_slack(self, template, context, channel):
        if settings.ENV in ["stage", "beta"]:
            return
        context["env"] = settings.ENV_ALIAS
        slack_message(template, context, channel=channel)
