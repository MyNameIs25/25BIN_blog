from django.contrib import admin
from . import models


# Register your models here.

class EntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'visited', 'created_time', 'modified_time']


# admin.site.register(models.Category)
# admin.site.register(models.Tag)
admin.site.register(models.ArticleColumn)
admin.site.register(models.Entry, EntryAdmin)

