import uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    PermissionsMixin,
    UserManager
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.fields import ThumbnailerImageField
from core.utils import UserPathAndRename

from phonenumber_field.modelfields import PhoneNumberField

from .managers import StaffManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        STAFF = "STAFF", "Staff"

    base_type = Types.STAFF

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    phonenumber = PhoneNumberField(unique=True, blank=False, db_index=True, null=True)
    phonenumber_meta = models.CharField(max_length=32, blank=True, db_index=True, help_text="Flag for banned user")

    username = models.CharField(
        _("username"),
        blank=True,
        default="",
        max_length=15,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={"unique": _("A user with that username already exists.")},
    )

    type = models.CharField("Type", max_length=10,
                            choices=Types.choices, default=Types.STAFF)

    email = models.EmailField(_("email address"), blank=True, unique=False, null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    banned = models.BooleanField(default=False, db_index=True)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    locale = models.CharField(max_length=10, default="en", blank=False)

    date_unregistered = models.DateTimeField(null=True, default=None)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phonenumber"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        app_label = "user"
        db_table = "auth_user"
        ordering = ["-id"]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def save(self, *args, **kwargs):
        if not self.type and not self.pk:
            self.type = self.base_type

        instance = super().save(*args, **kwargs)
        return instance

    def __str__(self):
        return f"[{self.type}]{self.username}"

    def _uuid(self):
        return self.uuid

    def phonenumber_national_str(self):
        return f"0{self.phonenumber.national_number}"


class UserStaff(CustomUser):
    base_type = CustomUser.Types.STAFF
    objects = StaffManager()

    class Meta:
        proxy = True

    @property
    def profile(self):
        return self.userprofilestaff


class UserProfileStaff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
    fullname = models.CharField(
        max_length=settings.USERPROFILE_FULLNAME_MAX_LENGTH,
        blank=True, default=""
    )
    image = ThumbnailerImageField(
        upload_to=UserPathAndRename("images/user/staff/"))

    class Meta:
        app_label = "user"
        db_table = "user_profile_staff"

    def __str__(self):
        return f"[Staff]{self.user.username} - {self.fullname}"
