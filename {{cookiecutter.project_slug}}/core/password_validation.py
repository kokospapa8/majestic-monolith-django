from django.core.exceptions import (
    ValidationError,
)

from django.utils.translation import gettext as _, ngettext


class MaximumLengthValidator:
    """
    Validate whether the password is of a minimum length.
    """

    def __init__(self, max_length=16):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                ngettext(
                    "This password is too long. It must contain less than %(max_length)d character.",
                    "This password is too long. It must contain less than %(max_length)d characters.",
                    self.max_length
                ),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain less than %(min_length)d character.",
            "Your password must contain less than %(min_length)d characters.",
            self.max_length
        ) % {'min_length': self.max_length}


class AlphaNumericPasswordValidator:
    """
    Validate whether the password is alphanumeric.
    """

    def validate(self, password, user=None):
        if not password.isalnum():
            raise ValidationError(
                _("This password must be alphanumeric."),
                code='password_not_alphanumeric',
            )

    def get_help_text(self):
        return _("Your password must be alphanumeric.")
