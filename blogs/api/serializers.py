from mptt.exceptions import InvalidMove
from rest_framework import serializers
from rest_framework import status
from django.apps import apps
from django.conf import settings
from rest_framework.response import Response

from blogs.models import Category, Post, PostImage, Author, Tag


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.UUIDField(
        source="parent.uuid",
        allow_null=True,
        default=None,
    )

    class Meta:
        model = Category
        fields = (
            "uuid",
            "name",
            "description",
            "parent",
            "image",
            "icon",
        )

    @classmethod
    def create_or_update_parent(cls, instance, parent_uuid):
        try:
            if parent_uuid:
                parent = cls.Meta.model.objects.get(uuid=parent_uuid.get("uuid"))
                instance.parent = parent
                instance.save()
            return instance
        except cls.Meta.model.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": "parent category does not exist"}
            )
        except InvalidMove:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "category may not be a child of itself"}
            )

    def create(self, validated_data):
        parent_uuid = validated_data.pop("parent")
        category = super().create(validated_data)
        return self.__class__.create_or_update_parent(category, parent_uuid)

    def update(self, instance, validated_data):
        parent_uuid = validated_data.pop("parent")
        category = super().update(instance, validated_data)
        return self.__class__.create_or_update_parent(category, parent_uuid)


class PostCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Category
        fields = ('name', 'uuid',)


class PostTagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Category
        fields = ('name',)


class PostAuthorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    uuid = serializers.UUIDField()

    class Meta:
        model = apps.get_model(*getattr(settings, "BLOGS_AUTHOR_MODEL", "blogs.Author").split('.', 1))
        exclude = ("id",)


class PostSerializer(serializers.ModelSerializer):
    author = PostAuthorSerializer(
        default=None
    )

    categories = PostCategorySerializer(
        default=[],
        many=True,
        read_only=True,
    )

    tags = PostTagSerializer(
        default=[],
        many=True,
        read_only=True,
    )

    published_at = serializers.DateField(read_only=True)

    class Meta:
        model = Post
        exclude = ("id", "status",)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ("id",)


class PostImageSerializer(serializers.ModelSerializer):
    post = serializers.CharField(
        source="post.slug",
        read_only=True
    )

    class Meta:
        model = PostImage
        exclude = ("id",)


class ParentCategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "uuid",
            "name",
            "description",
            "image",
            "icon",
        )


class CategoryReadSerializer(serializers.ModelSerializer):
    parent = ParentCategoryReadSerializer(
        read_only=True,
    )

    class Meta:
        model = Category
        fields = (
            "uuid",
            "name",
            "description",
            "parent",
            "image",
            "icon",
        )
