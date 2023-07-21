from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("task/<int:task_id>/", views.task, name="task"),
    path("tasks/", views.task_page, name="task_page"),
    path("categories/", views.all_categories, name="all_categories"),
    path("add_category/", views.add_category, name="add_category"),
    path("autocomplete_data/", views.autocomplete_data, name="autocomplete_data"),
    path("task/<int:task_id>/pdf/", views.show_pdf, name="show_pdf"),
    path("create_task/", views.create_task, name="create_task"),
    path("category/<int:category_id>/", views.category_detail, name="category_detail"),
    path(
        "category/<int:category_id>/create_task/",
        views.create_task_in_category,
        name="create_task_in_category",
    ),
    path("task/<int:task_id>/create_tag/", views.create_tag, name="create_tag"),
    path(
        "category_detail/<int:category_id>/update/",
        views.update_category,
        name="update_category",
    ),
    path("task/<int:task_id>/update/", views.update_task, name="update_task"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
