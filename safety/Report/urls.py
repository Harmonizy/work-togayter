from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from safety.Report.views import safety_form_partials

from .views import  safety_report, safety_overviews, safety_create,safety_edit, word_export, safety_delete 
# from .views import safety_create

app_name = 'report'

main_urlpatterns = [
    # path('desktop-home/', safety_report.list, name='safety-desktop-home'),

    path('', safety_report.list, name='safety-report.home'),
    path('safety-report/list', safety_report.list, name='safety-report.list'),
    path('safety-overviews/main-page/<int:base_report_id>/', safety_overviews.main_page, name='safety-overviews.main-page'),

    path('safety-create/new-report/', safety_create.new_report, name='safety-create.new_report'),   
    path('safety-edit/edit-report/<int:report_id>/', safety_edit.edit_report, name='safety-edit.edit-report'),
    path("delete/<int:pk>/", safety_delete.delete_report, name="delete"),
    
    # export
    path('word-export/safety-doc/<int:pk>/', word_export.safety_doc, name='word_export.safety_doc'),

    # form
    # path('create-safety-report/<str:report_type>/', create.create_report, name='create.create_report'),

    # mobile
    # path('mobile-home/', safety_report.mobile_home, name='mobile_home'),
    # path('mobile-create/', safety_report.mobile_create, name='mobile_create'),
]


partial_url_patterns = [
    path('safety-form-partials/base-title-air-ground/', safety_form_partials.base_title_air_ground, name='safety-form-partials.base-title-air-ground'),
]

urlpatterns = main_urlpatterns + partial_url_patterns