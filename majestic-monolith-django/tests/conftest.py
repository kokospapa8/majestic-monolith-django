import json
import os

import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.management import call_command
from rest_framework.test import APIRequestFactory
from rest_framework_extensions.test import APIClient
from django import setup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CustomUser = get_user_model()


def pytest_configure():
    setup(set_prefix=False)
    cache.clear()


class CustomClient(APIClient):
    def request(self, **request):
        # for drf-extensions cache_response
        response = super().request(**request)
        if not hasattr(response, 'data'):
            response.data = json.loads(response.content.decode('utf-8'))
        return response


@pytest.fixture(name='rf')
def request_factory():
    return APIRequestFactory()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        for app in ['auth',
                    'user',
                    'distribution',
                    'shipping'
                    ]:
            dir_path = os.path.join(BASE_DIR, f'tests/fixtures/{app}')
            files = os.listdir(dir_path)
            for file in files:
                print(app, file)
                call_command("loaddata", f"tests/fixtures/{app}/{file}")


# make xdist processes to use same database
@pytest.fixture(scope="session")
def django_db_modify_db_settings():
    pass


@pytest.fixture
def user_1(db):
    user = CustomUser.objects.get(pk=1)
    user.raw_password = 'password'
    EmailAddress.objects.get_or_create(user=user, email=user.email, verified=True)
    user.save()
    return user


@pytest.fixture
def staff_user():
    user = CustomUser.objects.get(pk=2)
    return user


@pytest.fixture
def unregistered_user(db):
    user = CustomUser.objects.create(is_active=False)
    return user


@pytest.fixture
def force_login_client():
    def _force_login_user(user):
        client = CustomClient()
        client.force_login(user)
        return client

    return _force_login_user


@pytest.fixture
def phonenumbers():
    return {
        "verified": "+821012341233",
        "not_verified": "+821012341232",
        "user_1": "+821012345555",
        "no_user": "+821011111111",
        "banned": "+821099999999",
        "new_user": "+821012349998"
    }
