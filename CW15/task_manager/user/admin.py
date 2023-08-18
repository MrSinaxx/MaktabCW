from django.contrib import admin
from .models import User
from django.db.models import Count


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "number_of_tasks",
    ]
    list_filter = ["is_active", "is_staff"]
    search_fields = ["username", "email"]

    def number_of_tasks(self, obj):
        return obj.number_of_tasks()

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(task_count=Count("task"))

    number_of_tasks.short_description = "Number of Tasks"
    number_of_tasks.admin_order_field = "task_count"


admin.site.register(User, UserAdmin)
