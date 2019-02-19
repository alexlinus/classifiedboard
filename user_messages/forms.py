from django.forms import ModelForm
from .models import Messages


class MessagesForm(ModelForm):
    class Meta:
        model = Messages
        exclude = ['message_date', 'from_user', 'dialog']
