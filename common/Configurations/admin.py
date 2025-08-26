from django.contrib import admin

from .models import Config

admin.site.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description')
    search_fields = ['key', 'description']