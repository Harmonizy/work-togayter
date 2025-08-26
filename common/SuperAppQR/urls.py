from django.urls import path

# from .views import HubSuperAppView
from .views import HubSuperAppView

app_name = 'SuperAppQR'
urlpatterns = [
    path('hub-super-app/', HubSuperAppView.as_view(), name='hub-super-app'),
    # path('hub-super-app/', hub_super_app_view, name='hub-super-app'),
    # path('hub-super-app/', api_view, name='hub-super-app'),
]
