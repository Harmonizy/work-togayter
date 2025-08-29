from django.contrib import admin

from ..models.reports import (
    BaseReport,
    # GroundReport,
    # AviationReport,
    # SafetyReport,
    # SafetyReportAircraftSystem,
    # SafetyReportEvent,
    # SafetyReportFlightPhase
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


# # ---------- Through Table Inlines for SafetyReport ----------
# class SafetyReportAircraftSystemInline(admin.TabularInline):
#     model = SafetyReportAircraftSystem
#     extra = 0


# class SafetyReportFlightPhaseInline(admin.TabularInline):
#     model = SafetyReportFlightPhase
#     extra = 0


# class SafetyReportEventInline(admin.TabularInline):
#     model = SafetyReportEvent
#     extra = 0


# class GroundReportInline(admin.StackedInline):
#     model = GroundReport
#     extra = 0


# class AviationReportInline(admin.StackedInline):
#     model = AviationReport
#     extra = 0


# class SafetyReportInline(admin.StackedInline):
#     model = SafetyReport
#     extra = 0
#     list_select_related = ('squadron', 'aircraft', 'flight', 'event')


# ---------- BaseReport Admin ----------
@admin.register(BaseReport)
class BaseReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'fiscal_year', 'event_date', 'report_type', 'status', 'priority', 'recorder', 'created_at')
    list_editable = ('status',)
    list_filter = ('fiscal_year', 'status', 'report_type')
    search_fields = ('title', 'description', 'comment')
    list_select_related = ('recorder', 'recorder__rank')
    autocomplete_fields = ('recorder',)
    # autocomplete_fields = ('recorder')

    inlines = [ 
            #    GroundReportInline,
            #     AviationReportInline,
            #     SafetyReportInline,
                FileAdminInline,
                ImageAdminInline,
                RecommendationAdminInline]

    # def get_inline_instances(self, request, obj=None):
    #     all_inlines = super().get_inline_instances(request, obj)

    #     # Filter only the inlines that have related objects (or are not part of the ones you want to hide)
    #     filtered_inlines = []
    #     for inline in all_inlines:
    #         model = inline.model
    #         if model in (GroundReport, AviationReport, SafetyReport):
    #             if model.objects.filter(base_report = obj).exists():
    #                 filtered_inlines.append(inline)
    #         else:
    #             # Always include other inlines
    #             filtered_inlines.append(inline)

    #     return filtered_inlines
    