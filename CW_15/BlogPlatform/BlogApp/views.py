from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Author, Comment
from .forms import CommentForm


def home(request):
    posts = Post.objects.all()
    authors = Author.objects.all()
    return render(request, "home.html", {"posts": posts, "authors": authors})


def all_posts(request):
    posts = Post.objects.all()
    return render(request, "all_posts.html", {"posts": posts})


def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect("post_details", pk=pk)
    else:
        form = CommentForm()

    return render(
        request, "post_details.html", {"post": post, "comments": comments, "form": form}
    )


def author_list(request):
    authors = Author.objects.all()
    return render(request, "author_list.html", {"authors": authors})


def author_details(request, pk):
    author = get_object_or_404(Author, pk=pk)
    posts = Post.objects.filter(author=author)
    return render(request, "author_details.html", {"author": author, "posts": posts})
