from django.urls import path

from .views import dashboard_home
from .apis import apis

app_name = 'safety-dashboard'
urlpatterns = [
    path('home/index', dashboard_home.index, name='dashboard-home.index'),
    path('apis/get-cap_data_api', apis.cap_data_api, name='cap_data_api.apis.cap_data_api'),
]

