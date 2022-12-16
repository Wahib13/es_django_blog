import random
import string

from django.db import models
import uuid
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.template.defaultfilters import slugify


class Category(MPTTModel):
    uuid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    name = models.CharField(max_length=250, unique=True)
    parent = TreeForeignKey("self", blank=True, null=True, on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    icon = models.FileField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=False, max_length=255, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            char = "".join((random.sample(string.ascii_lowercase, 5)))
            self.slug = slugify(self.name + "-" + char)
        return super().save(*args, **kwargs)
