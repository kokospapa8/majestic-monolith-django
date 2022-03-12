from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404 as _get_object_or_404

from rest_framework import viewsets
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_api_key.permissions import HasAPIKey

from core.permissions import IsStaff
from core.views import ListDataCreateAPIView

from .models import ShippingItem, ShippingBatch, ShippingTransport
from .serializers import ShippingItemSerializer, ShippingBatchSerializer, \
    ShippingTransportSerializer, ShippingBatchAddSerializer, \
    ShippingItemAddSerializer, ShippingTransportStartSerializer, \
    ShippingTransportCompleteSerializer
from .docs import doc_transport_batches, doc_batch_items


class ShippingTransportViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingTransportSerializer
    queryset = ShippingTransport.objects.all()
    permission_classes = [IsStaff | HasAPIKey]
    filter_backends = [DjangoFilterBackend,
                       OrderingFilter]
    filterset_fields = ['completed', 'driver_uuid',
                        'distribution_center_code_source',
                        'distribution_center_code_destination']
    ordering_fields = ['timestamp_created',
                       'timestamp_departed',
                       'timestamp_arrived']
    lookup_field = 'uuid'


class ShippingBatchViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingBatchSerializer
    queryset = ShippingBatch.objects.all()
    permission_classes = [IsStaff | HasAPIKey]
    filter_backends = [DjangoFilterBackend,
                       OrderingFilter]
    filterset_fields = ['completed']
    ordering_fields = ['timestamp_created',
                       'timestamp_completed']
    lookup_field = 'alias'


class ShippingItemViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingItemSerializer
    queryset = ShippingItem.objects.all()
    permission_classes = [IsStaff | HasAPIKey]
    filter_backends = [DjangoFilterBackend,
                       OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['timestamp_created',
                       'timestamp_completed']
    lookup_field = 'tracking_number'


class TransportBatchesView(generics.ListAPIView):
    serializer_class = ShippingBatchSerializer
    queryset = ShippingBatch.objects.all()
    permission_classes = [IsStaff | HasAPIKey]
    filter_backends = [DjangoFilterBackend,
                       OrderingFilter]
    filterset_fields = ['completed']
    ordering_fields = ['timestamp_created',
                       'timestamp_completed']
    lookup_url_kwarg = 'uuid'

    @doc_transport_batches
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        filter_kwargs = {'uuid': self.kwargs[self.lookup_url_kwarg]}
        transport = generics.get_object_or_404(ShippingTransport.objects.all(), **filter_kwargs)

        queryset = self.queryset.filter(shipping_transport=transport)
        return queryset


class BatchShippingitemsView(generics.ListAPIView):
    serializer_class = ShippingItemSerializer
    queryset = ShippingItem.objects.all()
    permission_classes = [IsStaff | HasAPIKey]
    filter_backends = [DjangoFilterBackend,
                       OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['timestamp_created',
                       'timestamp_completed']
    lookup_url_kwarg = 'alias'

    @doc_batch_items
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        filter_kwargs = {'alias': self.kwargs[self.lookup_url_kwarg]}
        batch = generics.get_object_or_404(ShippingBatch.objects.all(), **filter_kwargs)

        queryset = self.queryset.filter(shipping_batches=batch)
        return queryset


class TransportBatchesAddView(ListDataCreateAPIView):
    permission_classes = [IsStaff | HasAPIKey]
    serializer_class = ShippingBatchAddSerializer
    queryset = ShippingTransport.objects.all()
    lookup_url_kwarg = 'uuid'
    data_key = 'alias'

    def get_extra_context(self):
        filter_kwargs = {'uuid': self.kwargs[self.lookup_url_kwarg]}
        transport = generics.get_object_or_404(ShippingTransport.objects.all(), **filter_kwargs)
        return {"transport": transport}


class TransportActionBaseView(generics.GenericAPIView):
    permission_classes = [IsStaff | HasAPIKey]
    serializer_class = None
    queryset = ShippingTransport.objects.all()
    lookup_url_kwarg = 'uuid'
    lookup_field = 'uuid'

    def post(self, request, *args, **kwargs):
        transport = self.get_object()
        serializer = self.get_serializer(data=request.data,
                                         context={"transport": transport}
                                         )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransportStartView(TransportActionBaseView):
    serializer_class = ShippingTransportStartSerializer


class TransportCompleteView(TransportActionBaseView):
    serializer_class = ShippingTransportCompleteSerializer


class BatchShippingitemsAddView(ListDataCreateAPIView):
    permission_classes = [IsStaff | HasAPIKey]
    serializer_class = ShippingItemAddSerializer
    queryset = ShippingBatch.objects.all()
    lookup_url_kwarg = 'alias'
    data_key = 'tracking_number'

    def get_extra_context(self):
        filter_kwargs = {'alias': self.kwargs[self.lookup_url_kwarg]}
        batch = generics.get_object_or_404(ShippingBatch.objects.all(), **filter_kwargs)
        return {"batch": batch}
