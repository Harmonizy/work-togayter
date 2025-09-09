from django.contrib import admin

from .models import EventCategory, CalendarEvent, ThailandHoliday


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'category')
    list_filter = ('date', 'category')
    search_fields = ('title', 'description')


@admin.register(ThailandHoliday)
class ThailandHolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    search_fields = ('name', 'description')
    ordering = ('date',)
