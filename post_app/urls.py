from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:pk>', views.post_detail, name='post.detail'),
    path('create', views.post_create, name='post.create'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories')
]
