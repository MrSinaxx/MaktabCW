from django.urls import path
from .views import (
    home,
    post_list,
    post_details,
    category_details,
    category_list,
    search,
    write_comment,
    create_category,
    create_post,
)

urlpatterns = [
    path("", home, name="home"),
    path("post/", post_list, name="post_list"),
    path("post/<int:pk>/", post_details, name="post_details"),
    path("categories/", category_list, name="category_list"),
    path("categories/<int:pk>/", category_details, name="category_details"),
    path("search/", search, name="search"),
    path("post/<int:pk>/write-comment/", write_comment, name="write_comment"),
    path("categories/create/", create_category, name="create_category"),
    path("categories/<int:pk>/create-post/", create_post, name="create_post"),
]
