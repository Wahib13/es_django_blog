from django.urls import path

from blogs.api.views.categories import CategoryViewSet, PostCategoriesViewSet
from blogs.api.views.posts import PostViewSet, PostImageViewSet, ImageViewSet
from blogs.api.views.tags import TagViewSet, PostTagsViewSet

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

    path(
        "posts/<str:slug>/categories/",
        PostCategoriesViewSet.as_view({"get": "list", }),
        name="posts_categories-list"
    ),
    path(
        "posts/<str:slug>/categories/<str:uuid>/",
        PostCategoriesViewSet.as_view({"post": "create", "delete": "destroy", }),
        name="posts_categories-create-delete"
    ),

    path(
        "posts/<str:slug>/tags/",
        PostTagsViewSet.as_view({"get": "list", }),
        name="posts_tags-list"
    ),
    path(
        "posts/<str:slug>/tags/<str:name>/",
        PostTagsViewSet.as_view({"post": "create", "delete": "destroy", }),
        name="posts_tags-create-delete"
    ),
]
