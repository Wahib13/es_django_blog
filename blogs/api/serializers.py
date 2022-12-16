from mptt.exceptions import InvalidMove
from rest_framework import serializers
from rest_framework.exceptions import APIException

from blog_project.blogs.models import Category


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
