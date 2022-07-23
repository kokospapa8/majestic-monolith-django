import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from constructs import Construct


class SecurityGroupStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        infra_env = config["INFRA_ENV"]

        # Create alb sg
        alb_sg = ec2.CfnSecurityGroup(
            self,
            f"mmd-{infra_env}-alb-sg",
            group_description="alb sg",
            group_name=f"mmd-{infra_env}-alb-sg",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            security_group_ingress=[
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp", cidr_ip="0.0.0.0/0", from_port=443, to_port=443
                ),
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp", cidr_ip="0.0.0.0/0", from_port=80, to_port=80
                ),
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp", cidr_ip="0.0.0.0/0", from_port=8080, to_port=8080
                ),
            ],
        )

        # Create ecs sg
        ecs_sg = ec2.CfnSecurityGroup(
            self,
            f"mmd-{infra_env}-ecs-sg",
            group_description="ecs sg",
            group_name=f"mmd-{infra_env}-ecs-sg",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            security_group_ingress=[
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    source_security_group_id=alb_sg.ref,
                    from_port=80,
                    to_port=80,
                )
            ],
        )

        # Create bastion sg
        bastion_sg = ec2.CfnSecurityGroup(
            self,
            f"mmd-{infra_env}-bastion-sg",
            group_description="bastion sg",
            group_name=f"mmd-{infra_env}-bastion-sg",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            security_group_ingress=[
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    cidr_ip="211.226.225.105/32",
                    from_port=22,
                    to_port=22,
                    description="dongkyu home",
                ),
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    cidr_ip="183.98.54.252/32",
                    from_port=22,
                    to_port=22,
                    description="kokospapa home",
                ),
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    cidr_ip="121.138.24.180/32",
                    from_port=22,
                    to_port=22,
                    description="kokospapa 4F",
                ),
            ],
        )

        # Create bastion sg (retool)
        retool_bastion_sg = ec2.CfnSecurityGroup(
            self,
            f"mmd-{infra_env}-retool-bastion-sg",
            group_description="Retool bastion sg",
            group_name=f"mmd-{infra_env}-retool-bastion-sg",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            security_group_ingress=[
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    cidr_ip="52.175.251.223/32",
                    from_port=22,
                    to_port=22,
                    description="Retool Whitelist",
                ),
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    cidr_ip="121.135.221.237/32",
                    from_port=22,
                    to_port=22,
                ),
            ],
        )

        # Create redis sg
        redis_sg = ec2.CfnSecurityGroup(
            self,
            f"mmd-{infra_env}-redis-sg",
            group_description="redis sg",
            group_name=f"mmd-{infra_env}-redis-sg",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            security_group_ingress=[
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    source_security_group_id=bastion_sg.ref,
                    from_port=6379,
                    to_port=6379,
                ),
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    source_security_group_id=ecs_sg.ref,
                    from_port=6379,
                    to_port=6379,
                ),
            ],
        )

        # Create lambda sg
        lambda_sg = ec2.CfnSecurityGroup(
            self,
            f"mmd-{infra_env}-labmda-sg",
            group_description="lambda sg",
            group_name=f"mmd-{infra_env}-labmda-sg",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            security_group_ingress=[
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp", cidr_ip="0.0.0.0/0", from_port=443, to_port=443
                ),
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp", cidr_ip="0.0.0.0/0", from_port=80, to_port=80
                ),
            ],
        )

        # Create mysql sg
        mysql_sg = ec2.CfnSecurityGroup(
            self,
            f"mmd-{infra_env}-mysql-sg",
            group_description="mysql sg",
            group_name=f"mmd-{infra_env}-mysql-sg",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            security_group_ingress=[
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    source_security_group_id=bastion_sg.ref,
                    from_port=3306,
                    to_port=3306,
                ),
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    source_security_group_id=retool_bastion_sg.ref,
                    from_port=3306,
                    to_port=3306,
                ),
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    source_security_group_id=ecs_sg.ref,
                    from_port=3306,
                    to_port=3306,
                ),
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    source_security_group_id=lambda_sg.ref,
                    from_port=3306,
                    to_port=3306,
                ),
            ],
        )

        # Create vpc endpoint(ssm)
        ssm_vpc_endpoint = ec2.CfnVPCEndpoint(
            self,
            f"mmd-{infra_env}-ssm-vpc-endpoint",
            service_name="com.amazonaws.ap-northeast-2.ssm",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            subnet_ids=[
                cdk.Fn.import_value("pulbic-subnet-1-id"),
                cdk.Fn.import_value("private-subnet-2-id"),
                cdk.Fn.import_value("private-subnet-3-id"),
                cdk.Fn.import_value("pulbic-subnet-4-id"),
            ],
            security_group_ids=[
                lambda_sg.ref,
            ],
            private_dns_enabled=True,
            vpc_endpoint_type="Interface",
        )

        # Create vpc endpoint(events)
        events_vpc_endpoint = ec2.CfnVPCEndpoint(
            self,
            f"mmd-{infra_env}-events-vpc-endpoint",
            service_name="com.amazonaws.ap-northeast-2.events",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            subnet_ids=[
                cdk.Fn.import_value("pulbic-subnet-1-id"),
                cdk.Fn.import_value("private-subnet-2-id"),
                cdk.Fn.import_value("private-subnet-3-id"),
                cdk.Fn.import_value("pulbic-subnet-4-id"),
            ],
            security_group_ids=[
                lambda_sg.ref,
            ],
            private_dns_enabled=True,
            vpc_endpoint_type="Interface",
        )

        ssm_vpc_endpoint.add_depends_on(lambda_sg)
        events_vpc_endpoint.add_depends_on(ssm_vpc_endpoint)

        cdk.CfnOutput(self, "alb-sg", value=alb_sg.ref, export_name="alb-sg")
        cdk.CfnOutput(self, "ecs-sg", value=ecs_sg.ref, export_name="ecs-sg")
        cdk.CfnOutput(
            self, "bastion_sg", value=bastion_sg.ref, export_name="bastion-sg"
        )
        cdk.CfnOutput(
            self,
            "retool_bastion_sg",
            value=retool_bastion_sg.ref,
            export_name="retool-bastion-sg",
        )
        cdk.CfnOutput(self, "redis-sg", value=redis_sg.ref, export_name="redis-sg")
        cdk.CfnOutput(self, "mysql-sg", value=mysql_sg.ref, export_name="mysql-sg")
