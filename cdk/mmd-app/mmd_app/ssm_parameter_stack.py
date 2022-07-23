import aws_cdk as cdk
import aws_cdk.aws_ssm as ssm
from constructs import Construct


class SsmParameterStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get DB Password
        ssm_db_password = ssm.StringParameter.value_for_string_parameter(  # noqa: F841
            self, "/infraTest/DB_PASSWORD"
        )
        ssm_db_password_interface = ssm.StringParameter.from_string_parameter_name(
            self,
            "ssm_db_password_interface",
            string_parameter_name="/infraTest/DB_PASSWORD",
        )
        ssm_db_password_arn = ssm_db_password_interface.parameter_arn

        cdk.CfnOutput(
            self,
            "ssm-db-password-arn",
            value=ssm_db_password_arn,
            export_name="ssm-db-password-arn",
        )

        # Get DB Host
        ssm_db_host = ssm.StringParameter.value_for_string_parameter(  # noqa: F841
            self, "/infraTest/DB_HOST"
        )
        ssm_db_host_interface = ssm.StringParameter.from_string_parameter_name(
            self, "ssm_db_host_interface", string_parameter_name="/infraTest/DB_HOST"
        )
        ssm_db_host_arn = ssm_db_host_interface.parameter_arn

        cdk.CfnOutput(
            self,
            "ssm-db-host-arn",
            value=ssm_db_host_arn,
            export_name="ssm-db-host-arn",
        )

        # Get S3 Bucket
        ssm_s3 = ssm.StringParameter.value_for_string_parameter(  # noqa: F841
            self, "/infraTest/S3_BUCKET"
        )
        ssm_s3_interface = ssm.StringParameter.from_string_parameter_name(
            self, "ssm_s3_interface", string_parameter_name="/infraTest/S3_BUCKET"
        )
        ssm_s3_arn = ssm_s3_interface.parameter_arn

        cdk.CfnOutput(
            self,
            "ssm-s3-arn",
            value=ssm_s3_arn,
            export_name="ssm-s3-arn",
        )

        # Get Django SecretKey
        ssm_django_secret = (  # noqa: F841
            ssm.StringParameter.value_for_string_parameter(
                self, "/infraTest/SECRET_KEY"
            )
        )
        ssm_django_secret_interface = ssm.StringParameter.from_string_parameter_name(
            self,
            "ssm_django_secret_interface",
            string_parameter_name="/infraTest/SECRET_KEY",
        )
        ssm_django_secret_arn = ssm_django_secret_interface.parameter_arn

        cdk.CfnOutput(
            self,
            "ssm-django-secret-arn",
            value=ssm_django_secret_arn,
            export_name="ssm-django-secret-arn",
        )

        # Get AWS AccessKey
        ssm_aws_access = ssm.StringParameter.value_for_string_parameter(  # noqa: F841
            self, "/infraTest/AWS_ACCESS_KEY_ID"
        )
        ssm_aws_access_interface = ssm.StringParameter.from_string_parameter_name(
            self,
            "ssm_aws_access_interface",
            string_parameter_name="/infraTest/AWS_ACCESS_KEY_ID",
        )
        ssm_aws_access_arn = ssm_aws_access_interface.parameter_arn

        cdk.CfnOutput(
            self,
            "ssm-aws-access-arn",
            value=ssm_aws_access_arn,
            export_name="ssm-aws-access-arn",
        )

        # Get AWS SecretKey
        ssm_aws_secret = ssm.StringParameter.value_for_string_parameter(  # noqa: F841
            self, "/infraTest/AWS_SECRET_ACCESS_KEY"
        )
        ssm_aws_secret_interface = ssm.StringParameter.from_string_parameter_name(
            self,
            "ssm_aws_secret_interface",
            string_parameter_name="/infraTest/AWS_SECRET_ACCESS_KEY",
        )
        ssm_aws_secret_arn = ssm_aws_secret_interface.parameter_arn

        cdk.CfnOutput(
            self,
            "ssm-aws-secret-arn",
            value=ssm_aws_secret_arn,
            export_name="ssm-aws-secret-arn",
        )

        # Get Redis Host
        ssm_redis_host = ssm.StringParameter.value_for_string_parameter(  # noqa: F841
            self, "/infraTest/REDIS_HOST"
        )
        ssm_redis_host_interface = ssm.StringParameter.from_string_parameter_name(
            self,
            "ssm_redis_host_interface",
            string_parameter_name="/infraTest/REDIS_HOST",
        )
        ssm_redis_host_arn = ssm_redis_host_interface.parameter_arn

        cdk.CfnOutput(
            self,
            "ssm-redis-host-arn",
            value=ssm_redis_host_arn,
            export_name="ssm-redis-host-arn",
        )
