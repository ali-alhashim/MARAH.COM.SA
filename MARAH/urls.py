"""MARAH URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.LogoutInterfaceView.as_view(), name='logout'),
    path('User/Agreement/', views.UserAgreement, name="User.Agreement"),
    path('', views.home, name='home'),

    path('Filter/', views.search, name='post.search'),
    path('load_more_post/', views.load_more_posts, name='post.load_more'),

    path('post/', include('post_app.urls')),
    path('User/', include('user_app.urls')),
    path('client_Location', views.client_Location, name="client.Location"),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


handler403 = 'MARAH.views.custom_error_403'
