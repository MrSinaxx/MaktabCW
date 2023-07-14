from django.shortcuts import render, get_object_or_404
from .models import Category


def category_list(request):
    categories = Category.objects.all()
    return render(request, "category_list.html", {"categories": categories})


def category_details(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, "category_details.html", {"category": category})
