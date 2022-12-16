import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from blogs.api.serializers import TagSerializer
from blogs.models import Tag

logger = logging.getLogger(__name__)


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
