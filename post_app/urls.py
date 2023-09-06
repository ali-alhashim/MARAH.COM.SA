from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:pk>', views.post_detail, name='post.detail'),
    path('create', views.post_create, name='post.create'),
    path('get/subcategories', views.get_subcategories, name="get_subcategories"),
    path('MyPosts/list', views.MyPosts, name='My.Posts'),
    path('MyFavorite/List', views.MyFavorite_List, name='MyFavorite.List'),
    path('Post/Complaints/Message/create', views.Post_Complaints_Create, name="Post_Complaints.Message.create"),

     
]
