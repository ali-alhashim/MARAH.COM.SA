from django.urls import path
from . import views

urlpatterns = [
    path('new/registration/', views.register_new_user, name='register.new.user'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login/With/MobileNumber/', views.loginWithMobileNumber, name='login.With.Mobile.Number'),
    path('login/With/MobileNumber/OTP',views.verifyOTP,name='OTP.Enter'),
    path('MyAccount/index/', views.MyAccount_index, name='MyAccount.index'),
    path('MyAccount/index/ResetPassword', views.ResetPassword, name='MyAccount.ResetPassword'),

    path('MyMessages/list', views.UserMessage_list, name='User.Message.list'),
    path('UserMessage/create', views.UserMessage_create, name='User.Message.create'),
    path('UserMessage/detail/<int:message_id>', views.UserMessage_detail, name='User.Message.detail'),
    
]
