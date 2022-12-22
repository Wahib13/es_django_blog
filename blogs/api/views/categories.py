import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from blogs.api.serializers import CategorySerializer, PostCategorySerializer, CategoryReadSerializer
from blogs.models import Category, Post
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Count

logger = logging.getLogger(__name__)


class PostCategoriesViewSet(
    ModelViewSet
):
    serializer_class = PostCategorySerializer
    lookup_field = "uuid"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        try:
            post = Post.objects.get(slug=self.kwargs.get("slug"))
            return Category.objects.filter(posts__id__exact=post.id)
        except Post.DoesNotExist:
            return Category.objects.none()

    def perform_create(self, serializer):
        try:
            post = Post.objects.get(uuid=self.kwargs.get("slug"))
            category = Category.objects.get(uuid=self.kwargs.get("uuid"))
            post.categories.add(category)
            post.save()
        except (Post.DoesNotExist, Category.DoesNotExist):
            raise Http404

    def perform_destroy(self, instance):
        post = get_object_or_404(Post, uuid=self.kwargs.get("post_uuid"))
        try:
            post.categories.remove(instance)
        except Category.DoesNotExist:
            raise Http404


class CategoryViewSet(
    ModelViewSet
):

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CategoryReadSerializer
        return CategorySerializer

    queryset = Category.objects.select_related(
        "parent"
    ).prefetch_related(
        "posts"
    ).annotate(
        total_posts=Count("posts")
    ).all()
    lookup_field = "uuid"
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_fields = ("parent__name",)
    search_fields = ("name",)
    permission_classes = [IsAuthenticatedOrReadOnly]
