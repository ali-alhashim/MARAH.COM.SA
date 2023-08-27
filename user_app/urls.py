from django.urls import path
from . import views

urlpatterns = [
    path('new/registration/', views.register_new_user, name='register.new.user'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
