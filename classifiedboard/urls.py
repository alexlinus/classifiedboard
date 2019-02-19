"""classifiedboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from classified import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home_url'),
    path(r'dialog/', include('user_messages.urls')),
    path('add_classified/', views.add_classified, name='add_classified_url'),
    path('category/', include('category.urls')),
    path('classified/', include('classified.urls')),
    path('search/', views.search, name='search_url'),
    path(r'register/', views.get_register, name='get_register_url'),
    path(r'my_classifieds/', views.get_user_classifieds, name='get_user_classifieds_url'),
    path(r'accounts/', include('allauth.urls')),
    path(r'blog/', include('blog.urls')),
    path(r'page/', include('pages.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Остановился на том, что нужно вывести форму авторизации в модальное окно в Base.Html