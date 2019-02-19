from django.contrib import admin
from .models import Classified, ClassifiedImages, SiteConfiguration
# Register your models here.

class ClassifiedImagesInline(admin.TabularInline):
    model = ClassifiedImages
    extra = 1

class ClassifiedAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'create_date', 'author', 'category']
    inlines = [ClassifiedImagesInline]

    class Meta:
        model = Classified

admin.site.register(Classified, ClassifiedAdmin)

class ClassifiedImagesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ClassifiedImages._meta.fields]

    class Meta:
        model = ClassifiedImages

admin.site.register(ClassifiedImages, ClassifiedImagesAdmin)


from solo.admin import SingletonModelAdmin

admin.site.register(SiteConfiguration, SingletonModelAdmin)
