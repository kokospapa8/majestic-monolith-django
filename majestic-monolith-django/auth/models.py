# -*- coding: utf-8 -*-
import datetime
from random import randint

from django.conf import settings
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from .events import AuthEventsEmitter


class PhonenumberCheck(models.Model):
    phonenumber = PhoneNumberField(unique=True, blank=False)
    verified = models.BooleanField(default=False, db_index=True)
    timestamp_requested = models.DateTimeField(auto_now_add=True)
    timestamp_verified = models.DateTimeField(null=True)
    token = models.CharField(
        max_length=settings.PHONENUMBER_VERIFICATION_TOKEN_LENGTH, null=True
    )

    class Meta:
        app_label = "mmd_auth"
        db_table = "mmd_auth_phonenumber_check"

    def attempt_verification(self):
        # generate token
        token = "1234" if settings.ENV not in ["prod"] else randint(1000, 10000)

        # send verification code using event emitter
        # TODO: logic needs to be implemented in AWS using lambda
        AuthEventsEmitter().send_verification_code(token, str(self.phonenumber))

        self.timestamp_requested = timezone.now()
        self.token = token
        self.verified = False
        self.save()

        from auth.caches import PhonenumberVerificationCache

        PhonenumberVerificationCache().incr(str(self.phonenumber))

    def confirm_verification(self, token):
        if self.token == token:
            self.verified = True
            self.timestamp_verified = timezone.now()
            self.save()
            return True
        return False

    def is_expired(self):
        return self.get_expiration_time() < timezone.now()

    def get_expiration_time(self):
        return self.timestamp_requested + datetime.timedelta(
            minutes=settings.PHONENUMBER_EXPIRATION
        )

    def __str__(self):
        return f"{self.phonenumber}: verified: {self.verified}"


class PhonenumberVerificationLog(models.Model):
    class VerificationType(models.TextChoices):
        SIGNIN = "I", "Signin"
        SIGNUP = "U", "Signup"

    phonenumber = PhoneNumberField()
    type = models.CharField(choices=VerificationType.choices, max_length=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(null=True, help_text="null if request")

    class Meta:
        app_label = "mmd_auth"
        db_table = "mmd_auth_phonenumber_verification_log"


class AllowedPhonenumbers(models.Model):
    phonenumber = models.CharField(max_length=32, help_text="bypass phonenumber")
    description = models.CharField(max_length=32, help_text="name")

    class Meta:
        app_label = "mmd_auth"
        db_table = "mmd_auth_allowed_phonenumbers"
