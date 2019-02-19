from django.db import models
from django.conf import settings
from category.models import Category
from autoslug import AutoSlugField
from django.shortcuts import reverse
from solo.models import SingletonModel
from pages.models import Pages
# Create your models here.

class SiteConfiguration(SingletonModel):
    class Meta:
        verbose_name = 'Настройки сайта'

    our_title = models.CharField(max_length=150, blank=True, null=True, verbose_name='Название магазина')
    our_phone = models.CharField(max_length=100, blank=True, null=True, verbose_name='Телефон магазина')
    seo_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='SEO заголовок')
    seo_description = models.TextField(max_length=240, verbose_name='SEO описание')
    pages_menu = models.ManyToManyField(Pages, verbose_name='Страницы в меню')
    blog_active = models.BooleanField(default=False, verbose_name='Актировать блог')

class Classified(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='category_classifieds', on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=170, blank=False, null=False, verbose_name='Заголовок')
    slug = AutoSlugField(populate_from='title', default=None, verbose_name='Ссылка на товар', unique_for_date=True)
    description = models.TextField(blank=True, null=True, verbose_name='Описание товара')
    price = models.PositiveIntegerField(blank=False, null=False, verbose_name='Стоимость (руб)')
    phone = models.CharField(max_length=20, blank=False, null=False, default='0', verbose_name='Телефон')
    is_active = models.BooleanField(default=False, verbose_name='Опубликовано')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    edit_date = models.DateTimeField(auto_now=True, verbose_name='Дата последнего редактирования')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='classifieds', verbose_name='Автор')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    seo_title = models.CharField(max_length=180, blank=True, null=True, verbose_name='SEO заголовок')
    seo_description = models.CharField(max_length=200, blank=True, null=True, verbose_name='SEO описание')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('get_classified_detail_url', kwargs={'classified_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.seo_title:
            self.seo_title = self.title

        if not self.seo_description:
            if self.description:
                self.seo_description = self.description[:180]
            else:
                pass
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-create_date']


class ClassifiedImages(models.Model):
    classified = models.ForeignKey(Classified, related_name='images', blank=False, null=False, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/classified_images/', default='default.jpg', verbose_name='Изображение')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения')

    def __str__(self):
        return str(self.id) + str(self.classified)

    @property
    def get_src(self):
        return '/media/' + str(self.image)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['-create_date']