from django.urls import path

from blogs.api.views.categories import CategoryViewSet
from blogs.api.views.posts import PostViewSet, PostImageViewSet, ImageViewSet
from blogs.api.views.tags import TagViewSet

app_name = "blogs"

urlpatterns = [
    path(
        "categories/", CategoryViewSet.as_view({"get": "list", "post": "create"}, name="categories-list")
    ),
    path(
        "category/<str:uuid>/",
        CategoryViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"},
            name="category-detail"
        )
    ),

    path(
        "tags/", TagViewSet.as_view({"get": "list", "post": "create"}, name="posts-list")
    ),
    path(
        "tag/<str:name>/",
        TagViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"},
            name="tag-detail"
        )
    ),

    path(
        "posts/", PostViewSet.as_view({"get": "list", "post": "create"}, name="posts-list")
    ),
    path(
        "post/<str:slug>/",
        PostViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"},
            name="post-detail"
        )
    ),

    path(
        "posts/<str:slug>/images/", PostImageViewSet.as_view({"get": "list", "post": "create"}, name="post-images-list")
    ),
    path(
        "posts/images/<str:uuid>/",
        ImageViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"},
            name="post-image-detail"
        )
    ),
]
