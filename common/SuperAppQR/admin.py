import json

from django.contrib import admin
from .models import QRType, QRImageData, QRScan


@admin.register(QRType)
class QRTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'url_redirect', 'create_by', 'create_at']
    search_fields = ['name', 'description']
    list_filter = ['create_at']
    readonly_fields = ['create_at']
    autocomplete_fields = ['create_by']


class QRScanInline(admin.TabularInline):
    model = QRScan
    extra = 0
    readonly_fields = ['scanner', 'scan_time']
    can_delete = False


@admin.register(QRImageData)
class QRImageDataAdmin(admin.ModelAdmin):
    list_display = ['type', 'object_id', 'token', 'args_data']
    list_display_links = ['type', 'object_id']
    # search_fields = ['id', 'type__name']
    # list_filter = ['type']
    # inlines = [QRScanInline]
    def args_data(self, obj):
        return json.dumps(obj.args) if obj.args else '-'


@admin.register(QRScan)
class QRScanAdmin(admin.ModelAdmin):
    list_display = ['qr_image_data__type', 'scanner', 'scan_time']
    date_hierarchy = 'scan_time'    
    list_filter = ['scan_time',]
    search_fields = [ 'scanner__first_name', 'scanner__affiliation__short_name']
    readonly_fields = ['scan_time']
    list_select_related = ['scanner', 'qr_image_data__type', 'scanner__affiliation']
