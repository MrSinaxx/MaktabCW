from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.all_posts, name="all_posts"),
    path("posts/<int:pk>/", views.post_details, name="post_details"),
    path("author/", views.author_list, name="author_list"),
    path("author/<int:pk>/", views.author_details, name="author_details"),
]
