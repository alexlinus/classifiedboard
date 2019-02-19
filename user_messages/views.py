from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import MessagesForm
from .models import Dialogs
# Create your views here.
from django.http import Http404

def dialog_messages(request, from_user, to_user):
    from_user = User.objects.get(username=from_user)
    to_user = User.objects.get(username=to_user)
    message_form = MessagesForm()
    #Далее мы делаем проверку и выводим ошибку, если пользователь пытается перейти по ссылке диалога, не принадлежащей ему.
    if request.user != from_user:
        raise Http404()
    try:
        try:
            get_dialog = Dialogs.objects.get(first_user=to_user, second_user=from_user)
        except:
            get_dialog = Dialogs.objects.get(first_user=from_user, second_user=to_user)

        print('Сработал get_dialog')
        dialog_items = get_dialog.dialog_messages.all()
        print('Сработал try dialog_items')
        print(dialog_items)
    except:
        dialog_items = None
        print('Сработал Except dialog_items')

    if request.method == 'POST':
        try:
            try:
                dialog = Dialogs.objects.get(first_user=to_user, second_user=from_user)
            except:
                dialog = Dialogs.objects.get(first_user=from_user, second_user=to_user)
        except:
            dialog = Dialogs(first_user=to_user, second_user=from_user)
            dialog.save()

        form = MessagesForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            #Метод save() принимает необязательный именованный аргумент commit, который может иметь значения True или False. Если вы вызовите save() с commit=False, то метод вернёт объект, который ещё не был сохранён в базе данных. В этом случае, вам самостоятельно придётся вызвать метод save() у полученного объекта. Это бывает полезно, когда требуется выполнить дополнительные действия над объектом до его сохранения или если вам требуется воспользоваться одним из параметров сохранения модели. Атрибут commit по умолчанию имеет значение True.
            obj.dialog = dialog
            obj.from_user = from_user
            obj.save()

    return render(request, 'dialog.html', context={'message_form': message_form, 'from_user': from_user, 'to_user': to_user, 'dialog_items': dialog_items})


