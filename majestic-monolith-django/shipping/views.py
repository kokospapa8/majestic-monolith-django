from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404 as _get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, permissions, status

from core.permissions import IsStaff

from .models import ShippingItem, ShippingBatch, ShippingTransport
from .serializers import ShippingItemSerializer, ShippingBatchSerializer, \
    ShippingTransportSerializer


class ShippingTransportViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingTransportSerializer
    queryset = ShippingTransport.objects.all()
    permission_classes = [IsStaff]
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
    permission_classes = [IsStaff]
    filter_backends = [DjangoFilterBackend,
                       OrderingFilter]
    filterset_fields = ['completed']
    ordering_fields = ['timestamp_created',
                       'timestamp_completed']
    lookup_field = 'alias'


class ShippingItemViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingItemSerializer
    queryset = ShippingItem.objects.all()
    permission_classes = [IsStaff]
    filter_backends = [DjangoFilterBackend,
                       OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['timestamp_created',
                       'timestamp_completed']
    lookup_field = 'tracking_number'


class TransportBatchesView(generics.ListAPIView):
    serializer_class = ShippingBatchSerializer
    queryset = ShippingBatch.objects.all()
    permission_classes = [IsStaff]
    filter_backends = [DjangoFilterBackend,
                       OrderingFilter]
    filterset_fields = ['completed']
    ordering_fields = ['timestamp_created',
                       'timestamp_completed']
    lookup_url_kwarg = 'uuid'

    # @doc_transport_batches
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    def get_queryset(self):
        filter_kwargs = {'uuid': self.kwargs[self.lookup_url_kwarg]}
        transport = generics.get_object_or_404(ShippingTransport.objects.all(), **filter_kwargs)

        queryset = self.queryset.filter(shipping_transport=transport)
        return queryset


class BatchShippingitemsView(generics.ListAPIView):
    serializer_class = ShippingItemSerializer
    queryset = ShippingItem.objects.all()
    permission_classes = [IsStaff]
    filter_backends = [DjangoFilterBackend,
                       OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['timestamp_created',
                       'timestamp_completed']
    lookup_url_kwarg = 'alias'

    # @doc_transport_batches
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    def get_queryset(self):
        filter_kwargs = {'alias': self.kwargs[self.lookup_url_kwarg]}
        batch = generics.get_object_or_404(ShippingBatch.objects.all(), **filter_kwargs)

        queryset = self.queryset.filter(shipping_batches=batch)
        return queryset
