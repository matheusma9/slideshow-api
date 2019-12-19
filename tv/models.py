from django.db import models
from utils.models import ModelLog
from utils.ftypes import IMAGE_TYPES

# Create your models here.

class TV(ModelLog):
    """
    Modelo que representa a televisão que exibirá o conteúdo.

    Atributos:
        - name: Nome da Televisão, deve ser único.
        - group: Grupo de conteudos que serão exibidos na televisão.
    """
    name = models.CharField('Nome', max_length=100, unique=True)
    group = models.ForeignKey('content.Group', on_delete=models.SET_NULL, related_name='tvs', null=True)

    class Meta:
        verbose_name = 'Televisão'
        verbose_name_plural = 'Televisões'
        ordering = ['name']  

    @property
    def preview(self):
        return self.group.group_contents.filter(media__ftype__in=IMAGE_TYPES).first()

    def __str__(self):
        return self.name

    