from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
    ]
    list_filter = ["is_active", "is_staff"]
    search_fields = ["username", "email"]


admin.site.register(User, UserAdmin)
