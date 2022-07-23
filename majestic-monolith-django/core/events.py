import json
import logging

import boto3
from botocore.exceptions import ClientError
from django.conf import settings

logger = logging.getLogger("django.eventlogger")
events = boto3.client("events")


class BaseEventsEmitter:
    SOURCE = None
    EVENT_BUS = None
    TARGET = ["eventbridge"]

    def __init__(self):
        self.EVENT_BUS = settings.EVENT_BUS_PUSHOPS

    def emit(self, **kwargs):
        pass

    def emit_eventbridge(self, event_name, params):
        if settings.ENV in ["test", "local"]:
            logger.info(f"eventbridge mock: {event_name} - {params} ")
            return
        try:
            put_events = events.put_events(
                Entries=[
                    {
                        "Source": self.SOURCE,
                        "DetailType": event_name,
                        "Detail": json.dumps({"params": params}),
                        "EventBusName": settings.EVENT_BUS_PUSHOPS,
                        "Resources": [],
                    },
                ]
            )
            logger.info(f"Event emitted {put_events}")
        except ClientError as e:
            logger.error(f"error sending event error {e}")
            logger.error(f"event_name: {event_name}")
            logger.error(f"bus_name: {self.EVENT_BUS}")
            logger.error(f"params: {params}")


"""

# client
events = boto3.client("events")

# cteate event param_set
event_param_set = {
    "params": {
        "orde_number": "e2e1640093340257",
    }
}

# put_evnets
put_events = events.put_events(
    Entries=[
        {
            "Source": "mmd.api.order",
            "DetailType": "OrderCreated",
            "Detail": json.dumps(event_param_set),
            "EventBusName": "mmd-stage-events-pushops",
            "Resources": [],
        },
    ]
)
"""
