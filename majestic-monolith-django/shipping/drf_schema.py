from drf_spectacular.utils import extend_schema

from core.serializers import ErrorListSerializer

from .serializers import (
    ShippingBatchAddSerializer,
    ShippingBatchSerializer,
    ShippingItemAddSerializer,
    ShippingItemSerializer,
    ShippingTransportSerializer,
)

shipping_item_viewset_schema = {
    "list": extend_schema(
        summary="List Shipping Items",
        description="list all shipping items.",
        tags=["shipping", "shipping - item"],
    ),
    "create": extend_schema(
        summary="Create a Shipping Item",
        description="create a shipping item",
        tags=["shipping", "shipping - item"],
    ),
    "retrieve": extend_schema(
        summary="Get a Shipping Item",
        description="get a shipping item by uuid",
        tags=["shipping", "shipping - item"],
    ),
    "destroy": extend_schema(
        summary="Delete a Shipping Item",
        description="delete a shipping item",
        tags=["shipping", "shipping - item"],
    ),
    "partial_update": extend_schema(
        summary="Update a Shipping Item",
        description="update a shipping item",
        tags=["shipping", "shipping - item"],
    ),
}

shipping_batch_viewset_schema = {
    "list": extend_schema(
        summary="List Shipping Batches",
        description="list all shipping batches.",
        tags=["shipping", "shipping - batch"],
    ),
    "create": extend_schema(
        summary="Create a Shipping Batch",
        description="create a shipping batch",
        tags=["shipping", "shipping - batch"],
    ),
    "retrieve": extend_schema(
        summary="Get a Shipping Batch",
        description="get a shipping batch by uuid",
        tags=["shipping", "shipping - batch"],
    ),
    "destroy": extend_schema(
        summary="Delete a Shipping Batch",
        description="delete a shipping batch",
        tags=["shipping", "shipping - batch"],
    ),
    "partial_update": extend_schema(
        summary="Update a Shipping Batch",
        description="update a shipping batch",
        tags=["shipping", "shipping - batch"],
    ),
}

shipping_transport_viewset_schema = {
    "list": extend_schema(
        summary="List Shipping Transports",
        description="list all shipping transports",
        tags=["shipping", "shipping - transport"],
    ),
    "create": extend_schema(
        summary="Create a Shipping Transport",
        description="create a shipping transport",
        tags=["shipping", "shipping - transport"],
    ),
    "retrieve": extend_schema(
        summary="Get a Shipping Transport",
        description="get a shipping transport by uuid",
        tags=["shipping", "shipping - transport"],
    ),
    "destroy": extend_schema(
        summary="Delete a Shipping Transport",
        description="delete a shipping transport",
        tags=["shipping", "shipping - transport"],
    ),
    "partial_update": extend_schema(
        summary="Update a Shipping Transport",
        description="update a shipping transport",
        tags=["shipping", "shipping - transport"],
    ),
}

shipping_transport_batch_list_schema = {
    "summary": "List Transport Batches",
    "description": "list batches in a single transport",
    "tags": ["shipping", "shipping - transport"],
}

shipping_batch_item_list_schema = {
    "summary": "List Batch Items",
    "description": "list items in a single batch",
    "tags": ["shipping", "shipping - batch"],
}

shipping_batch_item_add_schema = {
    "summary": "Batch Shipping Items Add",
    "description": "Add Shipping items to a batch",
    "tags": ["shipping", "shipping - batch"],
    "responses": {200: ShippingItemSerializer(many=True), 400: ErrorListSerializer},
    "request": ShippingItemAddSerializer(many=True),
}

shipping_transport_batch_add_schema = {
    "summary": "Transport Batches Add",
    "description": "Add Shipping batches to a transport",
    "tags": ["shipping", "shipping - transport"],
    "responses": {200: ShippingBatchSerializer(many=True), 400: ErrorListSerializer},
    "request": ShippingBatchAddSerializer(many=True),
}

shipping_transport_start_schema = {
    "summary": "Transport Start",
    "description": "start the shipping transport",
    "tags": ["shipping", "shipping - transport"],
    "responses": {200: ShippingTransportSerializer},
}

shipping_transport_end_schema = {
    "summary": "Transport End",
    "description": "finish the shipping transport",
    "tags": ["shipping", "shipping - transport"],
    "responses": {200: ShippingTransportSerializer},
}
