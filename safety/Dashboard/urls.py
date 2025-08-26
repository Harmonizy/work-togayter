from django.urls import path

from .views import dashboard_home

app_name = 'safety-dashboard'
urlpatterns = [
    path('home/index', dashboard_home.index, name='dashboard-home.index'),
]

