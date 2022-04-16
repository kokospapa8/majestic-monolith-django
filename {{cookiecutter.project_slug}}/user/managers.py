from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager


class StaffManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        # need to import user here since
        # this module is imported before the model
        CustomUser = get_user_model()
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=CustomUser.Types.STAFF)
