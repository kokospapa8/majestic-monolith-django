import aws_cdk as cdk
import aws_cdk.aws_logs as logs
from constructs import Construct


class CloudWatchLogsStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]

        # Create Xray Logs
        xray_cloudwatch_logs = logs.CfnLogGroup(
            self, f"mmd-{infra_env}-xray-logs", log_group_name="/mmd/xray"
        )

        # Create Nginx Logs
        nginx_cloudwatch_logs = logs.CfnLogGroup(
            self, f"mmd-{infra_env}-nginx-logs", log_group_name="/ecs/mmd-nginx"
        )

        # Create API Logs
        api_cloudwatch_logs = logs.CfnLogGroup(
            self, f"mmd-{infra_env}-api-logs", log_group_name="/ecs/mmd-api"
        )

        # Create MmdNotificationSlack Logs
        lambda_mmd_noti_slack_logs = logs.LogGroup(
            self,
            f"mmd-{infra_env}-lambda-mmdnotislack",
            log_group_name="/aws/lambda/MmdNotificationSlack",
        )
