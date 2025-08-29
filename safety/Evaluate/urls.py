from django.urls import path

from . import views

app_name = 'evaluate'

urlpatterns = [    
    path('evaluate-main/', views.evaluate_main, name='evaluate-main'),
    path('api-next-question/', views.get_next_question, name='get-next-question'),
]

