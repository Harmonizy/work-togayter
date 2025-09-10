from django.urls import path

from .views import hazard_log, hazard_category

app_name = 'risk-management'

main_urlpatterns = [    
    path("hazard-log/list/", hazard_log.list, name="hazard-log"),
    path("hazard-category/list/", hazard_category.list, name="hazard-category.list"),
    path("hazard-log/create/", hazard_log.create, name="hazard-log.create"),
    #     path('hazard/create/', hazard_log_create, name='hazard_log_create'),
    # path('hazard/<int:pk>/edit/', hazard_log_update, name='hazard_log_update'),
]

partial_url_patterns = [
    
]

urlpatterns = main_urlpatterns + partial_url_patterns