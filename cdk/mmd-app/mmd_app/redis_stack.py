import aws_cdk as cdk
import aws_cdk.aws_elasticache as cache
from constructs import Construct


class CacheStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]

        # Create Redis Subnet Group
        redis_subnet_group = cache.CfnSubnetGroup(
            self,
            f"mmd-{infra_env}-app-rediscluster-subnetgroup",
            description=f"{infra_env} redis subnet group",
            subnet_ids=[
                cdk.Fn.import_value("private-subnet-1-id"),
                cdk.Fn.import_value("private-subnet-2-id"),
                cdk.Fn.import_value("private-subnet-3-id"),
                cdk.Fn.import_value("private-subnet-4-id"),
            ],
            cache_subnet_group_name=f"mmd-{infra_env}-app-rediscluster-subnetgroup",
        )

        # Create Redis Cluster (Clustermode ON)
        redis_cluster = cache.CfnReplicationGroup(
            self,
            f"mmd-{infra_env}-app-rediscluster",
            replication_group_description=f"{infra_env} redis(cluster mode on) group",
            cache_node_type="cache.t3.micro",
            cache_parameter_group_name="default.redis5.0.cluster.on",
            security_group_ids=[cdk.Fn.import_value("redis-sg")],
            engine="redis",
            engine_version="5.0.4",
            num_node_groups=1,
            replicas_per_node_group=1,
            cache_subnet_group_name=redis_subnet_group.cache_subnet_group_name,
        )

        redis_cluster.add_depends_on(redis_subnet_group)
