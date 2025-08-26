from django.contrib import admin
from .models import (
    Event, 
    AircraftSystem, 
    FlightPhase, 
    Location, 
    GroundSafetyCategory,
    Aircraft,
    Location,
    Keyword,
)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Show 'name' field in the list display
    search_fields = ('name',)  # Enable search by 'name'


@admin.register(AircraftSystem)
class AircraftSystemAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# @admin.register(FlightPhase)
# class FlightPhaseAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'is_airforce', 'latitude', 'longitude')
    list_filter = ('region', 'is_airforce')  # Add filters for region and airforce
    search_fields = ('name', 'region')  


@admin.register(GroundSafetyCategory)
class GroundSafetyCategoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', )
    list_display_links = ('order', 'name',)
    search_fields = ('name',)

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)

@admin.register(FlightPhase)
class FlightPhaseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)