from django.urls import path

from .views import ConfigListView, ConfigCreateView, ConfigUpdateView

app_name = 'Configurations'
urlpatterns = [
    path('', ConfigListView.as_view(), name='list'),
    path('add/', ConfigCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', ConfigUpdateView.as_view(), name='edit'),
]

