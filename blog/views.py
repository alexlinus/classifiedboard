from django.shortcuts import render
from .models import Post
# Create your views here.


def get_post(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    return render(request, 'post_detail.html', context={'post': post})


def get_blog_list(request):
    posts = Post.objects.filter(is_active=True)
    return render(request, 'blog_list.html', context={'posts': posts})