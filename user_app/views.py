from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from.models import User
from .forms import RegistrationForm
from django.contrib import messages

# Create your views here.

def register_new_user(request):
    if request.method == 'POST':
       form = RegistrationForm(request.POST)
       if form.is_valid():
           full_name    = form.cleaned_data['full_name']  
           mobile  = form.cleaned_data['mobile']
           email   = form.cleaned_data['email']
           nikname = form.cleaned_data['nikname']
           password= form.cleaned_data['password']
           user = User.objects.create(
                                       full_name     = full_name,
                                       mobile   = mobile,
                                       email    = email,
                                       nikname  = nikname, 
                                      
                                     )
           user.set_password(password)
           user.save()

           # user Activation
           current_site = get_current_site(request)
           mail_subject = 'please activate your account'
           message      = render_to_string('User/account_verification_email.html',{"user"  :user,
                                                                                    "domain":current_site,
                                                                                    "uid"   :urlsafe_base64_encode(force_bytes(user.pk)),
                                                                                    "token" : default_token_generator.make_token(user),
                                                                                    })
           to_email = email
           send_email = EmailMessage(mail_subject, message, to=[to_email])
           send_email.send()
           messages.success(request, 'تم التسجيل بنجاح سيصل لك رابط لــ توثيق البريد الإلكتروني')
           return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html',{"form":form})



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        pass
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()
        messages.success(request, 'تم توثيق البريد الإلكتروني بنجاح')
    else:
        messages.error(request, 'invlied activation link!') 
    return redirect('login')
