import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecr as ecr
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_elasticloadbalancingv2 as elb_v2
import aws_cdk.aws_iam as iam
import aws_cdk.aws_logs as logs
import aws_cdk.aws_ssm as ssm
from constructs import Construct


class EcsStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]
        mmd_vpc = ec2.Vpc.from_vpc_attributes(
            self,
            "ecs_stack_vpc",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            availability_zones=[
                "ap-northeast-2a",
                "ap-northeast-2b",
                "ap-northeast-2c",
                "ap-northeast-2d",
            ],
        )
        ecs_security_group = ec2.SecurityGroup.from_security_group_id(
            self, "ecs_stack_sg", security_group_id=cdk.Fn.import_value("ecs-sg")
        )
        ecs_private_subnet_1 = ec2.Subnet.from_subnet_id(
            self,
            "ecs_stack_private_subnet_1",
            subnet_id=cdk.Fn.import_value("private-subnet-1-id"),
        )
        ecs_private_subnet_2 = ec2.Subnet.from_subnet_id(
            self,
            "ecs_stack_private_subnet_2",
            subnet_id=cdk.Fn.import_value("private-subnet-2-id"),
        )
        ecs_private_subnet_3 = ec2.Subnet.from_subnet_id(
            self,
            "ecs_stack_private_subnet_3",
            subnet_id=cdk.Fn.import_value("private-subnet-3-id"),
        )
        ecs_private_subnet_4 = ec2.Subnet.from_subnet_id(
            self,
            "ecs_stack_private_subnet_4",
            subnet_id=cdk.Fn.import_value("private-subnet-4-id"),
        )
        ecs_application_target_group = (
            elb_v2.ApplicationTargetGroup.from_target_group_attributes(
                self,
                "ecs_stack_application_target_group",
                target_group_arn=cdk.Fn.import_value("alb-target-group-arn"),
            )
        )
        ecs_application_target_group_8080 = (  # noqa: F841
            elb_v2.ApplicationTargetGroup.from_target_group_attributes(
                self,
                "ecs_stack_application_target_group_8080",
                target_group_arn=cdk.Fn.import_value("alb-target-group-arn-8080"),
            )
        )
        ecs_server_task_role = iam.Role.from_role_arn(
            self,
            "ecs_stack_server_task_role",
            role_arn=cdk.Fn.import_value("ecs-server-task-role-arn"),
        )
        ecs_server_execution_role = iam.Role.from_role_arn(
            self,
            "ecs_stack_server_execution_role",
            role_arn=cdk.Fn.import_value("ecs-server-execution-role-arn"),
        )
        ssm_db_host = ssm.StringParameter.from_secure_string_parameter_attributes(
            self,
            "/Secure/DB_HOST",
            version=2,
            parameter_name="/Secure/DB_HOST",
        )
        ssm_db_password = ssm.StringParameter.from_secure_string_parameter_attributes(
            self,
            "/Secure/DB_PASSWORD",
            version=1,
            parameter_name="/Secure/DB_PASSWORD",
        )
        ssm_redis_host = ssm.StringParameter.from_secure_string_parameter_attributes(
            self,
            "/Secure/REDIS_HOST",
            version=2,
            parameter_name="/Secure/REDIS_HOST",
        )
        ssm_django_secret = ssm.StringParameter.from_secure_string_parameter_attributes(
            self,
            "/Secure/SECRET_KEY",
            version=1,
            parameter_name="/Secure/SECRET_KEY",
        )
        ssm_s3 = ssm.StringParameter.from_secure_string_parameter_attributes(
            self,
            "/Secure/S3_BUCKET",
            version=1,
            parameter_name="/Secure/S3_BUCKET",
        )
        ssm_slack_token = ssm.StringParameter.from_secure_string_parameter_attributes(
            self,
            "/Secure/SLACK_TOKEN",
            version=1,
            parameter_name="/Secure/SLACK_TOKEN",
        )
        ecr_mmd_server_container = ecr.Repository.from_repository_attributes(
            self,
            "ecr_mmd_server_uri",
            repository_name="mmd-server",
            repository_arn=cdk.Fn.import_value("ecr-mmd-server-arn"),
        )
        ecr_nginx_container = ecr.Repository.from_repository_attributes(
            self,
            "ecr_nginx_uri",
            repository_name="nginx",
            repository_arn=cdk.Fn.import_value("ecr-nginx-arn"),
        )
        # ecr_xray_container = ecr.Repository.from_repository_attributes(
        #     self,
        #     "ecr_xray_uri",
        #     repository_name="xray",
        #     repository_arn=cdk.Fn.import_value("ecr-xray-arn"),
        # )

        # Create ECS Cluster
        mmd_api_cluster = ecs.Cluster(
            self,
            f"mmd-{infra_env}-private-api-ecs-cluster",
            cluster_name=f"mmd-{infra_env}-private-api-ecs-cluster",
            container_insights=True,
            vpc=mmd_vpc,
        )

        # Create ECS Task Definition
        mmd_ecs_api_task_definition = ecs.FargateTaskDefinition(
            self,
            f"mmd-{infra_env}-private-api-ecs-task",
            cpu=1024,
            memory_limit_mib=2048,
            task_role=ecs_server_task_role,
            execution_role=ecs_server_execution_role,
        )

        # Create ECS Nginx Container
        mmd_ecs_nginx_container = mmd_ecs_api_task_definition.add_container(
            f"mmd-{infra_env}-private-nginx-ecs-container",
            image=ecs.ContainerImage.from_registry(
                f"{ecr_nginx_container.repository_uri}"
            ),
            container_name="nginx",
            memory_limit_mib=512,
            port_mappings=[
                ecs.PortMapping(
                    container_port=80,
                    host_port=80,
                )
            ],
            logging=ecs.LogDriver.aws_logs(
                stream_prefix="ecs",
                log_group=logs.LogGroup.from_log_group_name(
                    self,
                    f"mmd-{infra_env}-nginx-loggroup",
                    log_group_name="/ecs/mmd-nginx",
                ),
            ),
        )

        # Create ECS Xray Container
        # mmd_ecs_xray_container = mmd_ecs_api_task_definition.add_container(
        #     f"mmd-{infra_env}-private-xray-ecs-container",
        #     image=ecs.ContainerImage.from_registry("amazon/aws-xray-daemon"),
        #     container_name="xray",
        #     cpu=32,
        #     memory_limit_mib=256,
        #     port_mappings=[
        #         ecs.PortMapping(container_port=2000, host_port=2000, protocol=ecs.Protocol.UDP)
        #     ],
        #     environment={
        #         "AWS_REGION": "ap-northeast-2",
        #     },
        #     logging=ecs.LogDriver.aws_logs(
        #         stream_prefix="xray",
        #         log_group=logs.LogGroup.from_log_group_name(
        #             self, f"mmd-{infra_env}-xray-loggroup", log_group_name="/mmd/xray"
        #         ),
        #     ),
        # )

        # Create ECS mmd-api Container
        mmd_ecs_mmd_server_container = mmd_ecs_api_task_definition.add_container(
            f"mmd-{infra_env}-private-api-ecs-container",
            image=ecs.ContainerImage.from_registry(
                f"{ecr_mmd_server_container.repository_uri}"
            ),
            container_name="api",
            memory_limit_mib=1024,
            port_mappings=[
                ecs.PortMapping(
                    container_port=8000,
                    host_port=8000,
                )
            ],
            logging=ecs.LogDriver.aws_logs(
                stream_prefix="ecs",
                log_group=logs.LogGroup.from_log_group_name(
                    self,
                    f"mmd-{infra_env}-mmd-api-loggroup",
                    log_group_name="/ecs/mmd-api",
                ),
            ),
            health_check=ecs.HealthCheck(
                command=["CMD-SHELL", "python manage.py check"],
                interval=cdk.Duration.seconds(30),
                retries=5,
                timeout=cdk.Duration.seconds(10),
            ),
            environment={
                "APP": "api",
                "AWS_DEFAULT_REGION": "ap-northeast-2",
                "DJANGO_SETTINGS_MODULE": f"settings.{infra_env}",
                "ENV": infra_env,
            },
            secrets={
                "DB_HOST": ecs.Secret.from_ssm_parameter(ssm_db_host),
                "DB_PASSWORD": ecs.Secret.from_ssm_parameter(ssm_db_password),
                "REDIS_HOST": ecs.Secret.from_ssm_parameter(ssm_redis_host),
                "S3_BUCKET": ecs.Secret.from_ssm_parameter(ssm_s3),
                "SECRET_KEY": ecs.Secret.from_ssm_parameter(ssm_django_secret),
                "SLACK_TOKEN": ecs.Secret.from_ssm_parameter(ssm_slack_token),
            },
            docker_labels={"name": "mmd-api", "env": infra_env},
        )

        # Container Dependency
        mmd_ecs_container_dependency = ecs.ContainerDependency(
            container=mmd_ecs_mmd_server_container,
            condition=ecs.ContainerDependencyCondition.HEALTHY,
        )
        mmd_ecs_nginx_container.add_container_dependencies(mmd_ecs_container_dependency)
        # mmd_ecs_xray_container.add_container_dependencies(mmd_ecs_container_dependency)

        # Create ECS Service
        ecs_api_service = ecs.FargateService(
            self,
            f"mmd-{infra_env}-private-api-ecs-service",
            task_definition=mmd_ecs_api_task_definition,
            cluster=mmd_api_cluster,
            vpc_subnets=ec2.SubnetSelection(
                subnets=[
                    ecs_private_subnet_1,
                    ecs_private_subnet_2,
                    ecs_private_subnet_3,
                    ecs_private_subnet_4,
                ]
            ),
            security_groups=[ecs_security_group],
            service_name=f"mmd-{infra_env}-private-api-ecs-service",
            assign_public_ip=True,
            deployment_controller=ecs.DeploymentController(
                type=ecs.DeploymentControllerType.CODE_DEPLOY
            ),
            desired_count=1,
        )

        # Add Target Group 80
        ecs_api_service.attach_to_application_target_group(
            target_group=ecs_application_target_group
        )
