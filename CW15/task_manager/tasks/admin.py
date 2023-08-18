from django.contrib import admin
from .models import Category, Tag, Task

admin.site.register(Category)
admin.site.register(Tag)


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "status",
        "created",
        "updated",
        "is_active",
    ]
    readonly_fields = ["created", "updated", "is_active"]


admin.site.register(Task, TaskAdmin)
