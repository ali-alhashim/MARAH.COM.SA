from django.contrib import admin
from .models import Post, Post_Category, Sub_Category

class PostAdmin(admin.ModelAdmin):
    list_display = ['subject', 'category', 'sub_category', 'created_date', 'last_update']

   

admin.site.register(Post, PostAdmin)

