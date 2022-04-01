import aws_cdk as cdk
import aws_cdk.aws_events as events
from constructs import Construct


class EventBridgeStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]

        # Create eventbus
        mmd_pushops_eventbus = events.EventBus(
            self,
            f"mmd-{infra_env}-events-pushops",
            event_bus_name=f"mmd-{infra_env}-events-pushops",
        )

        # Create Archive
        mmd_pushops_eventbus.archive(
            f"mmd-{infra_env}-events-pushops",
            archive_name=f"mmd-{infra_env}-events-pushops",
            description=f"mmd-{infra_env}-events-pushops",
            retention=cdk.Duration.days(90),
            event_pattern=events.EventPattern(
                account=[EventBridgeStack.of(self).account]),
        )
