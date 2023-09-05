from django.contrib import admin
from .models import Post, Post_Category, Sub_Category, Post_Images, Location, Post_Comment, Post_Complaints

class PostImagesInline(admin.StackedInline):
    model = Post_Images

class PostAdmin(admin.ModelAdmin):
    list_display = ['subject', 'category', 'sub_category', 'created_date', 'last_update','created_by']
    inlines      = [PostImagesInline]


class PostComplaintsAdmin(admin.ModelAdmin):
    
    list_display = ['post','subject','user','created_date']

admin.site.register(Post_Complaints, PostComplaintsAdmin)
   

admin.site.register(Post, PostAdmin)


class SubCategoryInline(admin.StackedInline):
    model = Sub_Category

class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Post_Category, CategoryAdmin)


admin.site.register(Location)

admin.site.register(Post_Comment)







