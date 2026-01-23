from django.contrib import admin
from .models import (
    Event,
    AircraftType,
    Aircraft,
    AircraftSystem,
    FlightPhase,
    Location,
    GroundSafetyCategory,
    Keyword,
    Role
)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # list_display = ("name", "hazard_title")
    # search_fields = ("name", "hazard_title")
    pass


@admin.register(AircraftType)
class AircraftTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ("name", "name_en", "squadron", "type")
    search_fields = ("name", "name_en", "squadron__name")
    list_filter = ("squadron", "type")

    # def squadron_display(self, obj):
    #     return obj.squadron.name if obj.squadron else "-"
    # squadron_display.short_description = "ฝูงบิน"


@admin.register(AircraftSystem)
class AircraftSystemAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(FlightPhase)
class FlightPhaseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "is_airforce", "latitude", "longitude")
    list_filter = ("region", "is_airforce")
    search_fields = ("name",)


@admin.register(GroundSafetyCategory)
class GroundSafetyCategoryAdmin(admin.ModelAdmin):
    list_display = ("order", "name")
    ordering = ("order",)
    search_fields = ("name",)


# @admin.register(Keyword)
# class KeywordAdmin(admin.ModelAdmin):
#     list_display = ("name",)
#     search_fields = ("name",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)