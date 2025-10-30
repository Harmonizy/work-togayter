from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib import messages


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
    priority_filter = request.GET.get('priority', '').strip()

    if request.user.has_perm('Report.view_all_report_list'):
        reports = BaseReport.objects.all()
    elif request.user.has_perm('Report.view_affiliation_report_list'):
        reports = BaseReport.objects.filter(affiliation=request.user.affiliation)
    else:
        reports = BaseReport.objects.filter(recorder=request.user)

    reports = (
        reports.select_related("recorder", "affiliation", "recorder__rank")
                .prefetch_related("file_attachment", "image_attachment")
                .order_by("-event_date")
    )

    report_cards = card_data(reports)

    if search_query:
        reports = reports.filter(
            Q(title__icontains=search_query) |
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

    if priority_filter:
        reports = reports.filter(priority=priority_filter)

    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'report_cards': report_cards,
        'base_reports': page_obj,
        'ReportTypeChoices': ReportTypeChoices,
        'ReportStatusChoices': ReportStatusChoices,
        'search': search_query, 
        'date_range': date_range,
        'status': status_filter,
        'priority': priority_filter,
        'affiliation': Affiliation.objects.all().order_by('short_name'),
    }

    return render(request, 'Report/safety-reports/report-list.html', context)


class MobileHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'Report/safety-reports/mobile-home.html'
    

@login_required
def mobile_create(request):
    return render(request, 'Report/safety-reports/mobile-create.html')


@login_required
@permission_required("Report.approve_report", raise_exception=True)
def approve_report(request, report_id):
    """อนุมัติรายงาน"""
    report = get_object_or_404(BaseReport, id=report_id)

    if report.status != ReportStatusChoices.APPROVED:
        report.status = ReportStatusChoices.APPROVED
        report.save()
        messages.success(request, f"อนุมัติรายงาน {report.title} เรียบร้อยแล้ว")
    else:
        messages.info(request, "รายงานนี้ได้รับการอนุมัติแล้ว")

    return redirect("report:safety-report.list")


@login_required
@permission_required("Report.approve_report", raise_exception=True)
def reject_report(request, report_id):
    """ไม่อนุมัติรายงาน"""
    report = get_object_or_404(BaseReport, id=report_id)

    if report.status != ReportStatusChoices.REJECTED:
        report.status = ReportStatusChoices.REJECTED
        report.save()
        messages.warning(request, f"ไม่อนุมัติรายงาน {report.title}")
    else:
        messages.info(request, "รายงานนี้ถูกปฏิเสธไปแล้ว")

    return redirect("report:safety-report.list")