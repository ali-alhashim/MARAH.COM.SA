from django.db import models

# Create your models here.

class Post(models.Model):
    status = models.CharField(max_length=150, default='published')


class Post_Comment(models.Model):
    post  = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
