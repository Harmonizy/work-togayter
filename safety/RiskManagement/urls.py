from django.urls import path

from .views import hazard_log, hazard_edit, hazard_detail

app_name = 'risk_management'

main_urlpatterns = [    
    path("hazard-log/list/", hazard_log.list, name="hazard-log"),
    path("hazard-log/detail/<int:id>", hazard_detail.main, name="hazard-detail"),
    path("hazard-log/create/", hazard_log.create, name="hazard-log-create"),
    path("hazard-edit/update/<int:pk>/", hazard_edit.update, name="hazard-edit.update"),
    path("hazards/delete/<int:pk>/", hazard_log.delete, name="hazard-delete"),  
    

    # path("hazard-log/category/", hazard_category.list, name="hazard-category.list"),
]

partial_url_patterns = [
    
]

urlpatterns = main_urlpatterns + partial_url_patterns

