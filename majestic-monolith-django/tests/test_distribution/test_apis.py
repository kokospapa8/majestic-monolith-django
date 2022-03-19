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

from tests.schemas.distribution_schemas import center_schema
DistributionCenter = apps.get_model('distribution', 'DistributionCenter')


@pytest.mark.django_db
class TestDistributionViewSet:
    # test CRUD

    def test_user_rider_profile_get_unauthorized(self, client):
        url = resolve_url('center-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_distribution_list_empty(self, staff_user):
        url = resolve_url('center-list')
        client = CustomClient()
        client.force_login(staff_user)
        response = client.get(url)
        assert len(response.json()['results']) == 1

    def test_distribution_create(self, staff_user, new_center_param):
        url = resolve_url('center-list')
        client = CustomClient()
        client.force_login(staff_user)
        response = client.post(url, {
            "name": new_center_param['name'],
            "center_code": new_center_param['center_code']
        })
        assert center_schema.is_valid(response.json())

        assert response.json()['name'] == new_center_param['name']
        assert response.json()['center_code'] == new_center_param['center_code']
        uuid = response.json()['uuid']

        url = resolve_url('center-list')
        response = client.get(url)
        assert len(response.json()['results']) == 2

        url = resolve_url('center-detail', uuid=uuid)
        response = client.get(url)
        assert response.json()['uuid'] == uuid

    def test_distribution_create_same_code(self,
                                           staff_user, existing_center):
        url = resolve_url('center-list')
        client = CustomClient()
        client.force_login(staff_user)
        response = client.post(url, {
            "name": "randomname",
            "center_code": existing_center['center_code']
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_distribution_patch(self, staff_user, existing_center):
        url = resolve_url('center-detail', uuid=existing_center['uuid'])
        client = CustomClient()
        client.force_login(staff_user)
        new_name = "new_name"
        response = client.patch(url, {
            "name": new_name
        })
        print(response.json())
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['name'] == new_name
