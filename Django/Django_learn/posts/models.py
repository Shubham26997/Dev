from django.db import models
# from django.contrib.auth.models import User
from users.models import User
# Create your models here.


class Tag(models.Model):

    tag_name = models.CharField(max_length=30)

    def __str__(self):
        return self.tag_name


class Post(models.Model):
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='posts')
    tag = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title
