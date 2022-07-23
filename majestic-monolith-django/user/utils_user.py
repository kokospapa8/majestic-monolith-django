from django.contrib.auth import get_user_model

from .models import UserDriver, UserProfileDriver, UserProfileStaff, UserStaff
from .serializers import UserProfileDriverSerializer, UserProfileStaffSerializer

CustomUser = get_user_model()


# TODO: use match-case for python 3.10 - https://www.python.org/dev/peps/pep-0634/
def get_proxy_user_model(user):
    if user.type == CustomUser.Types.STAFF:
        return UserStaff
    if user.type == CustomUser.Types.DRIVER:
        return UserDriver


def get_proxy_userprofile_model(user):
    if user.type == CustomUser.Types.STAFF:
        return UserProfileStaff
    if user.type == CustomUser.Types.DRIVER:
        return UserProfileDriver


def get_proxy_userprofile_serializer(user):
    if user.type == CustomUser.Types.STAFF:
        return UserProfileStaffSerializer
    if user.type == CustomUser.Types.DRIVER:
        return UserProfileDriverSerializer


def delete_user_profile_cache(uuid):
    from user.caches import UserProfileCache

    UserProfileCache().delete(uuid)
