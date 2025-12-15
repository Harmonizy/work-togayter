from django.urls import path

from .views.Promotion import promotion_accept, promotion_create, promotion_delete, promotion_detail, promotion_edit, promotion_list, promotion_publish
from .views.Quiz import quiz_create, quiz_view, quiz_delete, quiz_detail, quiz_list, quiz_result, quiz_update
from .views.Document import document_list, document_detail, document_create, document_edit, document_delete, document_file

app_name = 'promotion'

main_urlpatterns = [    
    path('list_ground', promotion_list.list_ground, name='list_ground'),
    path('list_air', promotion_list.list_air, name='list_air'),

    path('create_ground/', promotion_create.create_ground, name='create_ground'),
    path('create_air/', promotion_create.create_air, name='create_air'),

    path('detail/<int:pk>/', promotion_detail.PromotionDetailView.as_view(), name='detail'),
    path('publish/<int:pk>/', promotion_publish.publish_promotion, name='publish_promotion'),
    path('edit/<int:pk>/', promotion_edit.edit, name='edit'),
    path('delete/<int:pk>/', promotion_delete.delete, name='delete'),
    path('accept/<int:pk>/', promotion_accept.accept, name="accept"),
    path('publish/partial/<int:pk>/', promotion_publish.publish_modal, name='publish_modal'),
    path('publish/dynamic-options/<int:pk>/', promotion_publish.publish_dynamic_options, name='publish_dynamic_options'),

    path('quiz/<int:quiz_id>/', quiz_view.view, name='quiz_view'),
    path('quiz/result/<int:result_id>/', quiz_result.result, name='quiz_result'),
    path('quiz/list/', quiz_list.list, name='quiz_list'),
    path('quiz/create/', quiz_create.create, name='quiz_create'),
    path('quiz/detail/<int:id>/', quiz_detail.detail, name='quiz_detail'),
    path('quiz/update/<int:id>/', quiz_update.update, name='quiz_update'),
    path('quiz/delete/<int:id>/', quiz_delete.delete, name='quiz_delete'),
    path('quiz/results/partial/<int:quiz_id>/', quiz_list.result_modal, name='quiz_result_modal'),

    path("document/", document_list.list, name="document_list"),
    path("document/<int:pk>/", document_detail.detail, name="document_detail"),
    path("document/create/", document_create.create, name="document_create"),
    path("document/<int:pk>/edit/", document_edit.edit, name="document_edit"),
    path("document/<int:pk>/delete/", document_delete.delete, name="document_delete"),
    path("document/add-file/<int:pk>", document_file.add_file, name="document_add_file"),
    path("document/files/<int:pk>", document_file.file_list, name="document_file_list"),
    path("document/files/delete/<int:file_id>/", document_file.file_delete, name="document_file_delete"),

    path("announcement/", promotion_list.announcement_list, name="announcement_list"),
    path("announcement/create/", promotion_create.announcement_create, name="announcement_create"),
]


partial_url_patterns = [
    
]

urlpatterns = main_urlpatterns + partial_url_patterns

