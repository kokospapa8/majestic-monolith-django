from django.contrib.auth import get_user_model

from .models import UserStaff, \
    UserProfileStaff
from .serializers import \
    UserProfileStaffSerializer

CustomUser = get_user_model()


# TODO: use match-case for python 3.10 - https://www.python.org/dev/peps/pep-0634/
def get_proxy_user_model(user):
    if user.type == CustomUser.Types.STAFF:
        return UserStaff


def get_proxy_userprofile_model(user):
    if user.type == CustomUser.Types.STAFF:
        return UserProfileStaff


def get_proxy_userprofile_serializer(user):
    if user.type == CustomUser.Types.STAFF:
        return UserProfileStaffSerializer


def delete_user_profile_cache(uuid):
    from user.caches import UserProfileCache
    UserProfileCache().delete(uuid)

