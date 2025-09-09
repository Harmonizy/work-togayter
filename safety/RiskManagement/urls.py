from django.urls import path

from .views import hazard_log, hazard_category

app_name = 'risk-management'

main_urlpatterns = [    
    path("hazard-log/list/", hazard_log.list, name="hazard_log"),
    path("hazard-category/list/", hazard_category.list, name="hazard_category.list"),
]

partial_url_patterns = [
    
]

urlpatterns = main_urlpatterns + partial_url_patterns