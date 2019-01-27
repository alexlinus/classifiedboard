from django.db import models
from autoslug import AutoSlugField
from django.shortcuts import reverse
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=180, blank=False, null=False, verbose_name='Заголовок')
    slug = AutoSlugField(populate_from='title', default=None, verbose_name='Ссылка на статью', unique_for_date=True)
    description = models.TextField(verbose_name='Текст')
    is_active = models.BooleanField(default=False, verbose_name='Опубликовано')
    seo_title = models.CharField(max_length=190, blank=True, null=True, verbose_name='SEO заголовок')
    seo_description = models.CharField(max_length=200, blank=True, null=True, verbose_name='SEO описание')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-pub_date']

    def get_absolute_url(self):
        return reverse('get_post_url', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.seo_title:
            self.seo_title = self.title

        if not self.seo_description:
            if self.description:
                self.seo_description = self.description[:180]
            else:
                pass
        super().save(*args, **kwargs)