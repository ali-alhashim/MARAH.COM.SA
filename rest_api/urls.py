from django.urls import path
from . import views

urlpatterns = [
    path('posts/list', views.api_posts_list, name='api_posts_list'),
    path('locations', views.api_locations, name="api_locations"),
    path('categories', views.api_categories, name="api_categories"),
    path("subCategory", views.api_subCategoryByCategory, name="api_subCategoryByCategory"),
    path('login', views.api_login, name="api_login"),
    path('addpost', views.api_add_post, name="api_add_post"),
]