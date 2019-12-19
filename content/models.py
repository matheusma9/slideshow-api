from django.db import models
from utils.models import ModelLog
import utils.ftypes as ftypes

# Create your models here.

class Group(ModelLog):
    """
    Modelo que representa o grupo de conteúdos que serão exibidos em uma Tv.

    Atributos:
        - nome: Nome do grupo.
        - contents: Os conteúdos do grupo.
    """
    name = models.CharField('Nome', max_length=100, unique=True)
    contents = models.ManyToManyField('content.Media', through='content.Content', related_name='groups')

    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['name']
    
    

class Content(ModelLog):
    """
    Modelo que representa o conteúdo que será exibido em um grupo.

    Atributos:
        - media: A mídia do conteúdo.
        - group: O grupo onde o conteúdo será exibido. 
        - duration: A duração da exibição.
        - order: A ordem de exibição.
    """
    media = models.ForeignKey('content.Media', on_delete=models.CASCADE, related_name='contents')
    group = models.ForeignKey('content.Group', on_delete=models.CASCADE, related_name='group_contents')
    duration = models.DurationField('Duração')
    order = models.PositiveIntegerField('Ordem')

    class Meta:
        verbose_name = 'Conteúdo'
        verbose_name_plural = 'Conteúdos'
        ordering = ['group__name', 'order']

    def __str__(self):
        return str(self.order) + ' - ' +self.group.name + ' - ' + self.media.name
    
    
    
class Media(ModelLog):
    """
    Modelo que representa o arquivo de mídia que será exibido.
    
    Atributos:
        - nome: Nome da mídia, deve ser único.
        - source: O arquivo de mídia.
        - ftype: Tipo da mídia.
    """
    name = models.CharField('Nome', max_length=100, unique=True)
    source = models.FileField('Arquivo', upload_to='content/media/')
    ftype = models.CharField('Tipo', max_length=10, choices=ftypes.TYPES)

    class Meta:
        verbose_name = 'Mídia'
        verbose_name_plural = 'Mídias'
        ordering = ['name']

    def __str__(self):
        return self.name

    
