from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _("%(value)s is not an even number"),
            params={"value": value},
        )
    
def validate_full_string(value):
    if len(value) <= 1:
        raise ValidationError(
            _("%(value) is not supported, please correct it"),
            params={"value": value},
        )