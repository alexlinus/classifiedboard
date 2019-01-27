from . import views
from django.urls import path

urlpatterns = [
    path('<str:classified_slug>/', views.get_classified, name='get_classified_detail_url'),
    path('<str:classified_slug>/edit/', views.classified_edit, name='edit_classified_url'),
    path('<str:classified_slug>/delete/', views.classified_delete, name='delete_classified_url'),
]