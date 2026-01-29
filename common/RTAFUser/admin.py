from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.models import LogEntry
from django.db.models.query import QuerySet
from django.db.models import Q
from django.http import HttpRequest
# from rest_framework.authtoken.admin import TokenAdmin

from .models import Rank, Affiliation, RTAFUser, Squadron, AffiliationAircraft

# TokenAdmin.raw_id_fields = ['user']


# @admin.register(LogEntry)
# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag')
#     search_fields = ('object_repr', 'user__username')
#     list_filter = ('action_flag',)

# @admin.register(Permission)
# class PermissionAdmin(admin.ModelAdmin):
#     list_display = ('name', 'content_type', 'codename', 'data_code_name')
#     search_fields = ('name', 'codename')
#     list_filter = ('content_type',)

#     def data_code_name(self, obj):
#         return obj.content_type.app_label.lower() + '.' + obj.codename
#     data_code_name.short_description = 'data.code_name'

admin.site.unregister(Group)

@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    list_display = ('name', 'description') 
    search_fields = ('name',) 


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'full_name', 'id', 'level', 'short_display', 'is_airforce')
    search_fields = ('short_name', 'full_name')
    list_filter = ('is_airforce',)
    save_as = True

class AffiliationAircraftInline(admin.TabularInline):
    model = AffiliationAircraft
    extra = 1

@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    list_display = ('hris_code', 'short_name', 'full_name', 'is_airbase',)
    list_display_links = ('short_name', 'full_name')
    list_editable = ('is_airbase',)
    search_fields = ('short_name', 'full_name')
    list_filter = ('is_airbase','is_rtaf_directed',)
    raw_id_fields = ()
    inlines = [AffiliationAircraftInline]


@admin.register(RTAFUser)
class RTAFUserAdmin(UserAdmin):
    list_display = ('username', 'get_full_name', 'position', 'affiliation', 'last_login',)
    list_display_links = ('username', 'get_full_name')
    search_fields = ('af_id', 'person_id', 'first_name', 'last_name', 'position', 'username')
    list_filter = ('groups', 'affiliation',)
    raw_id_fields = ('rank', 'affiliation', 'work_affiliation')
    list_select_related = ('rank', 'affiliation', 'work_affiliation')
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('ข้อมูลบุคคล', {
            'fields': ('af_id', 'person_id','rank', 'first_name', 'last_name', 'email',  'position')
        }),
        ('สังกัด', {
            'fields': ('affiliation', 'work_affiliation')
        }),
        ('สิทธิ์', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    ordering = ('-last_login',)

    def get_queryset(self, request: HttpRequest) -> QuerySet:    
        queryset = super().get_queryset(request)
        query = request.GET.get('q')
        if query:
            if len(query.split(" ")) > 1:
                return queryset.filter(Q(first_name__icontains=query.split(" ")[0]) & Q(last_name__icontains=query.split(" ")[1]))
        return queryset
        
@admin.register(Squadron)
class SquadronAdmin(admin.ModelAdmin):
    list_display = ('code', 'affiliation', 'nickname')
    list_filter = ('affiliation',)
    search_fields = ('code', 'nickname')
    

@admin.register(AffiliationAircraft)
class AffiliationAircraftAdmin(admin.ModelAdmin):
    list_display = ('affiliation', 'aircraft')
    search_fields = ('affiliation__model', 'aircraft__name')