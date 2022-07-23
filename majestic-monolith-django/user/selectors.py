from dataclasses import dataclass
from typing import List, Union

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from core.selector import Selector

from .models import CustomUser

User = get_user_model()


@dataclass
class UserDTO:
    user: CustomUser


class UserSelector(Selector):
    @staticmethod
    def get_active_user_by_type(user_type: str) -> Union[QuerySet, List[CustomUser]]:
        return CustomUser.objects.filter(is_active=True, type=user_type)

    @staticmethod
    def filter_users_by_phonenumber(phonenumber) -> list:
        users = list(User.objects.filter(phonenumber=phonenumber))
        return list(set(users))


user_selector = UserSelector()
