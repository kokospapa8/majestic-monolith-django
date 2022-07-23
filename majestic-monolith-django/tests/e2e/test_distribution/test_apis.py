import pytest
from django.apps import apps
from django.shortcuts import resolve_url
from rest_framework import status

from tests.conftest import CustomClient
from tests.schemas.distribution_schemas import center_schema

DistributionCenter = apps.get_model("distribution", "DistributionCenter")


@pytest.mark.django_db
class TestDistributionViewSet:
    # test CRUD

    def test_distribution_list_unauthorized(self, client):
        url = resolve_url("center-list")
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_distribution_list_initial(self, staff_user):
        url = resolve_url("center-list")
        client = CustomClient()
        client.force_login(staff_user)
        response = client.get(url)
        assert len(response.json()["results"]) == 2

    def test_distribution_create(self, staff_user, new_center_param):
        url = resolve_url("center-list")
        client = CustomClient()
        client.force_login(staff_user)
        response = client.post(
            url,
            {
                "name": new_center_param["name"],
                "center_code": new_center_param["center_code"],
            },
        )
        assert center_schema.is_valid(response.json())

        assert response.json()["name"] == new_center_param["name"]
        assert response.json()["center_code"] == new_center_param["center_code"]
        uuid = response.json()["uuid"]

        url = resolve_url("center-list")
        response = client.get(url)
        assert len(response.json()["results"]) == 3

        url = resolve_url("center-detail", uuid=uuid)
        response = client.get(url)
        assert response.json()["uuid"] == uuid

    def test_distribution_create_same_code(self, staff_user, existing_center):
        url = resolve_url("center-list")
        client = CustomClient()
        client.force_login(staff_user)
        response = client.post(
            url, {"name": "randomname", "center_code": existing_center["center_code"]}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_distribution_patch(self, staff_user, existing_center):
        url = resolve_url("center-detail", uuid=existing_center["uuid"])
        client = CustomClient()
        client.force_login(staff_user)
        new_name = "new_name"
        response = client.patch(url, {"name": new_name})
        # print(response.json())
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == new_name
