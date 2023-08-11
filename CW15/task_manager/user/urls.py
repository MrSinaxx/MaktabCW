from django.urls import path
from . import views
from .views import ProfileView

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
