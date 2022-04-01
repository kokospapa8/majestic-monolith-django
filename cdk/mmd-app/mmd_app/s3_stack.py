import aws_cdk as cdk
import aws_cdk.aws_iam as iam
import aws_cdk.aws_s3 as s3
from constructs import Construct


class S3Stack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]
        ecs_task_role_arn = cdk.Fn.import_value("ecs-server-task-role-arn")

        # Create public S3
        public_s3 = s3.Bucket(
            self,
            f"mmd-{infra_env}-pubilc-s3",
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
            public_read_access=True,
        )

        # Create public S3 (mmd_images)
        public_mmd_images_s3 = s3.Bucket(
            self,
            f"mmd-{infra_env}-pubilc-s3-mmd-images",
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
            public_read_access=True
        )

        # Add Cors Rule (Public S3)
        public_s3.add_cors_rule(
            allowed_methods=[s3.HttpMethods.GET, s3.HttpMethods.POST],
            allowed_origins=["*"],
        )

        # Create Policy_1 (Public S3)
        public_s3_policy_1 = iam.PolicyStatement(
            sid="AllowPublicRead",
            effect=iam.Effect.ALLOW,
            principals=[iam.AnyPrincipal()],
            resources=[public_s3.arn_for_objects("*")],
            actions=["s3:GetObject", "s3:GetObjectVersion"],
        )

        # Add Policy_1 (Public S3)
        public_s3.add_to_resource_policy(public_s3_policy_1)

        # Create Policy_2 (Public S3)
        public_s3_policy_2 = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            principals=[iam.ArnPrincipal(ecs_task_role_arn)],
            resources=[public_s3.arn_for_objects("*")],
            actions=["s3:PutObject", "s3:GetObject",
                     "s3:DeleteObject", "s3:PutObjectAcl"],
        )

        # Add Policy_2 (Public S3)
        public_s3.add_to_resource_policy(public_s3_policy_2)

        cdk.CfnOutput(self, "s3-stack-name",
                      value=self.artifact_id, export_name="s3-stack-name")
