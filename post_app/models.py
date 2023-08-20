from django.db import models
from user_app.models import User
# Create your models here.

class Post(models.Model):
    status     = models.CharField(max_length=150, default='published')
    subject    = models.CharField(max_length=250, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    location   = models.CharField(max_length=250, blank=True, null=True)

class Post_Images(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)


class Post_Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    
