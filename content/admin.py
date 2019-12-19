from django.contrib import admin
from .models import ( Content, Group, Media )  

# Register your models here.
class ContentInLine(admin.TabularInline):
    model = Content

class GroupAdmin(admin.ModelAdmin):
    fields = ('name', )
    inlines = (ContentInLine,)

admin.site.register(Content)
admin.site.register(Group, GroupAdmin)
admin.site.register(Media)