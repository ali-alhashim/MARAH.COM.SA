from django.contrib import admin

from .forms import CustomUserChangeForm
from .models import User
# Register your models here.



class UserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm
    list_display = ['full_name', 'email', 'mobile','last_login']
    search_fields = ['full_name','email','mobile']
    ordering = ['email']
    exclude = ('date_joined','first_name','username','last_name')

admin.site.register(User, UserAdmin)



