from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


class ImageSizeValidator:
    # Profile image size: 1280; Blog image size: 1200; Background image size: 1920
    MAX_IMAGE_WIDTH = 1024

    # Profile image size:  720; Blog image size:  630; Background image size: 1080
    MAX_IMAGE_HEIGHT = 768

    @classmethod
    def image_size_validator(cls, image):
        width, height = get_image_dimensions(image)

        if cls.MAX_IMAGE_WIDTH < width or cls.MAX_IMAGE_HEIGHT < height:
            raise ValidationError('Image size is larger than what is allowed.')