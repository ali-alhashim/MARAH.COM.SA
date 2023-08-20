from django.urls import path, include
from . import views

urlpatterns = [
    path('detail/<int:pk>', views.post_detail, name='post.detail'),
]
