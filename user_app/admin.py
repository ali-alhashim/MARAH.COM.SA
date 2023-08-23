from django.contrib import admin
from .models import User
# Register your models here.



class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'mobile','last_login']
    search_fields = ['full_name','email','mobile']

admin.site.register(User, UserAdmin)


