from django.shortcuts import render
from .models import Category
from classified.models import Classified
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
# Create your views here.

def get_category(request, category_slug):
    category = get_object_or_404(Category, slug__iexact=category_slug, is_active=True)
    all_classifieds = Classified.objects.filter(category=category)
    classifieds_paginator = Paginator(all_classifieds, 6)
    page = request.GET.get('page')
    try:
        classifieds = classifieds_paginator.page(page)
    except:
        classifieds = classifieds_paginator.page(1)

    current_page = classifieds.number - 1 #возвращает минимум 1, а так как у нас индексы с 0 начинаются, ,поэтому отнимаем 1
    start_index = current_page - 3
    if start_index < 0:
        start_index = 0
    max_pages = classifieds_paginator.num_pages #то же самое как и с currentp_page4
    end_index = current_page + 3
    if end_index > max_pages:
        end_index = max_pages
    page_range = list(classifieds_paginator.page_range)[start_index:end_index]
    return render(request, 'category_detail.html', context={'category': category,
                                                            'classifieds': classifieds,
                                                            'page_range': page_range})
