from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Login_Logs
from .forms import UserChangeForm, UserCreationForm
# Register your models here.
from django.contrib.auth.forms import AdminPasswordChangeForm


class UserAdmin(BaseUserAdmin):

    
    list_display  = ['name',  'mobile','last_login',  'mobile_verified']
    search_fields = ['name','mobile']
    ordering      = ['name',]
    exclude       = ('date_joined','first_name','username','last_name','email')
    change_password_form = AdminPasswordChangeForm

    form      = UserChangeForm
    add_form  = UserCreationForm

    fieldsets = (
        (None, {'fields': ('name', 'mobile', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'mobile', 'password1', 'password2'),
        }),
    )
  

    ordering = ['-date_joined',]
admin.site.register(User, UserAdmin)

class LogsAdmin(admin.ModelAdmin):
    list_display = ['ip','browser','user','location','created_date']

admin.site.register(Login_Logs, LogsAdmin)



