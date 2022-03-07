# -*- coding: utf-8 -*-
import logging

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field, user_username
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from user.utils_user import get_proxy_userprofile_model

CustomUser = get_user_model()
logger = logging.getLogger("django.eventlogger")


class AuthAccountAdapter(DefaultAccountAdapter):

    def new_user(self, request, user_type=CustomUser.Types.STAFF):
        """
        Instantiates a new User instance.
        staff is default user type
        """

        from user.models import UserStaff
        user = UserStaff()

        if user_type == CustomUser.Types.STAFF:
            from user.models import UserStaff
            user = UserStaff()
        if user_type == CustomUser.Types.DRIVER:
            from user.models import UserDriver
            user = UserDriver()

        return user

    def save_user(self, request, user, data, commit=True):
        phonenumber = data.get("phonenumber")
        username = data.get("username", None)

        # convert phonenumber to username (this is unique)
        try:
            # username = f"0{phonenumber.national_number}"
            username = phonenumber.phonenumber.replace('+', '')

        except Exception as e:
            logger.debug(f"{phonenumber} national error: {e}")
            username = str(phonenumber)

        # user_email(user, email)
        user_username(user, username)
        user.phonenumber = phonenumber

        if settings.ENV in ["dev", "dev", "local"]:
            user.set_password("12341234")
        else:
            user.set_unusable_password()
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()

            # create profile on new user
            proxy_profile = get_proxy_userprofile_model(user)
            profile, created = proxy_profile.objects.select_related('user') \
                .get_or_create(user__uuid=user.uuid, defaults={'user': user})

        return user
