from django.db import models
from user_app.models import User
from django.urls import reverse
from django_resized import ResizedImageField

# Create your models here.

class Location(models.Model):
    name         = models.CharField(max_length=250, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update  = models.DateTimeField(auto_now=True)
    latitude_start  = models.DecimalField(max_digits=9, decimal_places=6,blank=True, null=True)
    latitude_end    = models.DecimalField(max_digits=9, decimal_places=6,blank=True, null=True)
    longitude_start = models.DecimalField(max_digits=9, decimal_places=6,blank=True, null=True)
    longitude_end = models.DecimalField(max_digits=9, decimal_places=6,blank=True, null=True)
    def __str__(self):
        return self.name


class Post_Category(models.Model):
    name         = models.CharField(max_length=250, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update  = models.DateTimeField(auto_now=True)
    slug         = models.SlugField(max_length=100, unique=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('post_by_category', args=[self.slug])

# every category has many sub category
class Sub_Category(models.Model):
    category     = models.ForeignKey(Post_Category, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='sub_categories')
    name         = models.CharField(max_length=250, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update  = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Post(models.Model):
    status       = models.CharField(max_length=150, default='published')
    subject      = models.CharField(max_length=250, blank=True, null=True)
    created_by   = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    location     = models.ForeignKey(Location, on_delete=models.DO_NOTHING, null=True, blank=True)
    text         = models.TextField(max_length=1000, blank=True, null=True)
    category     = models.ForeignKey(Post_Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    sub_category     = models.ForeignKey(Sub_Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update  = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.subject


## every post has many images
class Post_Images(models.Model):
    post         = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='post_images')

    def upload_file(self, filename):
        return f'post_images/{self.post.id}/{filename}'
    image        = ResizedImageField(upload_to=upload_file, force_format="WEBP", quality=75, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update  = models.DateTimeField(auto_now=True)

## every post has many comments
class Post_Comment(models.Model):
    post         = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='post_comments')
    created_by   = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    comment      = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update  = models.DateTimeField(auto_now=True)
    status       = models.CharField(max_length=150, default='published')
    def get_created_by_nickname(self):
        return self.created_by.nikname if self.created_by else None
    

class MyFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_favorite_list')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)


class Post_Complaints(models.Model):
    post         = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    user         = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_Complaints_list')
    subject      = models.CharField(max_length=255, blank=True, null=True)
    message      = models.TextField(max_length=500, blank=True, null=True)
