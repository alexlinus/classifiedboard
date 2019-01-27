from django.urls import path
from category import views

urlpatterns = [
    path('<str:category_slug>/', views.get_category, name='get_category_url'),

]