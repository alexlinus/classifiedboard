from django.db import models
from autoslug import AutoSlugField
from django.shortcuts import reverse

# Create your models here.

class Category(models.Model):
    title = models.CharField(blank=False, null=False, verbose_name='Заголовок', max_length=170)
    slug = AutoSlugField(populate_from='title', verbose_name='Ссылка на категорию')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_edit = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    is_active = models.BooleanField(default=True, verbose_name='Опубликовано')
    seo_title = models.CharField(max_length=180, blank=True, null=True, verbose_name='SEO заголовок')
    seo_description = models.CharField(max_length=200, blank=True, null=True, verbose_name='SEO описание')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('get_category_url', kwargs={'category_slug': self.slug })

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-date_edit']

