from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_blog_list, name='get_blog_list_url'),
    path('<str:post_slug>/', views.get_post, name='get_post_url'),
]