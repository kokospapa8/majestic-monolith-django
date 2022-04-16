import logging

from core.events import BaseEventsEmitter
logger = logging.getLogger("django.eventlogger")


class AuthEventsEmitter(BaseEventsEmitter):
    SOURCE = "mmd.api.auth"
    DIRECT_NOTIFICATION = True

    def send_verification_code(self, token, phonenumber):
        kwargs = {
            "event_name": "verification_attempt",
            "params": {
                "token": token,
                "phonenumber": phonenumber
            }
        }
        self.emit_eventbridge(**kwargs)
