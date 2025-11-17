from django.urls import path

from .views import list, PromotionDetailView, create, edit, delete, quiz_view, quiz_result, publish_form, publish_unit_form, publish_promotion

app_name = 'promotion'

main_urlpatterns = [    
    path('', list, name='list'),
    path('detail/<int:pk>/', PromotionDetailView.as_view(), name='detail'),
    path('create/', create, name='create'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('delete/<int:pk>/', delete, name='delete'),

    path('quiz/<int:quiz_id>/', quiz_view, name='quiz_view'),
    path('quiz/result/<int:result_id>/', quiz_result, name='quiz_result'),
    path('publish/form/<int:pk>/', publish_form, name='publish_form'),
    path('publish/unit/form/<int:pk>/', publish_unit_form, name='publish_unit_form'),
    path('publish/<int:pk>/', publish_promotion, name='publish_promotion'),
]


partial_url_patterns = [
    
]

urlpatterns = main_urlpatterns + partial_url_patterns

