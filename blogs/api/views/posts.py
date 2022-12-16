import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from django.http import Http404

from blogs.api.serializers import PostSerializer, PostImageSerializer
from blogs.models import Post, PostImage

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
    permission_classes = [IsAuthenticatedOrReadOnly]


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
