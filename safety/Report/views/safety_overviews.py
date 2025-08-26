from datetime import date, timedelta

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Count, Q

from ..models import BaseReport
from ..choices import ReportTypeChoices


def main_page(request, base_report_id):
    base_report = BaseReport.objects.get(id=base_report_id)
    data_report = None
    template_name = 'Report/safety-overviews/main-page.aviation-report.html'
    
    
    # if hasattr(base_report, 'safetyreport'):
    #     data_report = base_report.safetyreport
    #     template_name += 'safety-report.html'
    # elif hasattr(base_report, 'AviationReport'):
    #     data_report = base_report.AviationReport
    #     template_name += 'aviation-report.html'
    # elif hasattr(base_report, 'GroundReport'):
    #     data_report = base_report.GroundReport
    #     template_name += 'ground-report.html'
    # elif hasattr(base_report, 'hazardreport'):
    #     data_report = base_report.hazardreport
    #     template_name += 'hazard-report.html'
    
    context = {
        'base_report' : base_report,
        'data_report' : data_report,
    }

    return render(request, template_name, context)