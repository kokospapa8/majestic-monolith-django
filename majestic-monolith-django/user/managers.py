from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager

CustomUser = get_user_model()


class GodManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=CustomUser.Types.GOD)


class HumanManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        CustomUser = get_user_model()
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=CustomUser.Types.HUMAN)


class OrcManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        CustomUser = get_user_model()
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=CustomUser.Types.ORC)
