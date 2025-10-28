from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import  report_list, report_create, report_create_officer, report_delete, report_details, report_edit, word_export
# from .views import safety_create

app_name = 'report'

main_urlpatterns = [
    # path('desktop-home/', safety_report.list, name='safety-desktop-home'),

    path('', report_list.list, name='safety-report.home'),
    path('safety-report/list/', report_list.list, name='safety-report.list'),
    path("safety-report/detail/<int:pk>/", report_details.main_page, name="safety-report.detail"),
    path("safety-report/approve/<int:report_id>/", report_list.approve_report, name="report.approve"),
    path("safety-report/reject/<int:report_id>/", report_list.reject_report, name="report.reject"),

    path('safety-create/new-report/', report_create.new_report, name='safety-create.new_report'),   
    path('safety-create-officer/new-report/', report_create_officer.new_report, name='safety-create-officer.new_report'),  
    path('safety-edit/edit-report/<int:report_id>/', report_edit.edit_report, name='safety-edit.edit-report'),
    path("delete/<int:pk>/", report_delete.delete_report, name="delete"),

    # path('safety-create/create-report/<>', safety_create.create_report, name='safety_create.create_report'),
    
    # export
    path('word-export/safety-doc/<int:pk>/', word_export.safety_doc, name='word_export.safety_doc'),
    path('word-export/rtaf-message-form/<int:base_report_id>/', word_export.rtaf_message_form, name='word_export.rtaf_message_form'),

    # form
    # path('create-safety-report/<str:report_type>/', create.create_report, name='create.create_report'),

    # mobile
    path('mobile-home/', report_list.MobileHomeView.as_view(), name='mobile_home'),
    path('mobile-create/', report_list.mobile_create, name='mobile_create'),

    
]


partial_url_patterns = [
    
]

urlpatterns = main_urlpatterns + partial_url_patterns