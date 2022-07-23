from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameNumberonlyValidator(validators.RegexValidator):
    regex = r"^[0-9]*$"
    message = _(
        "Enter a valid username. This value may contain only number letters, "
        "numbers, and _ characters."
    )


@deconstructible
class UsernameStaffValidator(validators.RegexValidator):
    regex = r"^[\w]*$"
    message = _(
        "Enter a valid username. This value may contain only ascii english letters, "
        "numbers, and _ characters."
    )
