from mptt.exceptions import InvalidMove
from rest_framework import serializers
from rest_framework.exceptions import APIException

from blogs.models import Category, Post, PostImage


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

    def create(self, validated_data):
        parent = validated_data.pop("parent")
        category = super().create(validated_data)
        try:
            if parent and parent.get("name"):
                parent_serializer = CategorySerializer(data={"name": parent.get("name")})
                parent_serializer.is_valid(raise_exception=True)
                parent = parent_serializer.save()
                category.parent = parent
                category.save()
            return category
        except InvalidMove:
            raise APIException(detail="category may not be a child of itself")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("id", "status",)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("id",)


class PostImageSerializer(serializers.ModelSerializer):
    post = serializers.CharField(
        source="post.slug",
        read_only=True
    )

    class Meta:
        model = PostImage
        exclude = ("id",)


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
