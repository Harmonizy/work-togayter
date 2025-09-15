from django.urls import path

from . import views

app_name = 'evaluate'


urlpatterns = [    
    path('evaluate-main/<int:report_id>/<int:question_id>/', views.evaluate_main, name='evaluate-main'),
    path('evaluate-main/<int:report_id>/', views.evaluate_main, name='evaluate-main'),
    path('api-current-question/', views.get_current_question, name='api-current-question'),
    path('api-next-question/', views.get_next_question, name='api-next-question'),
    
    path('api-submit-evaluation/', views.submit_evaluation, name='api-submit-evaluation'),
    
]

