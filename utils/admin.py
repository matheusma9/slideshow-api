from django.contrib import admin
from .models import Log
from django.contrib.contenttypes.models import ContentType
# Register your models here.

class LogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'data', 'object_id', 'content_type', 'content_object']
admin.site.register(Log, LogAdmin)
admin.site.register(ContentType)