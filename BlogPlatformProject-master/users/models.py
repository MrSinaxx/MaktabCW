from django.db import models


# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='img/', default="img/def.jpg")

    def __str__(self):
        return self.name



