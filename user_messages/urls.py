from django.urls import path
from . import views

urlpatterns = [
    path(r'<str:from_user>/<str:to_user>/', views.dialog_messages, name='dialog_url'),
]
