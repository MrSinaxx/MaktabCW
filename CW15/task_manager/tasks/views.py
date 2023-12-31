from asyncio import mixins
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Task, Category, Tag
from django.core.paginator import Paginator
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from .mixin import TodoOwnerRequiredMixin


def home(request):
    if request.user.is_authenticated:
        user = request.user
        tasks = Task.objects.filter(user=user)
    else:
        tasks = Task.objects.all()

    paginator = Paginator(tasks, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "home.html", {"page_obj": page_obj})


def search(request):
    query = request.GET.get("query", None)
    if query is not None:
        tasks = Task.objects.filter(title__icontains=query) | Task.objects.filter(
            tags__name__icontains=query
        )
        return render(request, "search.html", {"tasks": tasks})
    else:
        return render(request, "search.html", {})


def task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(
        request, "task.html", {"task": task, "categories": categories, "tags": tags}
    )


def task_page(request):
    user = request.user

    if user.is_authenticated:
        tasks_todo = Task.objects.filter(status="to-do", user=user)
        tasks_in_progress = Task.objects.filter(status="in-progress", user=user)
        tasks_done = Task.objects.filter(status="done", user=user)
    else:
        tasks_todo = Task.objects.filter(status="to-do")
        tasks_in_progress = Task.objects.filter(status="in-progress")
        tasks_done = Task.objects.filter(status="done")

    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        "tasks_todo": tasks_todo,
        "tasks_in_progress": tasks_in_progress,
        "tasks_done": tasks_done,
        "categories": categories,
        "tags": tags,
    }
    return render(request, "task_page.html", context)


def all_categories(request):
    user = request.user

    if user.is_authenticated:
        categories = Category.objects.filter(user=user)
    else:
        categories = Category.objects.all()

    return render(request, "categories.html", {"categories": categories})


def autocomplete_data(request):
    task_titles = Task.objects.values_list("title", flat=True)
    tag_names = Tag.objects.values_list("name", flat=True)

    autocomplete_data = list(task_titles) + list(tag_names)

    return JsonResponse(autocomplete_data, safe=False)


def show_pdf(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    doc = SimpleDocTemplate(f"{task.title}.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title = Paragraph(f"<b>Title:</b> {task.title}", styles["Heading1"])
    description = Paragraph(f"<b>Description:</b> {task.description}", styles["Normal"])
    due_date = Paragraph(f"<b>Due Date:</b> {task.due_date}", styles["Normal"])
    status = Paragraph(f"<b>Status:</b> {task.status}", styles["Normal"])
    category = Paragraph(f"<b>Category:</b> {task.category.name}", styles["Normal"])

    tags = ", ".join(tag.name for tag in task.tags.all())
    tags = Paragraph(f"<b>Tags:</b> {tags}", styles["Normal"])

    story.extend(
        [
            title,
            Spacer(1, 12),
            description,
            Spacer(1, 12),
            due_date,
            Spacer(1, 12),
            status,
            Spacer(1, 12),
            category,
            Spacer(1, 12),
            tags,
        ]
    )

    doc.build(story)

    with open(f"{task.title}.pdf", "rb") as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{task.title}.pdf"'
        return response


# def add_category(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         if name:
#             category = Category(name=name)
#             category.save()
#     return redirect("all_categories")


def create_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        status = request.POST.get("status")
        category_id = request.POST.get("category")
        tags_ids = request.POST.getlist("tags")
        files = request.FILES.get("files")

        category = Category.objects.get(id=category_id)
        tags = Tag.objects.filter(id__in=tags_ids)

        if request.user.is_authenticated:
            task = Task.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                status=status,
                category=category,
                files=files,
                user=request.user,
            )
            task.tags.set(tags)

            set_history_cookie(request, "Task Created")

            return redirect("task_page")

    return redirect("task_page")


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        due_date = request.POST["due_date"]
        status = request.POST["status"]
        category = get_object_or_404(Category, pk=request.POST["category"])

        task = Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            status=status,
            category=category,
        )
        tags = request.POST.getlist("tags")
        if tags:
            task.tags.add(*tags)

        return redirect("category_detail", category_id=category_id)

    tags = Tag.objects.all()

    context = {
        "category": category,
        "tags": tags,
    }
    return render(request, "category_detail.html", context)


def create_task_in_category(request, category_id):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        status = request.POST.get("status")
        category = get_object_or_404(Category, pk=category_id)

        task = Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            status=status,
            category=category,
        )
        task.save()

        return redirect("category_detail", category_id=category_id)

    return render(request, "create_task_in_category.html", {"category_id": category_id})


def create_tag(request, task_id):
    if request.method == "POST":
        tag_name = request.POST.get("tag_name")
        task = get_object_or_404(Task, id=task_id)
        tag = Tag.objects.create(name=tag_name)
        task.tags.add(tag)
        return redirect("task", task_id=task_id)
    else:
        return redirect("task", task_id=task_id)


def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        image = request.FILES.get("image")
        category = Category.objects.create(name=name, image=image)
        set_history_cookie(request, "Category Created")
        return redirect("categories")
    else:
        return render(request, "add_category.html")


def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        name = request.POST.get("name")
        image = request.FILES.get("image")

        category.name = name

        if image:
            category.image = image

        category.save()
        set_history_cookie(request, "Category Updated")

        return redirect("category_detail", category_id=category_id)

    return render(request, "category_detail.html", {"category": category})


class UpdateTaskView(TodoOwnerRequiredMixin, View):
    def get(self, request, task_id):
        task = self.get_task()
        task = get_object_or_404(Task, id=task_id)
        categories = Category.objects.all()
        tags = Tag.objects.all()
        return render(
            request, "task.html", {"task": task, "categories": categories, "tags": tags}
        )

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        status = request.POST.get("status")
        category_id = request.POST.get("category")
        tags_ids = request.POST.getlist("tags")

        category = Category.objects.get(id=category_id)
        tags = Tag.objects.filter(id__in=tags_ids)

        task.title = title
        task.description = description
        task.due_date = due_date
        task.status = status
        task.category = category
        task.tags.set(tags)

        if request.FILES.get("files"):
            task.files = request.FILES["files"]

        task.save()
        self.set_history_cookie(request, "Task Updated")

        return redirect("task", task_id)

    def set_history_cookie(self, request, message):
        response = HttpResponse()
        response.set_cookie("history", message)
        return response


def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    return render(request, "tag_detail.html", {"tag": tag})


def update_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)

    if request.method == "POST":
        name = request.POST.get("name")
        tag.name = name
        tag.save()
        return redirect("tag_detail", tag_id=tag_id)
    else:
        return render(request, "tag_detail.html", {"tag": tag})


def delete_category(request, category_id):
    if request.method == "POST":
        category = Category.objects.get(id=category_id)
        category.delete()
        set_history_cookie(request, "Category Deleted")
        return redirect("all_categories")
    else:
        return redirect("all_categories")


def delete_task(request, task_id):
    if request.method == "POST":
        task = Task.objects.get(id=task_id)
        task.delete()
        set_history_cookie(request, "Task Deleted")

        return redirect("task_page")
    else:
        return redirect("task_page")


def set_history_cookie(request, activity):
    history = request.COOKIES.get("history", "")
    history += f"{activity},"
    print(request.COOKIES)
    response = render(request, "histories.html", {})
    response.set_cookie("history", history)
    return response


def histories(request):
    history = request.COOKIES.get("history", "")
    activities = history.split(",") if history else []
    return render(request, "histories.html", {"activities": activities})
