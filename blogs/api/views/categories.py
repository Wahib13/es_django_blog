import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from blogs.api.serializers import CategorySerializer
from blogs.models import Category

logger = logging.getLogger(__name__)


class CategoryViewSet(
    ModelViewSet
):
    serializer_class = CategorySerializer
    # pagination_class = StandardResultsPagination
    queryset = Category.objects.prefetch_related(
        "parent"
    ).all()
    lookup_field = "uuid"
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_fields = ("parent__name",)
    search_fields = ("name",)
    permission_classes = [IsAuthenticatedOrReadOnly]
