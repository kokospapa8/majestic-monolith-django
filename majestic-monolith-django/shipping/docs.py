from drf_yasg.utils import swagger_auto_schema
from core.docs import dict_response_schema, param, list_response_schema


shipping_items_response = {
  "uuid": "45563485-ca00-43e7-b573-7890fd4c3822",
  "tracking_number": "20220309-0003066198",
  "sku": "1234",
  "status": "CREATED",
  "shipping_batches_history": [
      {
          "alias": "20220309-CqaaCZx",
          "completed": True,
          "shipping_transport__uuid": "ef7d79b3-5267-4f02-acde-593844fb02a0",
          "shipping_transport__distribution_center_code_source": "AFK",
          "shipping_transport__distribution_center_code_destination": "S01"
      },
      {
          "alias": "20220309-xWK",
          "completed": False,
          "shipping_transport__uuid": None,
          "shipping_transport__distribution_center_code_source": None,
          "shipping_transport__distribution_center_code_destination": None
      }
  ],
  "current_distribution_center_code": "S01",
  "timestamp_created": "2022-03-01T22:03:00+09:00",
  "timestamp_completed": None
}

shipping_batch_response = {
    "uuid": "5dd9b051-9c42-417e-9287-71751b9442b2",
    "alias": "20220309-xWK",
    "completed": False,
    "shipping_transport": None,
    "timestamp_created": None,
    "timestamp_completed": None
}

shipping_transport_response = {
    "uuid": "ef7d79b3-5267-4f02-acde-593844fb02a0",
    "completed": False,
    "batch_count": 2,
    "distribution_center_source": {
        "uuid": "48574f05-a29e-4735-a817-839b228c3e82",
        "center_code": "AFK",
        "name": "AFK",
        "staff_names": ""
    },
    "distribution_center_destination": None,
    "driver": None,
    "timestamp_created": "2022-03-09T22:20:15.418651+09:00",
    "timestamp_departed": "2022-03-12T16:15:35.224593+09:00",
    "timestamp_arrived": "2022-03-12T16:24:32.355557+09:00"
}

doc_transport_batches = swagger_auto_schema(
    operation_id='transport_batches',
    operation_description=
    'Description: \n'
    '  - list batches in transport \n'
    '  - \n\n'
    'Params: \n'
    '- ordering: timestamp_created, timestamp_completed\n'
    '- completed: 1, 0\n\n'
    'Permission: '
    '  - IsStaff | HasAPIKey\n\n'
    'Link: <link for extra information>',
    operation_summary="list batches in transport",
    manual_parameters=[
        param('ordering', 'timestamp_created, timestamp_completed, -timestamp_created, -timestamp_completed'),
        param('completed', '1, 0')
    ],
    tags=["shipping"],
    responses={
        200: dict_response_schema(
            list_response_schema(
                shipping_batch_response
            )
        ),
    }
)

doc_batch_items = swagger_auto_schema(
    operation_id='batch_items',
    operation_description=
    'Description: \n'
    '  - list shipping items in a batch \n'
    '  - \n\n'
    'Params: \n'
    '- status: \n'
    '- ordering: timestamp_created, timestamp_completed\n\n'
    'Permission: '
    '  - IsStaff | HasAPIKey\n\n'
    'Link: <link for extra information>',
    operation_summary="list shipping items in a batch \n",
    manual_parameters=[
        param('status', 'CREATED, MOVING, COMPLETED, DAMAGED, LOST'),
        param('completed', '1, 0')
    ],
    tags=["shipping"],
    responses={
        200: dict_response_schema(
            list_response_schema(
                shipping_items_response
            )
        )
    }
)