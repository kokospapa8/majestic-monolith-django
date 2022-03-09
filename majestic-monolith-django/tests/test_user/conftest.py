import pytest
from django.contrib.auth import get_user_model
from user.utils_user import get_proxy_userprofile_model
CustomUser = get_user_model()


@pytest.fixture
def userprofile_user_pk2():

    user = CustomUser.objects.get(pk=2)
    return get_proxy_userprofile_model(user).objects.get(user=user)
