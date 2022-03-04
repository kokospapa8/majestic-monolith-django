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

from .managers import GodManager, HumanManager, OrcManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        GOD = "GOD", "God"
        HUMAN = "HUMAN", "Human"
        ORC = "ORC", "Orc"

    base_type = Types.HUMAN

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
                            choices=Types.choices, default=Types.HUMAN)

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

        if instance and instance.is_active:
            from .utils_user import get_proxy_userprofile_model
            proxy_profile = get_proxy_userprofile_model(self)
            profile, created = proxy_profile.objects.select_related('user') \
                .get_or_create(user__uuid=self.uuid, defaults={'user': self})

        return instance

    def __str__(self):
        return f"[{self.type}]{self.username}"

    def _uuid(self):
        return self.uuid

    def phonenumber_national_str(self):
        return f"0{self.phonenumber.national_number}"


class UserGod(CustomUser):
    base_type = CustomUser.Types.God
    objects = GodManager()

    class Meta:
        proxy = True

    @property
    def profile(self):
        return self.userprofilegod


class UserHuman(CustomUser):
    base_type = CustomUser.Types.HUMAN
    objects = HumanManager()

    class Meta:
        proxy = True

    @property
    def profile(self):
        return self.userprofilehuman


class UserOrc(CustomUser):
    base_type = CustomUser.Types.ORC
    objects = OrcManager()

    class Meta:
        proxy = True

    @property
    def profile(self):
        return self.userprofileorc


class UserProfileGod(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
    fullname = models.CharField(
        max_length=settings.USERPROFILE_FULLNAME_MAX_LENGTH,
        blank=True, default=""
    )
    image = ThumbnailerImageField(
        upload_to=UserPathAndRename("images/user/god/"))

    class Meta:
        app_label = "user"
        db_table = "user_profile_god"

    def __str__(self):
        return f"[GOD]{self.user.username} - {self.fullname}"


class UserProfileHuman(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
    fullname = models.CharField(
        max_length=settings.USERPROFILE_FULLNAME_MAX_LENGTH,
        blank=True, default=""
    )
    dob = models.DateField(blank=True, null=True, default=None)
    image = ThumbnailerImageField(
        upload_to=UserPathAndRename("images/user/human/"))

    class Meta:
        app_label = "user"
        db_table = "user_profile_human"

    def __str__(self):
        return f"[Human]{self.user.username} - {self.fullname}"


class UserProfileOrc(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
    fullname = models.CharField(
        max_length=settings.USERPROFILE_FULLNAME_MAX_LENGTH,
        blank=True, default=""
    )
    dob = models.DateField(blank=True, null=True, default=None)
    image = ThumbnailerImageField(
        upload_to=UserPathAndRename("images/user/orc/"))

    class Meta:
        app_label = "user"
        db_table = "user_profile_orc"

    def __str__(self):
        return f"[Orc]{self.user.username} - {self.fullname}"
