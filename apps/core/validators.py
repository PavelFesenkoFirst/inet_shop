from django.core.exceptions import ValidationError


def name_validator(value):
    if value == 'admin':
        raise ValidationError(
            '%(value)s invalid name', params={'value': value}
        )
