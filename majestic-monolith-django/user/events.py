import logging

from core.events import BaseEventsEmitter

logger = logging.getLogger("django.eventlogger")


class UserEventsEmitter(BaseEventsEmitter):
    SOURCE = "mmd.api.user"
    DIRECT_NOTIFICATION = True

    def user_signup(self, user_data):
        kwargs = {"event_name": "UserSignup", "params": {"data": user_data}}
        self.emit_eventbridge(**kwargs)

    def user_deactivated(self, user_data):
        kwargs = {"event_name": "UserDeactivated", "params": {"data": user_data}}
        self.emit_eventbridge(**kwargs)

    def user_banned(self, user_data):
        kwargs = {"event_name": "UserBanned", "params": {"data": user_data}}
        self.emit_eventbridge(**kwargs)
