# -*- coding: utf-8 -*-
import logging

from allauth.account.adapter import get_adapter
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from auth.caches import PhonenumberVerificationCache

from .models import PhonenumberCheck, PhonenumberVerificationLog
from .utils_auth import bypass_token_request, is_banned_phonenumber

CustomUser = get_user_model()
logger = logging.getLogger("django.eventlogger")


# checks if user exists
class PhonenumberCheckSerializer(serializers.Serializer):
    phonenumber = PhoneNumberField(help_text="Must be in E164 format")

    def validate_phonenumber(self, attrs):
        if is_banned_phonenumber(attrs):
            raise serializers.ValidationError(_("This phonenumber is banned."))
        return attrs


class BaseSignupSerializer(serializers.Serializer):
    phonenumber = PhoneNumberField(help_text="Must be in E164 format")
    user_type = serializers.ChoiceField(choices=CustomUser.Types.choices)

    def validate_phonenumber(self, phonenumber):
        if bypass_token_request(str(phonenumber)):
            return phonenumber

        # check phonenumber exist
        if CustomUser.objects.filter(phonenumber=phonenumber).exists():
            raise serializers.ValidationError(_("phonenumber already exists."))

        # if is_banned_phonenumber(phonenumber):
        #     raise serializers.ValidationError("This number is permanently banned.")

        return phonenumber


class SignupSerializer(BaseSignupSerializer):
    def create_profile(self, request, user):
        user.profile.fullname = self.validated_data.get("fullname", "")
        if user.type == CustomUser.Types.DRIVER:
            user.profile.dob = self.validated_data.get("dob", None)
        user.profile.save()

    def save(self, request):
        user_type = self.validated_data.get("user_type", CustomUser.Types.STAFF)
        adapter = get_adapter()
        user = adapter.new_user(request, user_type=user_type)
        adapter.save_user(request, user, self.validated_data)
        self.create_profile(request, user)

        # import other domain module
        from user.events import UserEventsEmitter

        UserEventsEmitter().user_signup(user.uuid.hex)

        return user


class TokenObtainPairFromUserSerializer(serializers.Serializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = {}
        refresh = self.get_token(self.context["user"])
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class SignupTokenRequestSerializer(serializers.Serializer):
    phonenumber = PhoneNumberField()

    def validate_phonenumber(self, attrs):
        # check phone number exist
        if CustomUser.objects.filter(phonenumber=attrs).exists():
            raise serializers.ValidationError(_("phonenumber already exists."))

        if is_banned_phonenumber(attrs):
            raise serializers.ValidationError(_("This number is permanently banned."))
        return attrs


class SignupTokenConfirmSerializer(PhonenumberCheckSerializer):
    phonenumber = PhoneNumberField(required=True)
    token = serializers.CharField(
        max_length=settings.PHONENUMBER_VERIFICATION_TOKEN_LENGTH, required=True
    )

    def validate_phonenumber(self, attrs):
        if bypass_token_request(str(attrs)):
            return attrs

        if not PhonenumberCheck.objects.filter(
            phonenumber=attrs, verified=True
        ).exists():
            raise serializers.ValidationError(
                _("phonenumber verification has not been sent.")
            )

        return attrs


class SigninTokenRequestSerializer(serializers.Serializer):
    phonenumber = PhoneNumberField()

    def validate_phonenumber(self, attrs):
        # check phone number exist
        if not CustomUser.objects.filter(phonenumber=attrs).exists():
            raise serializers.ValidationError(_("phonenumber does not exists."))

        if is_banned_phonenumber(attrs):
            raise serializers.ValidationError("This number is permanently banned.")
        return attrs


class SigninTokenConfirmSerializer(LoginSerializer):
    username = None
    email = None
    phonenumber = PhoneNumberField()
    token = serializers.CharField(max_length=4)
    password = None

    def verify_token(self, phonenumber, token):
        if bypass_token_request(str(phonenumber)):
            return True
        phonenumber_check = PhonenumberCheck.objects.get(phonenumber=phonenumber)
        if phonenumber_check.is_expired():
            raise serializers.ValidationError(_("phonenumber check expired."))
        if phonenumber_check.confirm_verification(token):
            PhonenumberVerificationCache().delete(str(phonenumber))
            return True
        return False

    def validate_phonenumber(self, phonenumber):
        if bypass_token_request(str(phonenumber)):
            return phonenumber
        if not PhonenumberCheck.objects.filter(
            phonenumber=phonenumber, verified=False
        ).exists():
            raise serializers.ValidationError(
                _("phonenumber verification has not been sent.")
            )
        return phonenumber

    def validate(self, attrs):
        phonenumber = attrs.get("phonenumber")
        token = attrs.get("token")
        is_verified = self.verify_token(phonenumber, token)
        PhonenumberVerificationLog.objects.create(
            phonenumber=phonenumber,
            type=PhonenumberVerificationLog.VerificationType.SIGNIN,
            success=is_verified,
        )

        user = self.authenticate(
            phonenumber=phonenumber, verification_success=is_verified
        )

        attrs["user"] = user
        attrs["is_verified"] = is_verified
        return attrs


class SigninSerializer(LoginSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(style={"input_type": "password"})


class SignoutTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField(help_text="refresh_token")

    def validate(self, attrs):
        refresh = RefreshToken(attrs["refresh"])

        data = {"access": str(refresh.access_token)}
        if (
            api_settings.BLACKLIST_AFTER_ROTATION
            and "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS
        ):
            # try:
            # Attempt to blacklist the given refresh token
            refresh.blacklist()
            # except Exception as e:
            #     # If blacklist app not installed, `blacklist` method will
            #     # not be present
            #     pass

        return data


class TokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True, help_text="Access token.")
    refresh = serializers.CharField(read_only=True, help_text="Refresh token.")


class TokenHeartbeatResponseSerializer(serializers.Serializer):
    delete_count = serializers.ListField(help_text="How many tokens were deleted.")


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True, help_text="Access token.")


class TimestampExpiresResponseSerializer(serializers.Serializer):
    timestamp_expires = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S.%fZ",
        read_only=True,
        help_text="Timestamp when the token expires.",
    )
