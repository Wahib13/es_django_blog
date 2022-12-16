import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from blogs.api.serializers import TagSerializer, PostTagSerializer
from blogs.models import Tag, Post
from django.http import Http404
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


class PostTagsViewSet(
    ModelViewSet
):
    serializer_class = PostTagSerializer
    lookup_field = "uuid"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        try:
            post = Post.objects.get(slug=self.kwargs.get("slug"))
            return Tag.objects.filter(posts__id__exact=post.id)
        except Post.DoesNotExist:
            return Tag.objects.none()

    def perform_create(self, serializer):
        try:
            post = Post.objects.get(slug=self.kwargs.get("slug"))
            tag = Tag.objects.get(name=self.kwargs.get("name"))
            post.tags.add(tag)
            post.save()
        except (Post.DoesNotExist, Tag.DoesNotExist):
            raise Http404

    def perform_destroy(self, instance):
        post = get_object_or_404(Post, slug=self.kwargs.get("slug"))
        try:
            post.tags.remove(instance)
        except Tag.DoesNotExist:
            raise Http404


class TagViewSet(
    ModelViewSet
):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    lookup_field = "name"
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ("name",)
    permission_classes = [IsAuthenticatedOrReadOnly]
