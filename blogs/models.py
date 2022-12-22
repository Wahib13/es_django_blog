import random
import string
import uuid

from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.conf import settings

from blogs.utils import compress


class Author(models.Model):
    uuid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    name = models.CharField(
        max_length=30,
        db_index=True
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ("name",)


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
    slug = models.SlugField(blank=True, null=False, max_length=255, db_index=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            char = "".join((random.sample(string.ascii_lowercase, 5)))
            self.slug = slugify(self.name + "-" + char)
        return super().save(*args, **kwargs)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "Draft"
        PUBLISHED = "Published"

    slug = models.SlugField(blank=True, null=False, max_length=255, db_index=True, editable=False)
    status = models.CharField(
        max_length=9, choices=Status.choices, default=Status.DRAFT
    )
    title = models.CharField(max_length=255, db_index=True)
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    banner = models.ImageField(blank=True, null=True)
    body = models.TextField(blank=False, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)

    categories = models.ManyToManyField(Category, blank=True, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ("created_at",)

    def save(self, *args, **kwargs):
        if not self.slug:
            char = "".join((random.sample(string.ascii_lowercase, 5)))
            self.slug = slugify(self.title + "-" + char)
        return super().save(*args, **kwargs)


class PostImage(models.Model):

    def __init__(self, *args, **kwargs):
        super(PostImage, self).__init__(*args, **kwargs)
        self._image = self.image

    uuid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, )

    def save(self, *args, **kwargs):
        if self.image and self._image != self.image:
            self.image = compress(self.image)

        super(PostImage, self).save(*args, **kwargs)
