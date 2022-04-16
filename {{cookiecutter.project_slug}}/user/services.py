from dataclasses import dataclass

from django.contrib.auth import get_user_model

from core.utils import tokey
from core.services import Service

from .utils_user import get_proxy_userprofile_model
from .events import UserEventsEmitter
from .models import UserProfileStaff

User = get_user_model()


@dataclass
class UserDTO:
    user: User


class UserDeleteService(Service):
    dto: UserDTO

    def _delete_user_info(self, user) -> User:

        # might have profile for different user type
        UserProfileStaff.objects.filter(user=user).delete()

        # import inline for other module in different domain
        from auth.models import PhonenumberCheck, PhonenumberVerificationLog
        PhonenumberCheck.objects.filter(phonenumber=user.phonenumber).delete()
        PhonenumberVerificationLog.objects.filter(phonenumber=user.phonenumber).delete()

        user.username = f"!@#{user.id}-{user.username}"[:15]
        user.email = None
        user.is_active = False
        user.set_unusable_password()
        return user

    def ban(self) -> None:
        user = self.dto.user

        user = self._delete_user_info(user)
        if user.phonenumber:
            user.phonenumber_meta = tokey(
                user.phonenumber.country_code, user.phonenumber.national_number)
        user.phonenumber = None
        user.banned = True
        user.save()

        UserEventsEmitter().user_banned(user.uuid.hex)

    def unregister(self) -> None:
        user = self.dto.user

        user = self._delete_user_info(user)
        user.phonenumber = None
        user.phonenumber_meta = ""
        user.save()

        UserEventsEmitter().user_deactivated(user.uuid.hex)


user_service_delete = UserDeleteService()


