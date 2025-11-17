from django.urls import path

from .views import list, PromotionDetailView, create, edit, delete, quiz_view, quiz_result, publish_promotion, quiz_list, quiz_create, quiz_detail, quiz_update, quiz_delete

app_name = 'promotion'

main_urlpatterns = [    
    path('', list, name='list'),
    path('detail/<int:pk>/', PromotionDetailView.as_view(), name='detail'),
    path('create/', create, name='create'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('delete/<int:pk>/', delete, name='delete'),

    path('quiz/<int:quiz_id>/', quiz_view, name='quiz_view'),
    path('quiz/result/<int:result_id>/', quiz_result, name='quiz_result'),
    path('publish/<int:pk>/', publish_promotion, name='publish_promotion'),
    path('quiz/list', quiz_list, name='quiz_list'),
    path('quiz/create/', quiz_create, name='quiz_create'),
    path('quiz/detail/<int:id>/', quiz_detail, name='quiz_detail'),
    path('quiz/update/<int:id>/', quiz_update, name='quiz_update'),
    path('quiz/delete/<int:id>/', quiz_delete, name='quiz_delete'),
]


partial_url_patterns = [
    
]

urlpatterns = main_urlpatterns + partial_url_patterns

