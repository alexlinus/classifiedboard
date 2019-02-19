from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Classified, ClassifiedImages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import AddClassifiedForm, ImageClassifiedForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.forms import modelformset_factory
from allauth.account.forms import SignupForm
from django.shortcuts import reverse
# Create your views here.
from django.http import HttpResponseRedirect, JsonResponse

def home(request):
    classifieds = Classified.objects.all()
    #Сортируем далее по убыванию просмотров.
    most_viewed = Classified.objects.order_by('-views')[:6]
    return render(request, 'home.html', context={'classifieds': classifieds, 'most_viewed': most_viewed})


def get_classified(request, classified_slug):
    classified = get_object_or_404(Classified, slug=classified_slug)
    user = User.objects.get(username=classified.author)
    user_classifieds = user.classifieds.exclude(title=classified.title)[:3] #Здесь мы исключили из списка queries объект с текущим объявлением. Для вывода объявлений пользователя.

    #Здесь мы в сессии проверяем есть ли по ключу для каждогог товара в сессии значение, если нет, то создаем это значение views_slug_издесьидетслагтовара
    #Тем самым мы делаем так, чтобы 1 человек не накручивал просмотры. Но можно будет отключить куки, и делать так же как и на blive накручивать просмотры.
    try:
        views_slug = request.session['views_slug_{}'.format(classified_slug)]
    except:
        request.session['views_slug_{}'.format(classified_slug)] = classified_slug
        classified.views +=1
        classified.save()

# Здесь мы перебираем изображения и добавляем их словарь, с добавлением индекса через count. Чтобы выделить первое изображение, и сделать его в слайдере активным.
    item_images = {}
    count = 1
    for image in classified.images.all():
        item_images[count] = image.get_src
        count +=1

    return render(request, 'classified_detail.html', context={'classified': classified, 'item_images': item_images, 'user_classifieds': user_classifieds})


def search(request):
    search_query = request.GET.get('search-classified', '')
    user = request.GET.get('user')
    print(user)
    if search_query:
        search_classifieds = Classified.objects.filter(title__icontains=search_query)
        context = {'search_classifieds': search_classifieds, 'search_query': search_query}
    else:
        context = {'search_classifieds': '', 'search_query': 'Вы не ввели запрос!'}
    return render(request, 'search_detail.html', context)


def add_classified(request):
    ImageFormset = modelformset_factory(ClassifiedImages, form=ImageClassifiedForm, fields=('image',), extra=1)
    if request.is_ajax():
        formset = ImageFormset(request.POST, request.FILES)
        print(request.FILES)
        for f in formset.cleaned_data:
            print(f['image'])
        return JsonResponse({'new_image_url': 'DONE'})
    else:
        if request.method == 'POST':
            form = AddClassifiedForm(request.POST)
            formset = ImageFormset(request.POST or None, request.FILES or None)
            if form.is_valid() and formset.is_valid():
                classified = form.save(commit=False)
                classified.author = request.user
                classified.save()
                print(formset.cleaned_data)
                for f in formset.cleaned_data:
                    try:
                        f['image']
                        #РАБОТАЕТ, НО НУЖНО РАЗОБРАТЬСЯ, ПОЧЕМУ ДУБЛИРУЕТ ИЗОБРАЖЕНИе. ЕСЛИ ОДНО НЕ ЗАПОЛНЕНО.
                        photo = ClassifiedImages(classified=classified, image=f['image'])
                        photo.save()
                    except Exception as e:
                        print('Ошибка')

                return redirect(classified)
        else:
            form = AddClassifiedForm()
            formset = ImageFormset(queryset=ClassifiedImages.objects.none())
            context = {
                'form': form,
                'formset': formset,
            }
            return render(request, 'add_classified.html', context)


def get_register(request):
    register_form = SignupForm()
    return render(request, 'signup.html', context={'register_form': register_form})


def get_user_classifieds(request):
    if request.user.is_authenticated:
        user_classifieds_all = Classified.objects.filter(author=request.user)
        classifieds_paginator = Paginator(user_classifieds_all, 6)
        page = request.GET.get('page')
        try:
            user_classifieds = classifieds_paginator.page(page)
        except:
            user_classifieds = classifieds_paginator.page(1)

        current_page = user_classifieds.number - 1  # возвращает минимум 1, а так как у нас индексы с 0 начинаются, ,поэтому отнимаем 1
        start_index = current_page - 3
        if start_index < 0:
            start_index = 0
        max_pages = classifieds_paginator.num_pages  # то же самое как и с currentp_page4
        end_index = current_page + 3
        if end_index > max_pages:
            end_index = max_pages
        page_range = list(classifieds_paginator.page_range)[start_index:end_index]

        return render(request, 'user_classifieds.html', context={'user_classifieds': user_classifieds, 'page_range': page_range})
    else:
        raise Http404


def classified_edit(request, classified_slug):
    if request.user.is_authenticated:
        classified = Classified.objects.get(slug=classified_slug)
        ImageFormset = modelformset_factory(ClassifiedImages, form=ImageClassifiedForm, fields=('image',), extra=1)

        if request.is_ajax() and request.user == classified.author:
            formset = ImageFormset(request.POST, request.FILES)
            print('Сейчас будет request files')
            print(request.FILES)
            print('А далее f in formset.cleaned_data')
            for f in formset.cleaned_data:
                print(f)
            for f in formset.cleaned_data:
                try:
                    is_image = ClassifiedImages.objects.filter(classified=classified, image__iexact=f['image']).exists()
                except:
                    is_image = True
                if not is_image:
                    try:
                        photo = ClassifiedImages(classified=classified, image=f['image'])
                        photo.save()
                    except Exception as e:
                        print('Ошибка')
            print(photo.get_src)
            return JsonResponse({'new_image_url': photo.get_src})
        else:
            if request.user == classified.author:
                if request.method == 'GET':
                    form = AddClassifiedForm(instance=classified)
                    formset = ImageFormset(queryset=classified.images.all())
                if request.method == 'POST':
                    form = AddClassifiedForm(request.POST, instance=classified)
                    formset = ImageFormset(request.POST, request.FILES)
                    if form.is_valid() and formset.is_valid():
                        updated_classified = form.save()
                        for f in formset.cleaned_data:
                            try:
                                is_image = ClassifiedImages.objects.filter(classified=classified, image__iexact=f['image']).exists()
                            except:
                                is_image = True
                            if not is_image:
                                try:
                                    photo = ClassifiedImages(classified=classified, image=f['image'])
                                    photo.save()
                                except Exception as e:
                                    print('Ошибка')
                        return redirect(updated_classified)

            return render(request, 'edit_classified.html', context={'form': form, 'formset': formset, 'classified': classified})

def classified_delete(request, classified_slug):
    classified = get_object_or_404(Classified, slug=classified_slug)
    classified.delete()
    return redirect(get_user_classifieds)

