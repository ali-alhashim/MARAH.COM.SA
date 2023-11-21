from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import re


# Create your models here.
############################################## User
class MyAccountManager(BaseUserManager):
    def created_user(self, name, mobile,is_staff, is_superuser,  password=None):
        if not mobile:
            raise ValueError('User must have an mobile address or mobile')
        now = timezone.now()
        user = self.model(
            
            mobile = (mobile.lower()).replace(" ", ""),
            is_staff=is_staff, 
            is_superuser=is_superuser, 
            name = (name.lower()).replace(" ", ""),
            last_login=now,
            date_joined=now, 
            
          
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, name, mobile,  password):
        user = self.created_user(
            mobile = mobile,
            name= name,
            is_superuser = True,
            is_staff = True,
            
        )

        user.is_admin = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    


class User(AbstractBaseUser, PermissionsMixin):
    mobile              = models.CharField(max_length=255, unique=True)
    name                = models.CharField(max_length=100, blank=True, null=True, unique=True)
    token               = models.CharField(max_length=64, blank=True)
    
    mobile_verified     = models.BooleanField(default=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_update         = models.DateTimeField(auto_now=True)
    
    
    
    #username          = None
   


    def image_upload(instance, filename):
       
        return 'userApp/User_Profile_Photo/' + instance.name + '/'+filename 

    profile_photo = models.ImageField(upload_to= image_upload, blank=True, max_length=500)


   
    LANGUAGE_CHOICES = (
                        ('en-us', 'English'),
                        ('ar', 'Arabic'),
                        )

    language = models.CharField(default='en-us', choices=LANGUAGE_CHOICES, max_length=5)

    

    date_joined   = models.DateTimeField(auto_now_add=True)
    is_active     = models.BooleanField(default=True)
    is_admin      = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_superuser  = models.BooleanField(default=False)

    is_online             = models.BooleanField(default=False)
   

    objects = MyAccountManager()

    USERNAME_FIELD =  'mobile'
    REQUIRED_FIELDS = [ 'name',]

    def __str__(self):
        
        return self.name
        
    class Meta:
        ordering = ['-id']
    
    

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True



    def has_module_permission(self,request):
        return True
    
    def check_has_permission(self, perm, permissions_to_check):
        for index in range(len(permissions_to_check)):
            if perm == permissions_to_check[index]['codename']:
                return True

######################## \ user


####### User Messages

class UserMessage(models.Model):
    from_user    = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_sent_messages')
    to_user      = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_inbox_messages')
    sent_date    = models.DateTimeField(auto_now_add=True)
    read_date    = models.DateTimeField(blank=True, null=True)
    subject      = models.CharField(max_length=255, blank=True, null=True)
    message      = models.TextField(max_length=500, blank=True, null=True)
    class Meta:
        ordering = ['-sent_date']

class UserMessageReply(models.Model):
    reply_for   = models.ForeignKey(UserMessage, on_delete=models.CASCADE, blank=True, null=True, related_name='message_replies')
    sent_date   = models.DateTimeField(auto_now_add=True)
    message     = models.TextField(max_length=500, blank=True, null=True)
    reply_by    = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    read_date   = models.DateTimeField(blank=True, null=True)
    class Meta:
        ordering = ['sent_date']





class Login_Logs(models.Model):
     created_date        = models.DateTimeField(auto_now_add=True)
     ip                  = models.CharField(max_length=100, blank=True, null=True)
     location            = models.CharField(max_length=100, blank=True, null=True)
     browser             = models.CharField(max_length=100, blank=True, null=True)
     user                = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)



