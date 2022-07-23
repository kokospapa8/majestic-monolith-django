import pytest
from django.shortcuts import resolve_url
from rest_framework import status

from tests.conftest import CustomClient
from tests.schemas.user_schemas import user_profile_schema


@pytest.mark.django_db
class TestUserRiderProfile:
    schema = user_profile_schema

    def test_user_rider_profile_get_unauthorized(self, client):
        url = resolve_url("user_self")
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_profile_get(self, userprofile_user_pk2):
        url = resolve_url("user_self")
        client = CustomClient()
        client.force_login(userprofile_user_pk2.user)
        response = client.get(url)
        # print(response.json())
        assert response.status_code == status.HTTP_200_OK

        response_up = response.json()
        assert response_up["uuid"] == str(userprofile_user_pk2.user.uuid)
        assert response_up["fullname"] == userprofile_user_pk2.fullname
        assert response_up["phonenumber"] == str(userprofile_user_pk2.user.phonenumber)
        assert response_up["type"] == str(userprofile_user_pk2.user.type)
        assert self.schema.is_valid(response.json())

    def test_user_profile_patch_fullname(self, userprofile_user_pk2):
        url = resolve_url("user_self")
        client = CustomClient()
        client.force_login(userprofile_user_pk2.user)
        new_fullname = "staff_fullname_1234"
        response = client.patch(url, {"fullname": new_fullname})

        assert response.status_code == status.HTTP_200_OK
        response_up = response.json()
        assert response_up["fullname"] == new_fullname

    def test_user_profile_patch_username_not_changed(self, userprofile_user_pk2):
        url = resolve_url("user_self")
        client = CustomClient()
        client.force_login(userprofile_user_pk2.user)
        response = client.patch(url, {"username": "new_username"})

        assert response.status_code == status.HTTP_200_OK
        response_up = response.json()
        assert response_up["username"] == str(userprofile_user_pk2.user.username)
