from datetime import datetime

from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView

from .utils import card_data
from ..models import BaseReport
from ..choices import ReportStatusChoices, ReportTypeChoices
from ..rules import q_condition

from common.RTAFAuth.views import SuperAppLoginMixins
from common.RTAFUser.models import Affiliation



can_view_report = q_condition['report.can_view']

@login_required
def list(request):
    search_query = request.GET.get('search', '').strip()
    date_range = request.GET.get('date_range', '').strip()
    status_filter = request.GET.get('status', '').strip()

    reports = (BaseReport.objects.select_related("recorder", "affiliation", "recorder__rank")
                                 .prefetch_related("file_attachment","image_attachment")
                                 .filter(can_view_report(request.user))
                                 .order_by('-updated_at'))

    report_cards = card_data(reports)
    
    if search_query:
        reports = reports.filter(
            Q(title__icontains=search_query) |
            # Q(description__icontains=search_query) |
            # Q(keyword__name__icontains=search_query) |
            Q(recorder__first_name__icontains=search_query) |
            Q(recorder__last_name__icontains=search_query)
        ).distinct()

    if date_range and " to " in date_range:
        start_str, end_str = date_range.split(" to ", 1)
        try:
            start_date = datetime.strptime(start_str.strip(), "%d %b, %Y").date()
            end_date = datetime.strptime(end_str.strip(), "%d %b, %Y").date()
            reports = reports.filter(event_date__range=(start_date, end_date))
        except ValueError:
            pass  

    if status_filter.isdigit():
        reports = reports.filter(status=int(status_filter))

    
    paginator = Paginator(reports, 10)  # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'report_cards': report_cards,
        'base_reports': page_obj,
        'ReportTypeChoices': ReportTypeChoices,
        "ReportStatusChoices": ReportStatusChoices,
        'search': search_query, 
        'date_range': date_range,
        'status': status_filter,
        'affiliation': Affiliation.objects.all().order_by('short_name'),
    }

    return render(request, 'Report/safety-reports/list.html', context)


class MobileHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'Report/safety-reports/mobile-home.html'
    

@login_required
def mobile_create(request):
    return render(request, 'Report/safety-reports/mobile-create.html')