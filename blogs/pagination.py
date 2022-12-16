from rest_framework.pagination import PageNumberPagination

from django.conf import settings


class LargeResultsSetPagination(PageNumberPagination):
    page_size = getattr(settings, "LARGE_PAGE_SIZE", 100)
    page_size_query_param = "page_size"
    max_page_size = getattr(settings, "LARGE_MAX_PAGE_SIZE", 2000)


class StandardResultsPagination(PageNumberPagination):
    page_size = getattr(settings, "STANDARD_PAGE_SIZE", 50)
    page_size_query_param = "page_size"
    max_page_size = getattr(settings, "STANDARD_MAX_PAGE_SIZE", 100)
