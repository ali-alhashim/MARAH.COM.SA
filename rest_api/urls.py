from django.urls import path
from . import views

urlpatterns = [
    path('posts/list', views.api_posts_list, name='api_posts_list'),
    path('post/detail', views.api_post_detail, name="api_post_detail"),
    path('locations', views.api_locations, name="api_locations"),
    path('categories', views.api_categories, name="api_categories"),
    path("subCategory", views.api_subCategoryByCategory, name="api_subCategoryByCategory"),
    path('login', views.api_login, name="api_login"),
    path('addpost', views.api_add_post, name="api_add_post"),
    path('add/comment', views.api_add_post_comment,name="api_add_post_comment"),
    path('add/favorite', views.api_add_to_my_favorite, name="api_add_to_my_favorite"),
]