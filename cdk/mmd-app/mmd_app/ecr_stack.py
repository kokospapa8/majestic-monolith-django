import aws_cdk as cdk
import aws_cdk.aws_ecr as ecr
from constructs import Construct


class EcrStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]

        # Create ECR API
        ecr_mmd_server = ecr.CfnRepository(
            self,
            f"mmd-{infra_env}-private-api-ecr",
            image_tag_mutability="MUTABLE",
            repository_name="mmd-server",
        )

        # Create Nginx API
        ecr_nginx = ecr.CfnRepository(
            self,
            f"mmd-{infra_env}-private-nginx-ecr",
            image_tag_mutability="MUTABLE",
            repository_name="nginx",
        )

        # Create Xray
        ecr_xray = ecr.CfnRepository(
            self,
            f"mmd-{infra_env}-private-xray-ecr",
            image_tag_mutability="MUTABLE",
            repository_name="xray",
        )

        cdk.CfnOutput(
            self,
            "ecr-mmd-server-arn",
            value=ecr_mmd_server.attr_arn,
            export_name="ecr-mmd-server-arn",
        )
        cdk.CfnOutput(
            self,
            "ecr-nginx-arn",
            value=ecr_nginx.attr_arn,
            export_name="ecr-nginx-arn",
        )
        cdk.CfnOutput(
            self,
            "ecr-xray-arn",
            value=ecr_xray.attr_arn,
            export_name="ecr-xray-arn",
        )
