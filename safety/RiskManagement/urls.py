from django.urls import path

from .views import hazard_log, hazard_edit, hazard_detail, hazard_category, cap_delete, cap_edit

app_name = 'risk_management'

main_urlpatterns = [    
    path("hazard-log/list/", hazard_log.list, name="hazard-log"),
    path("hazard-log/detail/<int:id>", hazard_detail.main, name="hazard-detail"),
    
    path("hazard-log/create/", hazard_log.create, name="hazard-log-create"),
    path("hazard-log/create-by-report/<int:report_id>/", hazard_log.create_by_report, name="hazard-log.create-by-report"),
    path("hazard/<int:hazard_id>/cap/create/", hazard_log.handle_create_cap, name="hazard-log.cap-create"),
    
    path("hazard-edit/update/<int:pk>/", hazard_edit.update, name="hazard-edit.update"),
    
    path("hazards/delete/<int:pk>/", hazard_log.delete, name="hazard-delete"),  
    
    path("cap/edit/<int:cap_id>/", cap_edit.cap_edit, name="cap_edit"),
    path("cap/delete/<int:cap_id>/", cap_delete.cap_delete_view, name="cap_delete"),
    

    # path("hazard-log/category/", hazard_category.list, name="hazard-category.list"),
]

partial_url_patterns = [
    
]

urlpatterns = main_urlpatterns + partial_url_patterns

