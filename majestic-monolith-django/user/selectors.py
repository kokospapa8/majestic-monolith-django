from dataclasses import dataclass
from typing import Union, List

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from core.selector import Selector


from .models import CustomUser, UserHuman, UserOrc, UserGod

User = get_user_model()

@dataclass
class UserDTO:
    user: CustomUser


class UserSelector(Selector):

    @staticmethod
    def get_active_user_by_type(type: str) -> \
            Union[QuerySet, List[CustomUser]]:
        return CustomUser.objects.filter(is_active=True, type=type)


user_selector = UserSelector()
