from django.urls import path
from . import views


urlpatterns = [
    path("categories/", views.category_list, name="category_list"),
    path("categories/<int:pk>/", views.category_details, name="category_details"),
]
