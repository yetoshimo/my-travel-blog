from django.core.exceptions import ValidationError


def validate_name(name):
    if not name.isalpha():
        raise ValidationError('Text must contain only letters!')
    if len(name) < 2:
        raise ValidationError(f'Ensure this value has at least 2 characters (it has {len(name)}).')
