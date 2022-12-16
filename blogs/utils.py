from io import BytesIO

from PIL import Image
from django.conf import settings
from django.core.files import File


def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, format=im.format, quality=settings.IMAGE_COMPRESSION_QUALITY, optimize=True)
    compressed_image = File(im_io, name=image.name)
    return compressed_image
