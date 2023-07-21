from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Task, Category, Tag
from django.core.paginator import Paginator
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from io import BytesIO


def home(request):
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
    task = Task.objects.get(id=task_id)
    return render(request, "task.html", {"task": task})


def task_page(request):
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

        category = Category.objects.get(id=category_id)
        tags = Tag.objects.filter(id__in=tags_ids)

        task = Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            status=status,
            category=category,
        )
        task.tags.set(tags)

        return redirect("task_page")
    else:
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
        return redirect("categories")
    else:
        return render(request, "add_category.html")
