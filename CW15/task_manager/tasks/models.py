from django.db import models
from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to="category_images/", default="category_images/Ocean_18.png"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = (
        ("to-do", "To Do"),
        ("in-progress", "In Progress"),
        ("done", "Done"),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)
    files = models.FileField(upload_to="task_files/", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
