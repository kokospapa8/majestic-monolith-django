import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from constructs import Construct


class Ec2Stack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]
        ec2_key = config["KEY_NAME"]

        # App Instance_1 Shell Command
        ec2_app_instance_1_shellCommands = ec2.UserData.for_linux()
        ec2_app_instance_1_shellCommands.add_commands(
            "sudo apt-get update && sudo apt-get install squid",
            'echo "http_port 3306 transparent" | sudo tee -a /etc/squid/squid.conf',
            'sudo sed -i "s/http_access deny all/http_access allow all/" /etc/squid/squid.conf',
            "sudo systemctl restart squid",
        )

        # Create Instance (Using CfnInstance)
        ec2_app_instance_1 = ec2.CfnInstance(
            self,
            f"mmd-{infra_env}-app1-instance",
            image_id="ami-0ba5cd124d7a79612",
            instance_initiated_shutdown_behavior="terminate",
            instance_type="t3.nano",
            key_name=ec2_key,
            security_group_ids=[cdk.Fn.import_value("bastion-sg")],
            subnet_id=cdk.Fn.import_value("pulbic-subnet-1-id"),
            user_data=cdk.Fn.base64(ec2_app_instance_1_shellCommands.render()),
        )

        # Create EIP (ec2_app_instance_1)
        ec2_app_instance_1_eip = ec2.CfnEIP(
            self, f"mmd-{infra_env}-app-instance1-eip")

        # EIP Association (ec2_app_instance_1)
        ec2_app_instance_1_eip_asso = ec2.CfnEIPAssociation(
            self,
            f"mmd-{infra_env}-app-instance1-eip-asso",
            eip=ec2_app_instance_1_eip.ref,
            instance_id=ec2_app_instance_1.ref,
        )

        # Create Instance_2 (Using CfnInstance)
        ec2_app_instance_2 = ec2.CfnInstance(
            self,
            f"mmd-{infra_env}-app-instance2",
            image_id="ami-0ba5cd124d7a79612",
            instance_initiated_shutdown_behavior="terminate",
            instance_type="t3.nano",
            key_name=ec2_key,
            security_group_ids=[cdk.Fn.import_value("retool-bastion-sg")],
            subnet_id=cdk.Fn.import_value("pulbic-subnet-1-id"),
            user_data=cdk.Fn.base64(ec2_app_instance_1_shellCommands.render()),
        )

        # Create EIP (ec2_app_instance_2)
        ec2_app_instance_2_eip = ec2.CfnEIP(
            self, f"mmd-{infra_env}-app-instance2-eip")

        # EIP Association (ec2_app_instance_2)
        ec2_app_instance_2_eip_asso = ec2.CfnEIPAssociation(
            self,
            f"mmd-{infra_env}-app-instance2-eip-asso",
            eip=ec2_app_instance_2_eip.ref,
            instance_id=ec2_app_instance_2.ref,
        )
