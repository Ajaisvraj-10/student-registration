from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Article(models.Model):
    Name = models.CharField(max_length=200)
    Class = models.CharField(max_length=50)
    Division = models.CharField(max_length=50)
    RollNo = models.IntegerField()
    cover_image = models.ImageField(upload_to="article_images/", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

# def __str__(self):
#         return self.Name


class Comment(models.Model):
    text = models.CharField(max_length=100)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

