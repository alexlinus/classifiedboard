from django.db import models
from django.conf import settings

# Create your models here.
class Dialogs(models.Model):
    first_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='income_dialogs')
    second_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='outcome_dialogs')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'

class Messages(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_messages', verbose_name='От кого')
    message_body = models.TextField(max_length=250, verbose_name='Текст сообщения')
    message_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата сообщения')
    dialog = models.ForeignKey(Dialogs, verbose_name='Диалог', default=None, blank=True, null=True, related_name='dialog_messages', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' ' + str(self.message_date)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['message_date']

