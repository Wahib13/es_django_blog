from django.urls import path

from blogs.api.views.categories import CategoryViewSet

app_name = "blogs"

urlpatterns = [
    path(
        "categories/", CategoryViewSet.as_view({"get": "list", "post": "create"}, name="categories-list")
    ),
    path(
        "categories/<str:uuid>/",
        CategoryViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"},
            name="categories-detail"
        )
    ),
]
