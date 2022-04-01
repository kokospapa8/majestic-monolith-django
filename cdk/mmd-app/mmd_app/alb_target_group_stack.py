import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb_v2
import aws_cdk.aws_route53 as route53
import aws_cdk.aws_route53_targets as route53_targets
from constructs import Construct


class AlbTargetGroupStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]
        mmd_vpc = ec2.Vpc.from_vpc_attributes(
            self,
            "bastion_ec2_stack_vpc",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            availability_zones=[
                "ap-northeast-2a",
                "ap-northeast-2b",
                "ap-northeast-2c",
                "ap-northeast-2d",
            ],
        )

        # Create ALB (API)
        mmd_api_alb = elb_v2.ApplicationLoadBalancer(
            self,
            f"mmd-{infra_env}-api-alb",
            security_group=ec2.SecurityGroup.from_security_group_id(
                self,
                f"mmd-{infra_env}-api-alb-sg",
                security_group_id=cdk.Fn.import_value("alb-sg"),
            ),
            vpc=mmd_vpc,
            internet_facing=True,
            load_balancer_name=f"mmd-{infra_env}-api-alb",
            vpc_subnets=ec2.SubnetSelection(
                subnets=[
                    ec2.Subnet.from_subnet_attributes(
                        self,
                        f"mmd-{infra_env}-api-alb-subnet-1",
                        subnet_id=cdk.Fn.import_value("pulbic-subnet-1-id"),
                    ),
                    ec2.Subnet.from_subnet_attributes(
                        self,
                        f"mmd-{infra_env}-api-alb-subnet-2",
                        subnet_id=cdk.Fn.import_value("pulbic-subnet-2-id"),
                    ),
                    ec2.Subnet.from_subnet_attributes(
                        self,
                        f"mmd-{infra_env}-api-alb-subnet-3",
                        subnet_id=cdk.Fn.import_value("pulbic-subnet-3-id"),
                    ),
                    ec2.Subnet.from_subnet_attributes(
                        self,
                        f"mmd-{infra_env}-api-alb-subnet-4",
                        subnet_id=cdk.Fn.import_value("pulbic-subnet-4-id"),
                    ),
                ]
            ),
        )

        # Create Listener (API ALB Listener 80)
        mmd_api_alb_listener = elb_v2.ApplicationTargetGroup(
            self,
            f"mmd-{infra_env}-api-alb-listener",
            port=80,
            target_group_name=f"mmd-{infra_env}-api-alb-listener",
            health_check=elb_v2.HealthCheck(path="/api/healthcheck/"),
            vpc=mmd_vpc,
            target_type=elb_v2.TargetType.IP,
        )

        # Add 80 Listener (API ALB)
        mmd_api_alb_add_listener = mmd_api_alb.add_listener(
            f"mmd-{infra_env}-api-alb-add-listener-80",
            protocol=elb_v2.ApplicationProtocol.HTTP,
            port=80,
            default_action=elb_v2.ListenerAction(
                action_json=elb_v2.CfnListener.ActionProperty(
                    type="forward",
                    target_group_arn=mmd_api_alb_listener.target_group_arn,
                )
            ),
        )

        # Load Hosted Zone
        # mmd_api_hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
        #     self,
        #     f"mmd-api-hosted-zone-load",
        #     hosted_zone_id=cdk.Fn.import_value("api-hosted-zone-id"),
        #     zone_name=f"{infra_env}.mmd-api.com",
        # )

        # Create A Record (API ALB)
        # mmd_api_hosted_a_record = route53.ARecord(
        #     self,
        #     f"mmd-{infra_env}-api-arecord",
        #     zone=mmd_api_hosted_zone,
        #     target=route53.RecordTarget.from_alias(
        #         route53_targets.LoadBalancerTarget(mmd_api_alb)
        #     ),
        #     record_name="api",
        # )

        # Add 443 Listener (API ALB)
        # import aws_cdk.aws_certificatemanager as acm
        # Create mmd-api ACM
        # mmd_api_hosted_zone = route53.PublicHostedZone(
        #     self,
        #     f"mmd-{infra_env}-api-route53",
        #     zone_name=f"{infra_env}.mmd-api.com",
        # )
        # daas_api_acm = acm.Certificate(
        #     self,
        #     f"daas-{infra_env}-api-acm",
        #     domain_name=f"*.{infra_env}.daas-api.com",
        #     validation=acm.CertificateValidation.from_dns(mmd_api_hosted_zone),
        # )
        # mmd_api_alb_add_listener_443 = mmd_api_alb.add_listener(
        #     f"mmd-{infra_env}-api-alb-add-listener-443",
        #     certificates=[
        #         elb_v2.ListenerCertificate(certificate_arn=cdk.Fn.import_value("mmd-api-acm-arn"))
        #     ],
        #     port=443,
        #     protocol=elb_v2.ApplicationProtocol.HTTPS,
        #     default_action=elb_v2.ListenerAction(
        #         action_json=elb_v2.CfnListener.ActionProperty(
        #             type="forward",
        #             target_group_arn=mmd_api_alb_listener.target_group_arn,
        #         )
        #     ),
        # )

        # Create Listener (API ALB Listener 8080)
        mmd_api_alb_listener_8080 = elb_v2.ApplicationTargetGroup(
            self,
            f"mmd-{infra_env}-api-alb-listener-8080",
            port=8080,
            target_group_name=f"mmd-{infra_env}-api-alb-listener-8080",
            health_check=elb_v2.HealthCheck(path="/api/healthcheck/"),
            vpc=mmd_vpc,
            target_type=elb_v2.TargetType.IP,
        )

        # Add 8080 Listener (API ALB) - for blue green deployment
        mmd_api_alb_add_listener_8080 = mmd_api_alb.add_listener(
            f"mmd-{infra_env}-api-alb-add-listener-8080",
            protocol=elb_v2.ApplicationProtocol.HTTP,
            port=8080,
            default_action=elb_v2.ListenerAction(
                action_json=elb_v2.CfnListener.ActionProperty(
                    type="forward",
                    target_group_arn=mmd_api_alb_listener_8080.target_group_arn,
                )
            ),
        )

        cdk.CfnOutput(
            self,
            "alb-dns-name",
            value=mmd_api_alb.load_balancer_dns_name,
            export_name="alb-dns-name",
        )
        cdk.CfnOutput(
            self,
            "alb-target-group-arn",
            value=mmd_api_alb_listener.target_group_arn,
            export_name="alb-target-group-arn",
        )
        cdk.CfnOutput(
            self,
            "alb-target-group-arn-8080",
            value=mmd_api_alb_listener_8080.target_group_arn,
            export_name="alb-target-group-arn-8080",
        )
