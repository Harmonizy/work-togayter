from django.contrib import admin

from ..models.reports import (
    BaseReport,
    GroundReport,
    AviationReport,
    Participant,
    ReferenceReport,
)

from ..models.attachments import File, Image, Recommendation


class FileAdminInline(admin.TabularInline):
    model = File
    extra = 0

class ImageAdminInline(admin.TabularInline):
    model = Image
    extra = 0

class RecommendationAdminInline(admin.TabularInline):
    model = Recommendation
    extra = 0


class GroundReportInline(admin.StackedInline):
    model = GroundReport
    extra = 0


class AviationReportInline(admin.StackedInline):
    model = AviationReport
    extra = 0


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0
    autocomplete_fields = ['role']
    fields = ['full_name', 'role', 'injury_level', 'note']


class ReferenceReportInline(admin.TabularInline):
    model = ReferenceReport
    extra = 0
    autocomplete_fields = ['report']
    fields = ['report', 'note']
    fk_name = 'base_report'


# ---------- BaseReport Admin ----------
@admin.register(BaseReport)
class BaseReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'fiscal_year', 'event_date', 'report_type', 'status', 'priority', 'recorder', 'created_at')
    list_editable = ('status',)
    list_filter = ('fiscal_year', 'status', 'report_type')
    search_fields = ('title',)
    list_select_related = ('recorder', 'recorder__rank')
    autocomplete_fields = ('recorder',)
    # autocomplete_fields = ('recorder')

    inlines = [ 
                GroundReportInline,
                AviationReportInline,
                ParticipantInline,
                ReferenceReportInline,
                FileAdminInline,
                ImageAdminInline,
                RecommendationAdminInline]
    
    def get_inline_instances(self, request, obj=None):
        all_inlines = super().get_inline_instances(request, obj)

        # Filter only the inlines that have related objects (or are not part of the ones you want to hide)
        filtered_inlines = []
        for inline in all_inlines:
            model = inline.model
            if model in (GroundReport, AviationReport):
                if model.objects.filter(base_report = obj).exists():
                    filtered_inlines.append(inline)
            else:
                # Always include other inlines
                filtered_inlines.append(inline)

        return filtered_inlines


@admin.register(GroundReport)
class GroundReportAdmin(admin.ModelAdmin):
    list_display = (
        'base_report', 
        'location', 
        'category',
        'get_title',
        'get_report_type',
        'get_event_date'
    )
    list_filter = ('category',)
    search_fields = ('location', 'base_report__title')

    def get_title(self, obj):
        return obj.base_report.title
    get_title.short_description = "ชื่อรายงาน"

    def get_report_type(self, obj):
        return obj.base_report.get_report_type_display()
    get_report_type.short_description = "ประเภท"

    def get_event_date(self, obj):
        return obj.base_report.event_date
    get_event_date.short_description = "วันที่เกิดเหตุ"


@admin.register(AviationReport)
class AviationReportAdmin(admin.ModelAdmin):
    list_display = (
        'base_report', 
        'squadron', 
        'aircraft',
        'get_title',
        'get_report_type',
        'get_event_date'
    )
    list_filter = ('squadron', 'aircraft', 'system', 'flight_phase')
    search_fields = ('base_report__title', 'squadron__name', 'aircraft__name')
    filter_horizontal = ('system', 'flight_phase')

    def get_title(self, obj):
        return obj.base_report.title
    get_title.short_description = "ชื่อรายงาน"

    def get_report_type(self, obj):
        return obj.base_report.get_report_type_display()
    get_report_type.short_description = "ประเภท"

    def get_event_date(self, obj):
        return obj.base_report.event_date
    get_event_date.short_description = "วันที่เกิดเหตุ"


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('base_report', 'full_name', 'role', 'injury_level', 'note')
    search_fields = ('base_report__title', 'full_name', 'role__name')


@admin.register(ReferenceReport)
class ReferenceReportAdmin(admin.ModelAdmin):
    list_display = ('base_report', 'report', 'note')
    search_fields = ('base_report__title', 'report__title')