import json
import logging

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django_slack.utils import Backend

from core.invoke_lambda import invoke_lambda

logger = logging.getLogger("django.eventlogger")
events = boto3.client("events")


class LambdaBackend(Backend):
    def send(self, url, message_data, **kwargs):

        payload = {"env": settings.ENV_ALIAS, "url": url, "message_data": message_data}
        ret = invoke_lambda(  # noqa: F841
            settings.LAMBDA_FUNCTION_NAMES["NotificationSlack"], payload
        )


"""
successful response
{'ResponseMetadata': {'RequestId': '7379ef19-6606-4412-9ff2-9fb8e68b1195', 'HTTPStatusCode': 202, 'HTTPHeaders': {'date': 'Fri, 16 Apr 2021 16:43:57 GMT', 'content-length': '0', 'connection': 'keep-alive', 'x-amzn-requestid': '7379ef19-6606-4412-9ff2-9fb8e68b1195', 'x-amzn-remapped-content-length': '0', 'x-amzn-trace-id': 'root=1-6079becd-7f92c63566a47a235a9536a3;sampled=0'}, 'RetryAttempts': 0}, 'StatusCode': 202, 'Payload': <botocore.response.StreamingBody object at 0x1056744d0>}

"""


class EventBridgeBackend(Backend):
    SOURCE = "mmd.slack_backend"
    EVENT_BUS = settings.EVENT_BUS_PUSHOPS

    def send(self, url, message_data, **kwargs):

        payload = {"env": settings.ENV_ALIAS, "url": url, "message_data": message_data}
        self.emit_eventbridge("slack", payload)

    def emit_eventbridge(self, event_name, params):
        if settings.ENV == "test":
            return
        try:
            put_events = events.put_events(
                Entries=[
                    {
                        "Source": self.SOURCE,
                        "DetailType": event_name,
                        "Detail": json.dumps({"params": params}),
                        "EventBusName": self.EVENT_BUS,
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
