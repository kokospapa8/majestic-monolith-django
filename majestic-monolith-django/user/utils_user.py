from django.contrib.auth import get_user_model

from .models import UserGod, UserOrc, UserHuman, \
    UserProfileGod, UserProfileHuman, UserProfileOrc
from .serializers import UserProfileGodSerializer, \
    UserProfileHumanSerializer, UserProfileOrcSerializer

CustomUser = get_user_model()


# TODO: use match-case for python 3.10 - https://www.python.org/dev/peps/pep-0634/
def get_proxy_user_model(user):
    if user.type == CustomUser.Types.GOD:
        return UserGod
    if user.type == CustomUser.Types.HUMAN:
        return UserHuman
    if user.type == CustomUser.Types.ORC:
        return UserOrc


def get_proxy_userprofile_model(user):
    if user.type == CustomUser.Types.GOD:
        return UserProfileGod
    if user.type == CustomUser.Types.HUMAN:
        return UserProfileHuman
    if user.type == CustomUser.Types.ORC:
        return UserProfileOrc


def get_proxy_userprofile_serializer(user):
    if user.type == CustomUser.Types.GOD:
        return UserProfileGodSerializer
    if user.type == CustomUser.Types.HUMAN:
        return UserProfileHumanSerializer
    if user.type == CustomUser.Types.ORC:
        return UserProfileOrcSerializer


def delete_user_profile_cache(uuid):
    from user.caches import UserProfileCache
    UserProfileCache().delete(uuid)

