from django.contrib import admin
from .models import HazardCategory, HazardLog, CAP


@admin.register(HazardCategory)
class HazardCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "short_description")
    search_fields = ("event__name", "description")

    def short_description(self, obj):
        return (obj.description[:60] + "…") if obj.description and len(obj.description) > 60 else obj.description
    short_description.short_description = "รายละเอียด"


class CAPInline(admin.TabularInline):
    model = CAP
    extra = 0
    fields = ("title", "status", "due_date")
    show_change_link = True


@admin.register(HazardLog)
class HazardLogAdmin(admin.ModelAdmin):
    list_display = (
        "category", "code", "affiliation", "status", "inspect", "initial_risk_level", "residual_risk_level",)
    list_filter = ("category", "status", "inspect", "affiliation")
    search_fields = ("code", "affiliation__name", "assign_to__first_name", "affiliation__short_name")
    date_hierarchy = "date"
    inlines = [CAPInline]


@admin.register(CAP)
class CAPAdmin(admin.ModelAdmin):
    list_display = ("title", "hazard_log", "status", "due_date", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "description", "hazard_log__code")