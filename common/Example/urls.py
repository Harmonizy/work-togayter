from django.urls import path

from .views.pages import feedback_view


urlpatterns = [
    path('feedback/', feedback_view, name='feedback'),
]