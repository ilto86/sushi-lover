from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


class ImageSizeValidator:
    MAX_IMAGE_WIDTH = 1024
    MAX_IMAGE_HEIGHT = 768

    @classmethod
    def image_size_validator(cls, image):
        width, height = get_image_dimensions(image)

        if cls.MAX_IMAGE_WIDTH < width or cls.MAX_IMAGE_HEIGHT < height:
            raise ValidationError('Image size is larger than what is allowed.')