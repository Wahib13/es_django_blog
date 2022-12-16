import logging
from typing import Any
from urllib.request import Request

from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status

from blogs.api.serializers import PostSerializer, PostImageSerializer
from blogs.models import Post, PostImage
from django.apps import apps
from django.conf import settings

logger = logging.getLogger(__name__)


class PostViewSet(
    ModelViewSet
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "slug"
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    # filterset_fields = ("category",)
    search_fields = ("title",)

    # permission_classes = [IsAuthenticatedOrReadOnly]

    def handle_create_update_with_author(self, serializer):
        author_data = serializer.validated_data.pop("author", None)
        if not author_data:
            serializer.save()
            return
        try:
            author = apps.get_model(*getattr(settings, "BLOGS_AUTHOR_MODEL", "blogs.Author").split('.', 1)).objects.get(
                uuid=author_data.get("uuid"))
            serializer.save(author=author)
        except apps.get_model(*getattr(settings, "BLOGS_AUTHOR_MODEL", "blogs.Author").split('.', 1)).DoesNotExist:
            serializer.save()

    def perform_create(self, serializer):
        self.handle_create_update_with_author(serializer)

    def perform_update(self, serializer):
        self.handle_create_update_with_author(serializer)


class PostImageViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    serializer_class = PostImageSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return PostImage.objects.filter(post__slug=self.kwargs.get("slug"))

    def perform_create(self, serializer):
        try:
            recipe = PostImage.objects.get(slug=self.kwargs.get("slug"))
            serializer.save(recipe=recipe)
        except PostImage.DoesNotExist:
            raise Http404


class ImageViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    serializer_class = PostImageSerializer
    lookup_field = 'uuid'
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return PostImage.objects.all()


class PublishPost(
    CreateAPIView
):
    permission_classes = [IsAuthenticated]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            post = Post.objects.get(slug=self.kwargs.get("slug"))
            post.publish()
            return Response(
                status=status.HTTP_200_OK,
            )
        except Post.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "detail": "post does not exist"
                }
            )
