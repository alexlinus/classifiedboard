from django.db import models
from autoslug import AutoSlugField
from django.shortcuts import reverse
# Create your models here.

class Pages(models.Model):
    title = models.CharField(max_length=180, blank=False, null=False, verbose_name='Заголовок страницы')
    slug = AutoSlugField(populate_from='title', default=None, verbose_name='Ссылка на страницу', unique_for_date=True)
    description = models.TextField(verbose_name='Текст страницы')
    is_active = models.BooleanField(default=False, verbose_name='Опубликовано')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    edit_date = models.DateTimeField(auto_now=True, verbose_name='Дата последнего редактирования')

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        ordering = ['-create_date']

    def __str__(self):
        return self.title