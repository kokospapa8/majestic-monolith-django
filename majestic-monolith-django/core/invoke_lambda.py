import json
import logging

import boto3
from django.conf import settings

logger = logging.getLogger("django.eventlogger")

session = boto3.session.Session()
LAMBDA_CLIENT = session.client("lambda", region_name=settings.AWS_DEFAULT_REGION)


# TODO asyncio call uvloop
def invoke_lambda(function_name, payload):
    try:
        ret = LAMBDA_CLIENT.invoke(
            FunctionName=function_name,
            InvocationType="DryRun" if settings.ENV == "test" else "Event",
            Payload=json.dumps(payload),
        )
        logger.info(
            f"{function_name} invoked. "
            f"payload; {payload}. \n ret: {ret['StatusCode']}"
        )
        return ret
    except Exception as e:
        logger.error(
            f"Lambda {function_name} invoke error with {payload} \n " f"error: {e}"
        )
        return None
