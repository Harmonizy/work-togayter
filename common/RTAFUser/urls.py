from django.urls import include, path

from .views import forms as user_forms
from .views import pages

app_name = 'RTAFUser'
urlpatterns = [    
    path('create/', user_forms.RTAFUserCreateView.as_view(), name='create'),
    path('affiliation/', pages.AffiliationListView.as_view(), name='affiliation_list'),
    path('affiliation/<int:pk>/', pages.AffiliationDetailView.as_view(), name='affiliation_detail'),
    path('affiliation-update/<int:pk>/', pages.AffliationUpdateView.as_view(), name='affiliation_update'),
    path('affiliation-create/', pages.AffiliationCreateView.as_view(), name='affiliation_create'),
]
