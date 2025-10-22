from datetime import datetime
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from ..models import CalendarEvent
from safety.Report.models.reports import BaseReport
from safety.Report.choices import ReportStatusChoices, PriorityChoices, ReportTypeChoices

# 📅 เดือนภาษาไทยมาตรฐาน (production safe)
THAI_MONTHS = [
    "", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
    "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
    "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
]

def index(request):
    report = BaseReport.objects.all()
    report_all = report.count()
    report_draft = report.filter(status=ReportStatusChoices.DRAFT).count()
    report_approved = report.filter(status=ReportStatusChoices.APPROVED).count()
    report_high = report.filter(priority=PriorityChoices.HIGH).count()
    report_medium = report.filter(priority=PriorityChoices.MEDIUM).count()
    report_low = report.filter(priority=PriorityChoices.LOW).count()

    current_year = datetime.now().year
    current_month = datetime.now().month

    selected_year = request.GET.get("year")
    selected_month = request.GET.get("month")

    qs = BaseReport.objects.all()

    if selected_year and selected_year != "all":
        qs = qs.filter(event_date__year=int(selected_year))
    else:
        selected_year = current_year  

    if selected_month and selected_month != "all":
        qs = qs.filter(event_date__month=int(selected_month))
    else:
        selected_month = "all"

    qs = (
        qs.annotate(month=ExtractMonth("event_date"))
        .values("month", "report_type")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    all_types = [choice.label for choice in ReportTypeChoices]
    type_data = {t: [0] * 12 for t in all_types}

    for row in qs:
        if row["month"]:  
            month_index = row["month"] - 1
            label = ReportTypeChoices(row["report_type"]).label
            type_data[label][month_index] = row["total"]

    report_datasets = [{"label": label, "data": data} for label, data in type_data.items()]

    month_list = [{"number": "all", "name": "ทั้งหมด"}] + [
        {"number": i, "name": THAI_MONTHS[i]} for i in range(1, 13)
    ]
    year_list = [{"number": "all", "name": "ทั้งหมด"}] + [
        {"number": y, "name": str(y)} for y in range(current_year - 5, current_year + 1)
    ]

    context = {
        "report": report,
        "report_all": report_all,
        "report_draft": report_draft,
        "report_approved": report_approved,
        "report_high": report_high,
        "report_medium": report_medium,
        "report_low": report_low,
        "events": CalendarEvent.objects.filter(date__month=datetime.now().month).order_by("date", "time"),
        "report_datasets": report_datasets,
        "month_list": month_list,
        "year_list": year_list,
        "current_month": selected_month,
        "current_year": selected_year,
    }

    return render(request, "Dashboard/home-index.html", context)
