from django.urls import path

from .views import list_air, list_ground, PromotionDetailView, create, edit, delete, quiz_view, quiz_result, publish_promotion, quiz_list, quiz_create, quiz_detail, quiz_update, quiz_delete, accept, quiz_result_modal, publish_modal, publish_dynamic_options, document_list, document_detail, document_create, document_edit, document_delete, document_add_file, document_file_list, document_file_delete

app_name = 'promotion'

main_urlpatterns = [    
    path('list', list_ground, name='list'),
    path('list_ground', list_ground, name='list_ground'),
    path('list_air', list_air, name='list_air'),
    path('detail/<int:pk>/', PromotionDetailView.as_view(), name='detail'),
    path('publish/<int:pk>/', publish_promotion, name='publish_promotion'),
    path('create/', create, name='create'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('delete/<int:pk>/', delete, name='delete'),
    path("accept/<int:pk>/", accept, name="accept"),
    path('publish/partial/<int:pk>/', publish_modal, name='publish_modal'),
    path('publish/dynamic-options/<int:pk>/', publish_dynamic_options, name='publish_dynamic_options'),

    path('quiz/<int:quiz_id>/', quiz_view, name='quiz_view'),
    path('quiz/result/<int:result_id>/', quiz_result, name='quiz_result'),
    path('quiz/list/', quiz_list, name='quiz_list'),
    path('quiz/create/', quiz_create, name='quiz_create'),
    path('quiz/detail/<int:id>/', quiz_detail, name='quiz_detail'),
    path('quiz/update/<int:id>/', quiz_update, name='quiz_update'),
    path('quiz/delete/<int:id>/', quiz_delete, name='quiz_delete'),
    path('quiz/results/partial/<int:quiz_id>/', quiz_result_modal, name='quiz_result_modal'),

    path("documents/", document_list, name="document_list"),
    path("documents/<int:pk>/", document_detail, name="document_detail"),
    path("documents/create/", document_create, name="document_create"),
    path("documents/<int:pk>/edit/", document_edit, name="document_edit"),
    path("documents/<int:pk>/delete/", document_delete, name="document_delete"),
    path("documents/add-file/<int:pk>", document_add_file, name="document_add_file"),
    path("documents/files/<int:pk>", document_file_list, name="document_file_list"),
    path("documents/files/delete/<int:file_id>/", document_file_delete, name="document_file_delete"),


]


partial_url_patterns = [
    
]

urlpatterns = main_urlpatterns + partial_url_patterns

