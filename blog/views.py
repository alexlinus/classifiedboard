from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post
# Create your views here.


def get_post(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    return render(request, 'post_detail.html', context={'post': post})


def get_blog_list(request):
    all_posts = Post.objects.filter(is_active=True)
    posts_paginator = Paginator(all_posts, 6)
    page = request.GET.get('page')
    try:
        posts = posts_paginator.page(page)
    except:
        posts = posts_paginator.page(1)

    current_page = posts.number - 1 #возвращает минимум 1, а так как у нас индексы с 0 начинаются, ,поэтому отнимаем 1
    start_index = current_page - 3
    if start_index < 0:
        start_index = 0
    max_pages = posts_paginator.num_pages #то же самое как и с currentp_page4
    end_index = current_page + 3
    if end_index > max_pages:
        end_index = max_pages
    page_range = list(posts_paginator.page_range)[start_index:end_index]
    return render(request, 'blog_list.html', context={'posts': posts, 'page_range': page_range})