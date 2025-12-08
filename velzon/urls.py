from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.shortcuts import render

from debug_toolbar.toolbar import debug_toolbar_urls

from common.RTAFAuth.views import AFLoginView

blank = TemplateView.as_view(template_name="blank.html")

# from common.RTAFAuth.views import AFLoginView
from common.Services.secure_media_files import serve_secure_media

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.index_title = settings.ADMIN_INDEX_TITLE
admin.site.site_title = settings.ADMIN_SITE_TITLE

def redirect_by_screen_size(request):
    return render(request, 'redirect-by-size.html')

safe_urls = [
    path('', include('safety.Report.urls')),
    path('risk-management/', include('safety.RiskManagement.urls')),
    path('safety-dashboard/', include('safety.Dashboard.urls')),
    path('safety-evaluate/', include(('safety.Evaluate.urls'))),
    path('promotion/', include('safety.PromotionHub.urls')),

    path("select2/", include("django_select2.urls")),
]


urlpatterns = [
    path(settings.ADMIN_URL_PATH, admin.site.urls),
    path('media/<path:path>/', serve_secure_media, name='secure_media'),

    path('redirect-by-size/', redirect_by_screen_size, name='redirect-by-size'),

    path('login/', AFLoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),

    path('blank/', blank, name="blank"),
    path('dashboard/',include('dashboards.urls')),
    path('apps/',include('apps.urls')),
    path('layouts/',include('layouts.urls')),
    path('components/',include('components.urls')),
    path('pages/',include('pages.urls')),
    path('tinymce/', include('tinymce.urls')),

] + safe_urls + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
