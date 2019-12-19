from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
class ModelLog(models.Model):
    """
        Classe abstrata para monitoramento de mudanças.
    """
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        abstract = True

class Log(models.Model):
    ACTIONS = (
        ('create', 'Criou'),
        ('update', 'Atualizou'),
        ('delete', 'Removeu')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(verbose_name='Ação', max_length=7, choices=ACTIONS)
    data = models.DateTimeField('Data', auto_now_add=True)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.user.username + ' - ' + self.action + ' - ' + str(self.data)  
    




'''
id do usuário
ação: create/update/delete
data 
id do objeto
contenttype
'''