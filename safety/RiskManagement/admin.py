from django.contrib import admin
from .models import HazardLog, CAP


class CAPInline(admin.TabularInline):
    model = CAP
    extra = 0
    fields = ("title", "status", "assign_to", "due_date", "verification_date")
    raw_id_fields = ("assign_to",)
    show_change_link = True


@admin.register(HazardLog)
class HazardLogAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "get_event_name",
        "affiliation",
        "status",
        "investigation_type",
        "init_likelihood",
        "init_severity",
        "init_risk_lv",
        "res_likelihood",
        "res_severity",
        "res_risk_lv",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "status",
        "investigation_type",
        "affiliation",
        ("created_at", admin.DateFieldListFilter),
        ("updated_at", admin.DateFieldListFilter),
    )
    search_fields = (
        "code",
        "desc",
        "event__name",
        "affiliation__name",
        "caps__event",
        "caps__desc",
        "caps__assign_to__first_name",
        "caps__assign_to__last_name",
    )
    ordering = ("-updated_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("event", "affiliation")
    inlines = [CAPInline]

    @admin.display(description="เหตุการณ์")
    def get_event_name(self, obj):
        return getattr(obj.event, "name", "-")


@admin.register(CAP)
class CAPAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "hazard_log",
        "status",
        "assign_to",
        "due_date",
        "verification_date",
        "created_at",
    )
    list_filter = (
        "status",
        ("due_date", admin.DateFieldListFilter),
        ("verification_date", admin.DateFieldListFilter),
        "assign_to",
    )
    search_fields = (
        "title",
        "desc",
        "hazard_log__code",
        "hazard_log__title__name",
        "assign_to__first_name",
        "assign_to__last_name",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("hazard_log", "assign_to")