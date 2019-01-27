from django.shortcuts import render
from .models import Pages
# Create your views here.

def get_page(request, page_slug):
    page = Pages.objects.get(slug=page_slug)
    return render(request, 'page_detail.html', context={'page': page})