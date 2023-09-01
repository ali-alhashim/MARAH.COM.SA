from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from.models import User, UserMessage
from .forms import RegistrationForm
from django.contrib import messages
import vonage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import  login
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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

############################################## Auth by phone with Firebase api AIzaSyAHaM4itupXBqfaQQ-2wcRx581MMtwcvhY

def loginWithMobileNumber(request):
    # check if user already register if not let him first register for one time

    # get user Entered mobile
    ## send otp
    ## let user enter 
    mobile = request.POST.get('mobile')
    user_exists = User.objects.filter(mobile=mobile).exists()
    if user_exists:

        client = vonage.Client(key="e48cf721", secret="0kzxY067YT5r33sn")
        verify = vonage.Verify(client)
        response = verify.start_verification(number=mobile, brand="Marah")

        if response["status"] == "0":
            print("Started verification request_id is %s" % (response["request_id"]))
            request.session['request_id'] = response["request_id"]
            request.session['mobile'] = mobile
        else:
            print("Error: %s" % response["error_text"])


        return render(request,'User/OTP_verification_page.html',{})
    else:
        messages.error(request, 'أنت عضو جديد عليك التسجيل أولاً حتى تسجل الدخول برقم الجوال')
        return HttpResponseRedirect(reverse_lazy('register.new.user'))



def verifyOTP(request):
  client = vonage.Client(key="e48cf721", secret="0kzxY067YT5r33sn")
  verify = vonage.Verify(client)
  CODE = request.POST.get('otp')
  response = verify.check(request.session['request_id'], code=CODE)

  if response["status"] == "0":
        print("Verification successful, event_id is %s" % (response["event_id"]))
        ## let user login
        user = User.objects.filter(mobile=request.session['mobile']).first()
        user.mobile_verified = True
        user.save()
        print('Welcome back', user.full_name)
        login(request, user)
       

        del request.session['request_id']
        del request.session['mobile']
        return HttpResponseRedirect(reverse_lazy('home'))
  else:
        print("Error: %s" % response["error_text"])
        del request.session['request_id']
        return HttpResponseRedirect(reverse_lazy('login'))
  



  ######## MyAccount
@login_required(login_url='login')
def MyAccount_index(request):
    if request.method =="POST":
        email     = request.POST.get('email')
        full_name = request.POST.get('full_name')
        nikname   = request.POST.get('nikname')
        mobile    = request.POST.get('mobile')
        user = User.objects.get(pk=request.user.id)

        ## check if the user update his email or mobile or both
        ## remove the veryfication of the old email and mobile
        if mobile != user.mobile:
            user.mobile_verified = False
            print('user update his mobile')
        if email != user.email:
            user.email_verified  = False
            print('user update his email')
        try:
            user.email     = email
            user.full_name = full_name
            user.nikname   = nikname
            user.mobile    = mobile
            user.save()
            messages.success(request,'تم الحفظ')
            return HttpResponseRedirect(reverse_lazy('MyAccount.index'))
        except Exception as e:
            print(e)
            messages.error(request, 'حدث خطأ')

    return render(request, 'User/MyAccount/index.html', {})


#### ResetPassword
@login_required(login_url='login')
def ResetPassword(request):
    if request.method =="POST":
        current_password = request.POST.get('current_password')
        new_password     = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
    
        if new_password == confirm_password:
            user = User.objects.get(pk=request.user.id)
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                messages.success(request,'تم تغيير كلمة المرور الرجاء أستخدام كلمة المرور الجديدة لــ تسجيل الدخول')
                return HttpResponseRedirect(reverse_lazy('login'))
            else:
                messages.error(request, 'كلمة المرور الحاليه غير صحيحة')
                return HttpResponseRedirect(reverse_lazy('MyAccount.ResetPassword'))
        else:
            messages.error(request, 'كلمة المرور الجديدة غير متطابقة')
            return HttpResponseRedirect(reverse_lazy('MyAccount.ResetPassword'))

    return render(request, 'User/MyAccount/ResetPassword.html', {})


#### UserMessage list

def UserMessage_list(request):
    user = User.objects.get(pk=request.user.id)
    userInbox = UserMessage.objects.filter(Q(from_user = user) | Q(to_user = user))
    return render(request,'User/MyMessages/list.html',{"userInbox":userInbox})
  
  