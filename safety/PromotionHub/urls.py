from django.urls import path

from .views import list, PromotionDetailView, create, edit, delete, quiz_view, quiz_result

app_name = 'promotion'

main_urlpatterns = [    
    path('', list, name='list'),
    path('detail/<int:pk>/', PromotionDetailView.as_view(), name='detail'),
    path('create/', create, name='create'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('delete/<int:pk>/', delete, name='delete'),

    path('quiz/<int:quiz_id>/', quiz_view, name='quiz_view'),
    path('quiz/result/<int:result_id>/', quiz_result, name='quiz_result'),
]

partial_url_patterns = [
    
]

urlpatterns = main_urlpatterns + partial_url_patterns

