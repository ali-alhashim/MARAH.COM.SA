from django.contrib import admin
from .models import Post, Post_Category, Sub_Category, Post_Images, Location, Post_Comment

class PostImagesInline(admin.StackedInline):
    model = Post_Images

class PostAdmin(admin.ModelAdmin):
    list_display = ['subject', 'category', 'sub_category', 'created_date', 'last_update','created_by']
    inlines      = [PostImagesInline]
   

admin.site.register(Post, PostAdmin)


class SubCategoryInline(admin.StackedInline):
    model = Sub_Category

class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Post_Category, CategoryAdmin)


admin.site.register(Location)

admin.site.register(Post_Comment)





