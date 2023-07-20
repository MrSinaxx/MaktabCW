from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from users.models import Author
from django.http import HttpResponse


# Create your views here.


def home(request):
    context = {}
    return render(request, "index.html", context)


def post_list(request):
    all_posts = Post.objects.all()
    return render(request, "Blog/post_list.html", {"all_posts": all_posts})


def category_list(request):
    all_category = Category.objects.all()
    return render(request, "Blog/category_list.html", {"all_category": all_category})


def category_details(request, pk):
    category = Category.objects.get(id=pk)
    return render(request, "Blog/category_details.html", {"category": category})


def search(request):
    query = request.GET.get("query")
    posts = Post.objects.filter(title__icontains=query) | Post.objects.filter(
        content__icontains=query
    )
    context = {"posts": posts, "query": query}
    return render(request, "index.html", context)


def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    context = {"post": post, "comments": comments}
    return render(request, "Blog/post.html", context)


def write_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        author_name = request.POST.get("author_name")
        content = request.POST.get("content")
        author = Author.objects.create(name=author_name)
        comment = Comment(post=post, author=author, content=content)
        comment.save()
        return redirect("post_details", pk=pk)
    else:
        return render(request, "Blog/write_comment.html", {"post": post})


def create_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        category = Category(name=name, description=description)
        category.save()
        return redirect("category_list")
    else:
        return render(request, "Blog/category_list.html")


def create_post(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == "POST":
        author = Author.objects.get(id=1)
        title = request.POST.get("title")
        content = request.POST.get("content")
        post = Post(title=title, content=content, category=category, author=author)
        post.save()
        return redirect("category_details", pk=pk)
    else:
        return render(request, "Blog/category_details.html", {"category": category})
