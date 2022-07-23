from schema import Or, Schema

from .distribution_schemas import center_schema
from .user_schemas import user_profile_schema

shippingitem_schema = Schema(
    {
        "uuid": str,
        "tracking_number": str,
        "sku": str,
        "status": str,
        "shipping_batches_history": list,  # list of dictionary
        "current_distribution_center_code": Or(str, None),
        "timestamp_created": Or(str, None),
        "timestamp_completed": Or(str, None),
    }
)

shippingbatch_schema = Schema(
    {
        "uuid": str,
        "alias": str,
        "completed": bool,
        "shipping_transport": Or(None, dict),
        "timestamp_created": Or(str, None),
        # 'timestamp_transport_assigned': Or(str, None),
        "timestamp_completed": Or(str, None),
    }
)

shippingtransport_schema = Schema(
    {
        "uuid": str,
        "completed": bool,
        "batch_count": int,
        "distribution_center_source": Or(None, center_schema),
        "distribution_center_destination": Or(None, center_schema),
        "driver": Or(None, user_profile_schema),
        "timestamp_created": Or(str, None),
        "timestamp_departed": Or(str, None),
        "timestamp_arrived": Or(str, None),
    }
)
