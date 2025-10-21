from datetime import datetime
from django.shortcuts import render
from django.db.models import Count

from ..models import CalendarEvent, EventCategory, ThailandHoliday
from safety.Report.models.reports import BaseReport
from safety.Report.choices import ReportStatusChoices, PriorityChoices

def index(request):
    report = BaseReport.objects.all()
    report_all = report.count()
    report_draft = report.filter(status=ReportStatusChoices.DRAFT).count()
    report_approved = report.filter(status=ReportStatusChoices.APPROVED).count()
    report_high = report.filter(priority=PriorityChoices.HIGH).count()
    report_medium = report.filter(priority=PriorityChoices.MEDIUM).count()
    report_low = report.filter(priority=PriorityChoices.LOW).count()

    current_month = datetime.now().month
    context = {
        'report': report,
        'report_all': report_all,
        'report_draft': report_draft,
        'report_approved': report_approved,
        'report_high': report_high,
        'report_medium': report_medium,
        'report_low': report_low,
        'events': CalendarEvent.objects.filter(date__month=current_month).order_by('date','time')
    }
    return render(request, 'Dashboard/home-index.html', context)
