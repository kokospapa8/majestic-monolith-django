import aws_cdk as cdk
import aws_cdk.aws_redshift as redshift
import aws_cdk.aws_ssm as ssm
from constructs import Construct


class RedshiftStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]
        ssm_redshift_password = (
            ssm.StringParameter.from_secure_string_parameter_attributes(
                self,
                "/Secure/REDSHIFT_PASSWORD",
                version=1,
                parameter_name="/Secure/REDSHIFT_PASSWORD",
            )
        )
        redshift_paasword = ssm_redshift_password.string_value

        # Create Redshift Subnet Group
        redshift_subnet_group = redshift.CfnClusterSubnetGroup(
            self,
            f"mmd-{infra_env}-app-redshift-subnetgroup",
            description="mmd Redshift Subnet Group",
            subnet_ids=[
                cdk.Fn.import_value("private-subnet-1-id"),
                cdk.Fn.import_value("private-subnet-2-id"),
                cdk.Fn.import_value("private-subnet-3-id"),
                cdk.Fn.import_value("private-subnet-4-id"),
            ],
        )

        # Create Redshift Cluster
        redshift_cluster = redshift.CfnCluster(
            self,
            f"mmd-{infra_env}-app-redshift-cluster",
            cluster_type="multi-node",
            number_of_nodes=2,
            db_name="dw",
            cluster_identifier="mmd-redshift",
            master_username="mmd_admin",
            master_user_password=redshift_paasword,
            node_type="dc2.large",
            cluster_subnet_group_name=redshift_subnet_group.ref,
            vpc_security_group_ids=[
                cdk.Fn.import_value("redshift-sg"),
            ],
            publicly_accessible=False,
            enhanced_vpc_routing=True,
        )

        redshift_cluster.add_depends_on(redshift_subnet_group)
