from . import views
from django.urls import path

urlpatterns = [
    path('<str:page_slug>/', views.get_page, name='get_page_detail_url'),
]