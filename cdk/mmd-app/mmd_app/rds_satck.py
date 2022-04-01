import aws_cdk as cdk
import aws_cdk.aws_rds as rds
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_ssm as ssm
from constructs import Construct


class RdsStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]
        rds_role = f"arn:aws:iam::{self.account}:role/aws-service-role/rds.amazonaws.com/AWSServiceRoleForRDS"
        ssm_db_password = ssm.StringParameter.from_secure_string_parameter_attributes(
            self,
            "/Secure/DB_PASSWORD",
            version=2,
            parameter_name="/Secure/DB_PASSWORD",
        )
        rds_password = ssm_db_password.string_value
        print(rds_password)
        # rds_password = config["DB_PASSWORD"]

        # Create Subnet Group
        rds_subnet_group = rds.CfnDBSubnetGroup(
            self,
            f"mmd-{infra_env}-app-aurora-cluster-subnetgroup",
            db_subnet_group_description=f"mmd aurora cluster subnetgroup",
            subnet_ids=[
                cdk.Fn.import_value("private-subnet-1-id"),
                cdk.Fn.import_value("private-subnet-2-id"),
                cdk.Fn.import_value("private-subnet-3-id"),
                cdk.Fn.import_value("private-subnet-4-id"),
            ],
            db_subnet_group_name=f"mmd-{infra_env}-app-aurora-cluster-subnetgroup",
        )

        # Create DB Cluster Parameter Group
        aurora_rds_cluster_parameter = rds.CfnDBClusterParameterGroup(
            self,
            f"mmd-{infra_env}-app-aurora-cluster-parameter",
            family="aurora-mysql5.7",
            description="aurora 5.7 cluster parameter group",
            parameters={
                "character_set_server": "utf8mb4",
                "character_set_connection": "utf8mb4",
                "character_set_database": "utf8mb4",
                "character_set_filesystem": "utf8mb4",
                "character_set_results": "utf8mb4",
                "character_set_client": "utf8mb4",
                "collation_connection": "utf8mb4_general_ci",
                "collation_server": "utf8mb4_general_ci",
            },
        )

        # Create Aurora Cluster
        aurora_rds_cluster = rds.CfnDBCluster(
            self,
            f"mmd-{infra_env}-app-aurora-cluster",
            associated_roles=[
                rds.CfnDBCluster.DBClusterRoleProperty(role_arn=rds_role)],
            engine="aurora-mysql",
            engine_mode="provisioned",
            backtrack_window=0,
            backup_retention_period=1,
            db_subnet_group_name=f"mmd-{infra_env}-app-aurora-cluster-subnetgroup",
            db_cluster_parameter_group_name=aurora_rds_cluster_parameter.ref,
            db_cluster_identifier=f"mmd-{infra_env}-app-aurora-cluster",
            master_username="admin",
            master_user_password=rds_password,
            port=3306,
            storage_encrypted=False,
            vpc_security_group_ids=[cdk.Fn.import_value("mysql-sg")],
            database_name="mmd",
        )

        # Create Aurora Instance
        aurora_rds_instance_1 = rds.CfnDBInstance(
            self,
            f"mmd-{infra_env}-app-aurora-instance1",
            db_cluster_identifier=aurora_rds_cluster.ref,
            db_instance_class="db.r5.large",
            db_instance_identifier=f"mmd-{infra_env}-app-aurora-instance1",
            engine="aurora-mysql",
        )

        # # Create Aurora Read Instance
        aurora_rds_read_instance_1 = rds.CfnDBInstance(
            self,
            f"mmd-{infra_env}-app-aurora-read-instance1",
            db_instance_class="db.r5.large",
            db_cluster_identifier=aurora_rds_cluster.ref,
            db_instance_identifier=f"mmd-{infra_env}-app-aurora-read-instance1",
            source_db_instance_identifier=aurora_rds_instance_1.source_db_instance_identifier,
            engine="aurora-mysql",
        )

        aurora_rds_cluster.add_depends_on(rds_subnet_group)
        aurora_rds_cluster.add_depends_on(aurora_rds_cluster_parameter)
        aurora_rds_instance_1.add_depends_on(aurora_rds_cluster)
        aurora_rds_read_instance_1.add_depends_on(aurora_rds_instance_1)

        cdk.CfnOutput(
            self,
            "rds-test",
            value=aurora_rds_cluster_parameter.ref,
            export_name="rds-test",
        )

        cdk.CfnOutput(
            self,
            "rds-endpoint",
            value=aurora_rds_cluster.attr_endpoint_address,
            export_name="rds-end-point",
        )
