from django.core.exceptions import ValidationError


def validate_first_name(first_name):
    if not first_name.isalpha():
        raise ValidationError(
            {'first_name': 'Text must contain only letters!'})


def validate_first_name_length(first_name):
    if len(first_name) < 2:
        raise ValidationError(
            {'first_name': f'Ensure this value has at least 2 characters (it has {len(first_name)}).'})


def validate_last_name(last_name):
    if not last_name.isalpha():
        raise ValidationError({
            'last_name': 'Text must contain only letters!'})


def validate_last_name_length(last_name):
    if len(last_name) < 2:
        raise ValidationError({
            'last_name': f'Ensure this value has at least 2 characters (it has {len(last_name)}).'})
