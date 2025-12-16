# =========================================
#  DASHBOARD VIEW (แก้ใหม่แบบใช้งานได้จริง)
# =========================================
from datetime import datetime
import json

from django.shortcuts import render
from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from ..models import CalendarEvent
from safety.Report.models.reports import BaseReport
from safety.Report.choices import ReportStatusChoices, PriorityChoices, ReportTypeChoices
from safety.RiskManagement.models import CAP
from common.RTAFUser.models import Affiliation
from safety.Report.models import GroundReport
from safety.Report.choices import GroundSafetyCategoryChoices


THAI_MONTHS = [
    "", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
    "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
    "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
]





def get_ground_category_dataset():
    qs = (
        GroundReport.objects
        .filter(category__isnull=False)
        .values("category")
        .annotate(total=Count("base_report_id"))
    )

    data = {choice.label: 0 for choice in GroundSafetyCategoryChoices}

    for row in qs:
        label = GroundSafetyCategoryChoices(row["category"]).label
        data[label] = row["total"]

    return data


def get_cap_datasets(year, month):
    cap = CAP.objects.all()

    # ---- YEAR FILTER ----
    if year != "all":
        cap = cap.filter(hazard_log__date__year=int(year))

    # ---- MONTH FILTER ----
    if month != "all":
        cap = cap.filter(hazard_log__date__month=int(month))

    # ---- COUNT GROUP BY AFFILIATION ----
    raw = (
        cap.values("hazard_log__affiliation__short_name")
        .annotate(
            planning=Count("id", filter=Q(status="P")),
            in_progress=Count("id", filter=Q(status="I")),
            complete=Count("id", filter=Q(status="C")),
        )
    )

    raw_dict = {d["hazard_log__affiliation__short_name"]: d for d in raw}
    all_aff = Affiliation.objects.values_list("short_name", flat=True)

    result = []
    for aff in all_aff:
        result.append(
            raw_dict.get(
                aff,
                {
                    "hazard_log__affiliation__short_name": aff,
                    "planning": 0,
                    "in_progress": 0,
                    "complete": 0,
                }
            )
        )

    result.sort(key=lambda x: x["hazard_log__affiliation__short_name"])
    return result


@login_required
def index(request):
    user = request.user

    # สิทธิ์ดู Dashboard
    if user.is_superuser or user.has_perm("Report.view_all_dashboard"):
        report = BaseReport.objects.all()

    elif user.has_perm("Report.view_affiliation_dashboard"):
        report = BaseReport.objects.filter(affiliation=user.affiliation)

    else:
        report = BaseReport.objects.filter(recorder=user)

    # ---- COUNTERS ----
    report_all = report.count()
    report_draft = report.filter(status=ReportStatusChoices.DRAFT).count()
    report_approved = report.filter(status=ReportStatusChoices.APPROVED).count()
    report_high = report.filter(priority=PriorityChoices.HIGH).count()
    report_medium = report.filter(priority=PriorityChoices.MEDIUM).count()
    report_low = report.filter(priority=PriorityChoices.LOW).count()

    # ---- FILTER ----
    current_year = datetime.now().year

    selected_year = request.GET.get("year", "all")
    selected_month = request.GET.get("month", "all")

    reports = report

    if selected_year != "all":
        reports = reports.filter(event_date__year=int(selected_year))

    if selected_month != "all":
        reports = reports.filter(event_date__month=int(selected_month))

    # ---- REPORT datasets ----
    report_datasets = get_monthly_reports_by_type(reports)
    priority_datasets = get_monthly_reports_by_priority(reports)

    # ---- CAP datasets ----
    cap_datasets = get_cap_datasets(selected_year, selected_month)
    ground_category_data = get_ground_category_dataset()
    
    affiliations = list(
        Affiliation.objects.annotate(
            report_count=Count("base_reports")   # ใช้ related_name ของ affiliation field
        ).values(
            "short_name",
            "full_name",
            "report_count",
        )
    )

    # ---- Dropdown ----
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

        "events": CalendarEvent.objects.filter(date__month=datetime.now().month)
                        .order_by("date", "time"),

        # === ส่ง JSON ให้ JS ===
        "cap_datasets": json.dumps(cap_datasets, ensure_ascii=False),
        "report_datasets": json.dumps(report_datasets, ensure_ascii=False),
        "priority_datasets": json.dumps(priority_datasets, ensure_ascii=False),
        "affiliations_json": json.dumps(affiliations, ensure_ascii=False),
        "ground_category_json": json.dumps(ground_category_data, ensure_ascii=False),

        # === Filters ===
        "month_list": month_list,
        "year_list": year_list,
        "current_month": selected_month,
        "current_year": selected_year,
    }

    return render(request, "Dashboard/home-index.html", context)


def get_monthly_reports_by_type(reports):
    qs = (
        reports.annotate(month=ExtractMonth("event_date"))
               .values("month", "report_type")
               .annotate(total=Count("id"))
               .order_by("month")
    )

    all_types = [choice.label for choice in ReportTypeChoices] + ["ไม่ระบุประเภท"]
    type_data = {t: [0] * 12 for t in all_types}

    for row in qs:
        if not row["month"]:
            continue

        month_index = row["month"] - 1
        raw_value = row["report_type"] or ""

        try:
            label = ReportTypeChoices(raw_value).label
        except ValueError:
            label = "ไม่ระบุประเภท"

        type_data[label][month_index] = row["total"]

    return [{"label": label, "data": data} for label, data in type_data.items()]


def get_monthly_reports_by_priority(reports):
    qs = (
        reports.annotate(month=ExtractMonth("event_date"))
               .values("month", "priority")
               .annotate(total=Count("id"))
               .order_by("month")
    )

    all_priorities = [choice.label for choice in PriorityChoices]
    priority_data = {p: [0] * 12 for p in all_priorities}

    for row in qs:
        if row["month"]:
            month_index = row["month"] - 1
            label = PriorityChoices(row["priority"]).label
            priority_data[label][month_index] = row["total"]

    return [{"label": label, "data": data} for label, data in priority_data.items()]
