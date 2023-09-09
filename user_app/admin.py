from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserChangeForm, UserCreationForm
# Register your models here.
from django.contrib.auth.forms import AdminPasswordChangeForm


class UserAdmin(BaseUserAdmin):

    
    list_display  = ['full_name', 'email', 'mobile','last_login', 'email_verified', 'mobile_verified','nikname']
    search_fields = ['full_name','email','mobile']
    ordering      = ['email',]
    exclude       = ('date_joined','first_name','username','last_name')
    change_password_form = AdminPasswordChangeForm

    form      = UserChangeForm
    add_form  = UserCreationForm
    fieldsets = (
    ('login info | معلومات الدخول', {'fields': ('email', 'password', 'mobile')}),
    ('Personal info | المعلومات الشخصية', {'fields': ('full_name',)}),
    ('Permissions | الصلاحيات', {'fields': ('is_admin', 'is_superuser', 'is_staff', 'is_active', 'groups')}),
)
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
                        ('login info | معلومات الدخول', {
                                                            'classes': ('wide',),
                                                            'fields': ('email', 'password1', 'password2'),
                                                         }
                        ),

                        ('Personal info | المعلومات الشخصية', {'fields': ('full_name', 'nikname')}),
                        
                        ('Permissions | الصلاحيات',   {'fields': ('is_admin', 'is_superuser','is_staff','is_active','groups')}),
                    )

    ordering = ['-date_joined',]
admin.site.register(User, UserAdmin)



