import aws_cdk as cdk
import aws_cdk.aws_iam as iam
from constructs import Construct

from .iam_custom_policies import (
    get_policy_bastion_instance,
    get_policy_code_deploy,
    get_policy_ecs_execution_policy,
    get_policy_ecs_server_task_policy,
)


class AppIamRoleStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        infra_env = config["INFRA_ENV"]

        ecs_server_task_role = iam.Role(
            self,
            f"mmd-{infra_env}-app-ecsservertask-iam-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            role_name=f"mmd-{infra_env}-app-ecsservertask-iam-role",
            inline_policies=[iam.PolicyDocument(
                statements=[get_policy_ecs_server_task_policy()])],
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AWSXRayDaemonWriteAccess")
            ],
        )

        ecs_server_execution_role = iam.Role(
            self,
            f"mmd-{infra_env}-app-ecsserverexecution-iam-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            role_name=f"mmd-{infra_env}-app-ecsserverexecution-iam-role",
            inline_policies=[iam.PolicyDocument(
                statements=[get_policy_ecs_execution_policy()])],
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(
                    self,
                    "ECSTaskExecutionRolePolicy",
                    managed_policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
                )
            ],
        )

        bastion_instance_role = iam.Role(
            self,
            f"mmd-{infra_env}-app-bastioninstance-iam-role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            role_name=f"mmd-{infra_env}-app-bastioninstance-iam-role",
            inline_policies=[iam.PolicyDocument(
                statements=[get_policy_bastion_instance()])],
        )

        ecs_code_deploy_role = iam.Role(
            self,
            f"mmd-{infra_env}-app-codedeploy-iam-role",
            assumed_by=iam.ServicePrincipal("codedeploy.amazonaws.com"),
            role_name=f"mmd-{infra_env}-app-codedeploy-iam-role",
            inline_policies=[iam.PolicyDocument(
                statements=[get_policy_code_deploy()])],
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(
                    self,
                    "AWSCodeDeployRoleForECS",
                    managed_policy_arn="arn:aws:iam::aws:policy/AWSCodeDeployRoleForECS",
                )
            ],
        )

        cdk.CfnOutput(
            self,
            "mmd-cdk-id",
            value=self.account,
            export_name="mmd-cdk-id",
        )

        cdk.CfnOutput(
            self,
            "ecs-server-task-role",
            value=ecs_server_task_role.role_arn,
            export_name="ecs-server-task-role-arn",
        )

        cdk.CfnOutput(
            self,
            "ecs-server-execution-role",
            value=ecs_server_execution_role.role_arn,
            export_name="ecs-server-execution-role-arn",
        )

        cdk.CfnOutput(
            self,
            "ecs-codedeploy-iam-role",
            value=ecs_code_deploy_role.role_arn,
            export_name="ecs-codedeploy-iam-role-arn",
        )
