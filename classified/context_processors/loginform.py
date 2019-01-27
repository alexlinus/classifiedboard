from allauth.account.forms import LoginForm

#Здесь мы импортируем форму для логирования из django allauth, чтобы использовать во всех шаблонах, как context_proccessors
def login_form_tag(request):
    login_form = LoginForm()
    return {'login_form': login_form}