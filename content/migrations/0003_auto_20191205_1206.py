# Generated by Django 3.0 on 2019-12-05 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20191204_1554'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['group__name', 'order'], 'verbose_name': 'Conteúdo', 'verbose_name_plural': 'Conteúdos'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['name'], 'verbose_name': 'Grupo', 'verbose_name_plural': 'Grupos'},
        ),
        migrations.AlterModelOptions(
            name='media',
            options={'ordering': ['name'], 'verbose_name': 'Mídia', 'verbose_name_plural': 'Mídias'},
        ),
    ]
