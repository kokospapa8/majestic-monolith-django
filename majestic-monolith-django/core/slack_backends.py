import boto3
import json

from django.conf import settings
from django_slack.utils import Backend

from core.invoke_lambda import invoke_lambda


class LambdaBackend(Backend):

    def send(self, url, message_data, **kwargs):

        payload = {
            "env": settings.ENV_ALIAS,
            "url": url,
            "message_data": message_data
        }
        ret = invoke_lambda(settings.LAMBDA_FUNCTION_NAMES['NotificationSlack'],
                            payload)


'''
successful response
{'ResponseMetadata': {'RequestId': '7379ef19-6606-4412-9ff2-9fb8e68b1195', 'HTTPStatusCode': 202, 'HTTPHeaders': {'date': 'Fri, 16 Apr 2021 16:43:57 GMT', 'content-length': '0', 'connection': 'keep-alive', 'x-amzn-requestid': '7379ef19-6606-4412-9ff2-9fb8e68b1195', 'x-amzn-remapped-content-length': '0', 'x-amzn-trace-id': 'root=1-6079becd-7f92c63566a47a235a9536a3;sampled=0'}, 'RetryAttempts': 0}, 'StatusCode': 202, 'Payload': <botocore.response.StreamingBody object at 0x1056744d0>}

'''


class EventbridgeBackend(Backend):
    def send(self, url, message_data, **kwargs):
        pass
