from django.shortcuts import render
from .models import Author


# Create your views here.


def author_list(request):
    all_author = Author.objects.all()
    return render(request, "Author/authors.html", {"all_author": all_author})


def author_details(request, pk):
    author = Author.objects.get(id=pk)
    return render(request, "Author/author.html", {"author": author})