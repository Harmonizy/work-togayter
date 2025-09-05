from django.urls import path

from .views import hazard_log

app_name = 'risk-management'

main_urlpatterns = [    
    path("hazard-log/list/", hazard_log.list, name="hazard_log"),
]

partial_url_patterns = [
   
]

urlpatterns = main_urlpatterns + partial_url_patterns