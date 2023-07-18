from django.db import models
from users.models import Author


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    publication_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    comment_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.post}:{self.author}, {self.comment_date}"
