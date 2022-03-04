from dataclasses import dataclass

from core.utils import tokey
from core.services import Service

from .utils_user import get_proxy_userprofile_model
from .events import UserEventsEmitter
from .models import UserProfileGod, UserProfileOrc, \
    UserProfileHuman, CustomUser


@dataclass
class UserDTO:
    user: CustomUser


class UserService(Service):
    dto: UserDTO

    def _delete_user_info(self):

        UserProfileGod.objects.filter(user=self).delete()
        UserProfileOrc.objects.filter(user=self).delete()
        UserProfileHuman.objects.filter(user=self).delete()

        from auth.models import PhonenumberCheck, PhonenumberVerificationLog
        PhonenumberCheck.objects.filter(phonenumber=self.phonenumber).delete()
        PhonenumberVerificationLog.objects.filter(phonenumber=self.phonenumber).delete()

        self.username = f"!@#{self.id}-{self.username}"[:15]
        self.email = None
        self.is_active = False
        self.set_unusable_password()

    @staticmethod
    def ban(user):
        user._delete_user_info()
        if user.phonenumber:
            user.phonenumber_meta = tokey(
                user.phonenumber.country_code, user.phonenumber.national_number)
        user.phonenumber = None
        user.banned = True
        user.save()

        from user.events import UserEventsEmitter
        UserEventsEmitter().user_banned(user.uuid)

    @staticmethod
    def unregister(user):
        user._delete_user_info()
        user.phonenumber = None
        user.phonenumber_meta = ""
        user.save()

        from user.events import UserEventsEmitter
        UserEventsEmitter().user_deactivated(user.uuid)


user_service = UserService()


