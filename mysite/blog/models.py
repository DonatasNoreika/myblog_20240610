from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField(verbose_name="Title", max_length=50)
    content = models.TextField(verbose_name="Content", max_length=3000)
    date_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    author = models.ForeignKey(to=User, verbose_name="Author", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']


class Comment(models.Model):
    content = models.TextField(verbose_name="Content", max_length=1000)
    date_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    author = models.ForeignKey(to=User, verbose_name="Author", on_delete=models.CASCADE)
    post = models.ForeignKey(to="Post", verbose_name="Post", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.content} ({self.author})"

    class Meta:
        ordering = ['-date_created']