from django.contrib import admin
from .models import User
from django.db.models import Count
from django.contrib.admin import SimpleListFilter


class GreatUserFilter(SimpleListFilter):
    title = "is_great_user"
    parameter_name = "is_great_user"

    def lookups(self, request, model_admin):
        return [
            ("Yes", "Yes"),
            ("No", "No"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "Yes":
            return queryset.annotate(task_count=Count("task")).filter(task_count__gt=10)
        if self.value() == "No":
            return queryset.annotate(task_count=Count("task")).filter(
                task_count__lte=10
            )


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
    list_filter = ["is_active", "is_staff", GreatUserFilter]

    def number_of_tasks(self, obj):
        return obj.number_of_tasks()

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(task_count=Count("task"))

    number_of_tasks.short_description = "Number of Tasks"
    number_of_tasks.admin_order_field = "task_count"


admin.site.register(User, UserAdmin)
