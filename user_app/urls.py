from django.urls import path
from . import views

urlpatterns = [
    path('new/registration/', views.register_new_user, name='register.new.user'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login/With/MobileNumber/', views.loginWithMobileNumber, name='login.With.Mobile.Number'),
    path('login/With/MobileNumber/OTP',views.verifyOTP,name='OTP.Enter')
]
