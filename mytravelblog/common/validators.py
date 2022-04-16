from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageSizeInMBValidator:
    def __init__(self, max_size_in_mb):
        self.max_size_in_mb = max_size_in_mb

    def __call__(self, value, *args, **kwargs):
        if value and not hasattr(value, 'url'):
            filesize = value.size
            if filesize > self.__megabytes_to_bytes(self.max_size_in_mb):
                raise ValidationError(self.__get_exception_message())

    @staticmethod
    def __megabytes_to_bytes(value):
        return value * 1024 * 1024

    def __get_exception_message(self):
        return f"Max file size is {self.max_size_in_mb:.2f} MB"


def validate_file_content_type(field_name, file_content_type):
    if file_content_type != 'image/jpeg' and file_content_type != 'image/png':
        raise ValidationError({
            f'{field_name}': 'Please select an image file!'
        })
