from django.forms import ModelForm, inlineformset_factory, forms
from django.utils.safestring import mark_safe

from .models import Classified, ClassifiedImages
from django.contrib.admin.widgets import AdminFileWidget

class AddClassifiedForm(ModelForm):
    class Meta:
        model = Classified
        exclude = ['author', 'edit_date', 'create_date', 'views', 'slug', 'seo_description', 'seo_title']

    #Далее мы переопределям __init__ класс формы, где указываем для каждого поля класс и плейсхолдер, куда помещаем label поля
    def __init__(self, *args, **kwargs):
        super(AddClassifiedForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" /></a>' %(image_url, image_url, file_name))
            return mark_safe(u''.join(output))
        else:
            return mark_safe(u''.join(super(AdminFileWidget, self).render(name, value, attrs, renderer)))
            #output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))

class ImageClassifiedForm(ModelForm):
    image = forms.FileField(widget=AdminImageWidget, label='')

    class Meta:
        model = ClassifiedImages
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(ImageClassifiedForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control photo-upload'

#AddClassifiedFormSet = inlineformset_factory(Classified, ClassifiedImages, fields = ['image'], extra=3, can_delete=False, can_order=False,)