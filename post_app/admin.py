from django.contrib import admin
from.models import Post_Category, Sub_Category, Post, Post_Images
# Register your models here.


class SubCategoryInline(admin.StackedInline):
    model = Sub_Category
    raw_id_fields = ('category',)  # Add this line to enable filtering

class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]

class PostImagesInline(admin.StackedInline):
    model = Post_Images

class PostAdmin(admin.ModelAdmin):
    inlines = [PostImagesInline]

admin.site.register(Post, PostAdmin)

admin.site.register(Post_Category, CategoryAdmin)