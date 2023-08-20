from django.db import models
from user_app.models import User
# Create your models here.



class Post_Category(models.Model):
    name         = models.CharField(max_length=250, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update  = models.DateTimeField(auto_now=True)

# every category has many sub category
class Sub_Category(models.Model):
    category     = models.ForeignKey(Post_Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    name         = models.CharField(max_length=250, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update  = models.DateTimeField(auto_now=True)

class Post(models.Model):
    status       = models.CharField(max_length=150, default='published')
    subject      = models.CharField(max_length=250, blank=True, null=True)
    created_by   = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    location     = models.CharField(max_length=250, blank=True, null=True)
    text         = models.TextField(max_length=1000, blank=True, null=True)
    category     = models.ForeignKey(Post_Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update  = models.DateTimeField(auto_now=True)


## every post has many images
class Post_Images(models.Model):
    post         = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='post_images')
    def upload_file(self, filename):
        return f'post_images/{self.post.id}/{filename}'
    image        = models.ImageField(upload_to=upload_file, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update  = models.DateTimeField(auto_now=True)

## every post has many comments
class Post_Comment(models.Model):
    post         = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    created_by   = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    comment      = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update  = models.DateTimeField(auto_now=True)
    status       = models.CharField(max_length=150, default='published')
    
