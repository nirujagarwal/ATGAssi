
from django.urls import path
from .views import create_blog_post, blog_post_list, my_blog_posts, blog_post_detail

urlpatterns = [
    path('create/', create_blog_post, name='create_blog_post'),
    path('', blog_post_list, name='blog_post_list'),
    path('my-posts/', my_blog_posts, name='my_blog_posts'), 
    path('post/<int:pk>/', blog_post_detail, name='blog_post_detail'), 
]
