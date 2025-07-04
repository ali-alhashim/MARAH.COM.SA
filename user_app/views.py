from django.shortcuts import render, redirect

from.models import User, UserMessage, UserMessageReply
from .forms import RegistrationForm
from django.contrib import messages

### otp sms 
from TaqnyatSms import client
import random
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import  login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from post_app.models import MyFavorite, Post
import json
# Create your views here.

def register_new_user(request):
    if request.method == 'POST':
       print('register_new_user start .......')
       form = RegistrationForm(request.POST)
       
       if User.objects.filter(name = request.POST.get('name')).exists:
               messages.error(request, 'الاسم موجود اختر اسم آخر')
               redirect('register.new.user')
       if User.objects.filter(mobile = request.POST.get('mobile')).exists:
                messages.error(request, 'رقم الجوال مسجل ! ')
                redirect('register.new.user')

       if form.is_valid():
           name    = form.cleaned_data['name'].lower().replace(" ", "")  
           mobile  = form.cleaned_data['mobile'].lower().replace(" ", "")
           print('form is valid')
           

           

           password= form.cleaned_data['password']
           user = User(
                        name     = name,
                        mobile   = mobile,                             
                      )
           user.set_password(password)
           
           

           

           bearer = '5679a3ef8b5814d2b364eb0d11a88b6c'

           code_number = random.randint(1000, 9999)
           request.session['code_number'] = code_number
           body       = f'{code_number}: كود التحقق من منصة مراح'
           recipients = [f'{mobile}']
           sender     = 'Marah'
           scheduled  =''
           taqnyt     = client(bearer)
           response   = taqnyt.sendMsg(body, recipients, sender,scheduled)
           response_data = json.loads(response)
           print(response_data)



           if response_data["statusCode"] == 201:
                print("Started verification")
                request.session['mobile'] = mobile
                messages.success(request, 'تم التسجيل بنجاح سيصل لك كود  التوثيق ')
               
                ## user saved
                user.save()
                return render(request,'User/OTP_verification_page.html',{})
           else:
               
                
                messages.error(request, f' {response_data} حدث خطأ الرجاء التأكد من رقم الجوال مع الرمز الدولي') 
                
                return HttpResponseRedirect(reverse_lazy('register.new.user'))
       else:
           print('form is Not valid')
          
           
    else:
        form = RegistrationForm()
    return render(request, 'User/register.html',{"form":form})



######### ForgetPassword

def ForgetPassword(request):
    ## check if request send POST mobile
    if request.method =="POST":
        if request.POST.get('mobile'):
            ## check if there is user with this mobile 
            user = User.objects.filter(mobile = request.POST.get('mobile')).first()
            if user is not None:

                ## user exist send sms 
                bearer = '5679a3ef8b5814d2b364eb0d11a88b6c'

                code_number = random.randint(1000, 9999)
                request.session['code_number'] = code_number

                body       = f'{code_number}: كود التحقق من منصة مراح'
                recipients = [f'{user.mobile}']
                sender     = 'taqnyat.sa'
                scheduled  =''
                taqnyt  = client(bearer)
                response = taqnyt.sendMsg(body, recipients, sender,scheduled)
                response_data = json.loads(response)
                print(response_data)

                if response_data["statusCode"] == 201:
                        print("Started verification ")
                       
                        request.session['mobile'] = request.POST.get('mobile')
                        request.session['forget'] = "forget"

                        messages.success(request, 'تم الارسال بنجاح سيصل لك كود  التوثيق ')
                        return render(request,'User/OTP_verification_page.html',{})
                else:
                    print("Error:")
                    messages.error(request,f'خدمة الرسائل خارج الخدمة {response_data}' )
                    return redirect('login')
            else:
                messages.error(request, ' لايوجد رقم جوال مسجل بالرقم المدخل')
                return redirect('login')
        else:
            messages.error(request, '  الرجاء إدخال رقم الجوال')
            return redirect('login')
    




def verifyOTP(request):
 

  CODE = request.POST.get('otp')
  if int(request.session['code_number']) == int(CODE):
    
        print("Verification successful")
        ## let user login
        user = User.objects.filter(mobile=request.session['mobile']).first()
        user.mobile_verified = True
        user.save()
        print('Welcome back', user.name)
        
        login(request, user)
       
        try:
           
            del request.session['mobile']
            del request.session['code_number'] 
        except Exception as e:
            print(e)

        if "forget" in request.session:
            return redirect('MyAccount.ResetPassword')
        messages.success(request,"تم التفعيل بنجاح")
        return HttpResponseRedirect(reverse_lazy('home'))
  else:
        print("Error: the code not match!")
        messages.error(request,'كود التفعيل غير صحيح')
      
        return HttpResponseRedirect(reverse_lazy('login'))
  



  ######## MyAccount
@login_required(login_url='login')
def MyAccount_index(request):
    if request.method =="POST":
        
        name = request.POST.get('name')
      
        mobile    = request.POST.get('mobile')
        user = User.objects.get(pk=request.user.id)

        ## check if the user update his email or mobile or both
        ## remove the veryfication of the old email and mobile
        if mobile != user.mobile:
            user.mobile_verified = False
            print('user update his mobile')
        
        try:
           
            user.name = name
            
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
            elif "forget" in request.session and request.session['forget'] =="forget":
                user.set_password(new_password)
                user.save()
                messages.success(request,'تم تغيير كلمة المرور الرجاء أستخدام كلمة المرور الجديدة لــ تسجيل الدخول')
                del request.session['forget']
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


#### Create User Message

def UserMessage_create(request):
    if  not request.user.id:
         messages.error(request,'عليك تسجيل الدخول أولا')
         return redirect('login')
     
    if request.method =="POST":
        send_to = request.POST.get('send_to')
        message = request.POST.get('message')
        subject = request.POST.get('subject')

        from_user = User.objects.get(pk=request.user.id)
        to_user   = User.objects.get(pk=send_to) 
        newMessage = UserMessage(
                                    from_user  =from_user,
                                    to_user    =to_user,
                                    subject    =subject,
                                    message    =message, 
                                )
        newMessage.save()
        messages.success(request, " تم إرسال الرسالة")
        return HttpResponseRedirect(reverse_lazy('User.Message.list'))
  

#### Message Detail

def UserMessage_detail(request, message_id):
    theMessage = UserMessage.objects.get(pk=message_id)
    theUserOpen = User.objects.get(pk=request.user.id)
    if theUserOpen == theMessage.to_user:
        theMessage.read_date = timezone.now()
        theMessage.save()
        theMessage = UserMessage.objects.get(pk=message_id)

    messageReply = UserMessageReply.objects.filter(reply_for=theMessage)
    for reply in messageReply:
        if reply.reply_by != theUserOpen:
           reply.read_date = timezone.now()
           reply.save()

    if request.method=="POST":
        theMessage = UserMessage.objects.get(pk=request.POST.get('message_id'))
        message_reply = request.POST.get('message_reply')
        NewMessageReply = UserMessageReply(
                                             reply_for = theMessage,
                                             message   = message_reply,
                                             reply_by  = request.user,
                                          )
        NewMessageReply.save()
        return redirect('User.Message.detail', message_id=message_id)
    return render(request, 'User/MyMessages/detail.html',{"theMessage":theMessage})




def AddRemoveMyFavorite(request, pk):
    
    if  not request.user.id:
         messages.error(request,'عليك تسجيل الدخول أولا')
         return redirect('login')
    post = Post.objects.get(pk=pk)
    theFavorite = MyFavorite.objects.filter(user = request.user, post = post).exists()
    if theFavorite:
        print('already favorite so remove')
        theFavorite = MyFavorite.objects.filter(user = request.user, post = post).first()
        theFavorite.delete()
    else:
        print('add to favorite')
        newFavorite = MyFavorite(
                                    user = request.user,
                                    post = post,
                                )
        newFavorite.save()
    return redirect('post.detail', pk=pk)