
from safety.Report.choices import ReportStatusChoices, PriorityChoices


def card_data(reports):    
    total_reports = reports.count()
    total_growth = "0.87"
    pending_reports = reports.filter(status=ReportStatusChoices.DRAFT).count()
    pending_growth = "3.2"
    completed_reports = reports.filter(status=ReportStatusChoices.APPROVED).count()
    completed_growth = "5.8"
    high_priority_reports = reports.filter(priority=PriorityChoices.HIGH).count()
    high_priority_growth = "1.1"

    return [
        {
            "label": "รายงานรวม",
            "count": total_reports,
            "growth": total_growth,
            "trend_icon": "down",
            "trend_color": "danger",
            "icon_bg": "bg-info-subtle",
            "icon_text": "text-info",
            "icon": "ri-file-text-line"
        },
        {
            "label": "รอดำเนินการ",
            "count": pending_reports,
            "growth": pending_growth,
            "trend_icon": "down",
            "trend_color": "danger",
            "icon_bg": "bg-warning-subtle",
            "icon_text": "text-warning",
            "icon": "mdi mdi-timer-sand"
        },
        {
            "label": "รายงานอนุมัติ",
            "count": completed_reports,
            "growth": completed_growth,
            "trend_icon": "up",
            "trend_color": "success",
            "icon_bg": "bg-success-subtle",
            "icon_text": "text-success",
            "icon": "ri-checkbox-circle-line"
        },
        {
            "label": "รายงานเร่งด่วน",
            "count": high_priority_reports,
            "growth": high_priority_growth,
            "trend_icon": "up",
            "trend_color": "danger",
            "icon_bg": "bg-danger-subtle",
            "icon_text": "text-danger",
            "icon": "ri-alert-line"
        },
    ]
