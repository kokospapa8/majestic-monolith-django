import logging

from django.conf import settings
from django.contrib.auth import get_user_model

from core.slack_notification import BaseSlackNotification

User = get_user_model()
logger = logging.getLogger("django.eventlogger")


class SlackNotificationUser(BaseSlackNotification):

    ############################################
    # User
    ############################################

    def signup(self, user, fullname):
        context = {}
        context['action'] = "user signup"
        context['data'] = f"uuid: {user.uuid}, fullname:{fullname}, " \
            f"phonenumber:{user.phonenumber_national_str()}"
        self.send_slack("slack/ops_lastmile.slack",
                        context,
                        settings.SLACK_OPS_CHANNEL)

    def deacivated(self, user):
        # ops log slack
        context = {}
        context['action'] = "user deactivated"
        context['data'] = f"uuid: {user.uuid}, " \
            f"username:{user.username}, " \
            f"phonenumber:{user.phonenumber}"
        self.send_slack("slack/ops_log.slack", context,
                        settings.SLACK_OPS_CHANNEL)

    def banned(self, user):
        # ops log slack
        context = {}
        context['action'] = "user banned"
        context['data'] = f"uuid: {user.uuid}, " \
            f"username:{user.username}, " \
            f"phonenumber:{user.phonenumber}"
        self.send_slack("slack/ops_log.slack", context,
                        settings.SLACK_OPS_CHANNEL)

