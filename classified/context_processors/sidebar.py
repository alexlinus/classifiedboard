from category.models import Category
from django.template.context_processors import request

def get_categories_sidebar(request):
    categories = Category.objects.filter(is_active=True)
    return {'categories': categories}