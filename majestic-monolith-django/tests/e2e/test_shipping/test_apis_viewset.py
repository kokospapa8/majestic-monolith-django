from unittest import mock

import pytest
from django.shortcuts import resolve_url
from django.apps import apps
from django.conf import settings

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from tests.conftest import CustomClient

from tests.schemas.auth_schemas import token_schema, signup_schema

from auth.serializers import SigninTokenConfirmSerializer
from auth.utils_auth import bypass_token_request
from auth.caches import PhonenumberVerificationCache

from tests.schemas.shipping_schemas import shippingitem_schema, \
    shippingbatch_schema, shippingtransport_schema

DistributionCenter = apps.get_model('distribution', 'DistributionCenter')
ShippingItem = apps.get_model('shipping', 'ShippingItem')
ShippingBatch = apps.get_model('shipping', 'ShippingBatch')
ShippingTransport = apps.get_model('shipping', 'ShippingTransport')


@pytest.mark.django_db
class TestShippingItemViewSet:
    # test CRUD

    def test_shippingitem_list_unauthorized(self, client):
        url = resolve_url('shippingitem-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_shippingitem_list_initail(self, staff_user):
        url = resolve_url('shippingitem-list')
        client = CustomClient()
        client.force_login(staff_user)
        response = client.get(url)
        assert len(response.json()['results']) == 1

    def test_shippingitem_create(self, staff_user, new_shipping_item):
        url = resolve_url('shippingitem-list')
        client = CustomClient()
        client.force_login(staff_user)
        response = client.post(url, {
            "sku": new_shipping_item['sku'],
        })
        print(response.json())
        assert response.status_code == status.HTTP_201_CREATED
        new_item_tracking_number = response.json()['tracking_number']
        assert shippingitem_schema.is_valid(response.json())

        assert response.json()['sku'] == new_shipping_item['sku']

        url = resolve_url('shippingitem-list')
        response = client.get(url)
        assert len(response.json()['results']) == 2

        url = resolve_url('shippingitem-detail',
                          tracking_number=new_item_tracking_number)
        response = client.get(url)
        assert response.json()['tracking_number'] == new_item_tracking_number


@pytest.mark.django_db
class TestShippingBatchViewSet:
    def test_shippingbatch_list_unauthorized(self, client):
        url = resolve_url('batch-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_shippingbatch_list_empty(self, staff_user):
        url = resolve_url('batch-list')
        client = CustomClient()
        client.force_login(staff_user)
        response = client.get(url)
        assert len(response.json()['results']) == 0

    def test_shippingbatch_create(self, staff_user, new_batch):
        url = resolve_url('batch-list')
        client = CustomClient()
        client.force_login(staff_user)
        response = client.post(url, {
            "alias": new_batch['alias'],
        })
        print(response.json())
        assert response.status_code == status.HTTP_201_CREATED
        new_alias = response.json()['alias']
        assert shippingbatch_schema.is_valid(response.json())

        assert response.json()['alias'] == new_batch['alias']

        url = resolve_url('batch-list')
        response = client.get(url)
        assert len(response.json()['results']) == 1

        url = resolve_url('batch-detail',
                          alias=new_alias)
        response = client.get(url)
        assert response.json()['alias'] == new_alias


@pytest.mark.django_db
class TestShippingTransportViewSet:
    def test_shippingtransport_list_unauthorized(self, client):
        url = resolve_url('transport-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_shippingtransport_list_empty(self, staff_user):
        url = resolve_url('transport-list')
        client = CustomClient()
        client.force_login(staff_user)
        response = client.get(url)
        assert len(response.json()['results']) == 0

    def test_shippingtransport_create(self, staff_user, new_transport):
        url = resolve_url('transport-list')
        client = CustomClient()
        client.force_login(staff_user)
        response = client.post(url, {
            "distribution_center_code_source":
                new_transport['distribution_center_code_source'],
            "distribution_center_code_destination":
                new_transport['distribution_center_code_destination'],
        })
        print(response.json())
        assert response.status_code == status.HTTP_201_CREATED
        new_uuid = response.json()['uuid']
        assert shippingtransport_schema.is_valid(response.json())

        assert response.json()['distribution_center_source']['center_code'] == \
            new_transport['distribution_center_code_source']
        assert response.json()['distribution_center_destination']['center_code'] == \
            new_transport['distribution_center_code_destination']

        url = resolve_url('transport-list')
        response = client.get(url)
        assert len(response.json()['results']) == 1

        url = resolve_url('transport-detail',
                          uuid=new_uuid)
        response = client.get(url)
        assert response.json()['uuid'] == new_uuid
