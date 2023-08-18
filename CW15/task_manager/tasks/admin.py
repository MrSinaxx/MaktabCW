from django.contrib import admin
from .models import Category, Tag, Task
import csv
from django.http import HttpResponse, JsonResponse

admin.site.register(Category)
admin.site.register(Tag)


def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(["Title", "Description", "Due Date"])
    for obj in queryset:
        writer.writerow([obj.title, obj.description, obj.due_date])

    return response


export_csv.short_description = "Export Selected Tasks as CSV"


def export_json(modeladmin, request, queryset):
    response_data = []
    for obj in queryset:
        data = {
            "Title": obj.title,
            "Description": obj.description,
            "Due Date": str(obj.due_date),
        }
        response_data.append(data)

    response = JsonResponse(response_data, safe=False)
    response["Content-Disposition"] = 'attachment; filename="tasks.json"'
    return response


export_json.short_description = "Export Selected Tasks as JSON"


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "status",
        "created",
        "updated",
        "is_active",
    ]
    readonly_fields = ["created", "updated", "is_active"]
    actions = [export_csv, export_json]


admin.site.register(Task, TaskAdmin)
