from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.core.files.images import get_image_dimensions
from django.utils.translation import gettext_lazy as _

from painless.helper.typing import Byte


@deconstructible
class DimensionValidator(BaseValidator):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __call__(self, value):
        pic = value.file.open()
        width, height = get_image_dimensions(pic)
        if not (width == self.width and height == self.height):
            raise ValidationError(
                _(f'Expected dimension is: [{self.width}w, {self.height}h] but actual is: [{width}w, {height}h]'))  # noqa


@deconstructible
class ImageSizeValidator(BaseValidator):
    def __init__(self, limit_size: Byte):
        self.limit_size = limit_size

    def __call__(self, value):
        if value.size > self.limit_size:
            raise ValidationError(f'Please upload file lower than one Megabyte.')  # noqa


@deconstructible
class SquareDimensionValidator(object):
    def __init__(self):
        pass

    def __call__(self, value):
        pic = value
        width, height = get_image_dimensions(pic)

        if not (width == height):
            raise ValidationError(
                _(f'Width and Height must '
                  f'be the same but entered [{width}w, {height}h]'))
