from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from core.permissions import IsStaff
from core.views import BulkDataPostAPIView

from .drf_schema import (
    shipping_batch_item_add_schema,
    shipping_batch_item_list_schema,
    shipping_batch_viewset_schema,
    shipping_item_viewset_schema,
    shipping_transport_batch_add_schema,
    shipping_transport_batch_list_schema,
    shipping_transport_end_schema,
    shipping_transport_start_schema,
    shipping_transport_viewset_schema,
)
from .models import ShippingBatch, ShippingItem, ShippingTransport
from .serializers import (
    ShippingBatchAddSerializer,
    ShippingBatchSerializer,
    ShippingItemAddSerializer,
    ShippingItemSerializer,
    ShippingTransportCompleteSerializer,
    ShippingTransportSerializer,
    ShippingTransportStartSerializer,
)


@extend_schema_view(**shipping_transport_viewset_schema)
class ShippingTransportViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingTransportSerializer
    queryset = ShippingTransport.objects.all()
    permission_classes = [IsStaff | HasAPIKey]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        "completed",
        "driver_uuid",
        "distribution_center_code_source",
        "distribution_center_code_destination",
    ]
    ordering_fields = ["timestamp_created", "timestamp_departed", "timestamp_arrived"]
    lookup_field = "uuid"


@extend_schema_view(**shipping_batch_viewset_schema)
class ShippingBatchViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingBatchSerializer
    queryset = ShippingBatch.objects.all()
    permission_classes = [IsStaff | HasAPIKey]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["completed"]
    ordering_fields = ["timestamp_created", "timestamp_completed"]
    lookup_field = "alias"


@extend_schema_view(**shipping_item_viewset_schema)
class ShippingItemViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingItemSerializer
    queryset = ShippingItem.objects.all()
    permission_classes = [IsStaff | HasAPIKey]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status"]
    ordering_fields = ["timestamp_created", "timestamp_completed"]
    lookup_field = "tracking_number"


class TransportBatchesView(generics.ListAPIView):
    serializer_class = ShippingBatchSerializer
    queryset = ShippingBatch.objects.all()
    permission_classes = [IsStaff | HasAPIKey]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["completed"]
    ordering_fields = ["timestamp_created", "timestamp_completed"]
    lookup_url_kwarg = "uuid"

    @extend_schema(**shipping_transport_batch_list_schema)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        filter_kwargs = {"uuid": self.kwargs[self.lookup_url_kwarg]}
        transport = generics.get_object_or_404(
            ShippingTransport.objects.all(), **filter_kwargs
        )

        queryset = self.queryset.filter(shipping_transport=transport)
        return queryset


class BatchShippingitemsView(generics.ListAPIView):
    serializer_class = ShippingItemSerializer
    queryset = ShippingItem.objects.all()
    permission_classes = [IsStaff | HasAPIKey]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status"]
    ordering_fields = ["timestamp_created", "timestamp_completed"]
    lookup_url_kwarg = "alias"

    @extend_schema(**shipping_batch_item_list_schema)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        filter_kwargs = {"alias": self.kwargs[self.lookup_url_kwarg]}
        batch = generics.get_object_or_404(ShippingBatch.objects.all(), **filter_kwargs)

        queryset = self.queryset.filter(shipping_batches=batch)
        return queryset


class TransportBatchesAddView(BulkDataPostAPIView):
    permission_classes = [IsStaff | HasAPIKey]
    serializer_class = ShippingBatchAddSerializer
    queryset = ShippingTransport.objects.all()
    lookup_url_kwarg = "uuid"
    data_key = "alias"

    def get_extra_context(self):
        filter_kwargs = {"uuid": self.kwargs[self.lookup_url_kwarg]}
        transport = generics.get_object_or_404(
            ShippingTransport.objects.all(), **filter_kwargs
        )
        return {"transport": transport}

    @extend_schema(**shipping_transport_batch_add_schema)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TransportActionBaseView(generics.GenericAPIView):
    permission_classes = [IsStaff | HasAPIKey]
    serializer_class = None
    queryset = ShippingTransport.objects.all()
    lookup_url_kwarg = "uuid"
    lookup_field = "uuid"

    def post(self, request, *args, **kwargs):
        transport = self.get_object()
        serializer = self.get_serializer(
            data=request.data, context={"transport": transport}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransportStartView(TransportActionBaseView):
    serializer_class = ShippingTransportStartSerializer

    @extend_schema(**shipping_transport_start_schema)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TransportCompleteView(TransportActionBaseView):
    serializer_class = ShippingTransportCompleteSerializer

    @extend_schema(**shipping_transport_end_schema)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BatchShippingitemsAddView(BulkDataPostAPIView):
    permission_classes = [IsStaff | HasAPIKey]
    serializer_class = ShippingItemAddSerializer
    queryset = ShippingBatch.objects.all()
    lookup_url_kwarg = "alias"
    data_key = "tracking_number"

    def get_extra_context(self):
        filter_kwargs = {"alias": self.kwargs[self.lookup_url_kwarg]}
        batch = generics.get_object_or_404(ShippingBatch.objects.all(), **filter_kwargs)
        return {"batch": batch}

    @extend_schema(**shipping_batch_item_add_schema)
    def post(self, request, *args, **kwargs):
        errors = []
        serializers = []
        items = []
        # print(self.request.data)
        post_data = self.get_request_data()
        for data in post_data:
            serializer = self.get_serializer(
                data=data, context=self.get_serializer_context()
            )
            if serializer.is_valid(raise_exception=False):
                serializers.append(serializer)
            else:
                data_key = data.get(self.data_key, None)
                error_dict = {data_key: serializer.errors}
                errors.append(error_dict)
        if len(errors) > 0:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            for serializer in serializers:
                serializer.save()
                items.append(serializer.data)
        return Response(items, status=status.HTTP_200_OK)
