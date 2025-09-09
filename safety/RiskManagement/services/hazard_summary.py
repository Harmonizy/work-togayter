from django.db.models import Avg, Count

from ..models import HazardLog

def get_hazard_summary_cards():
    total_logs = HazardLog.objects.count()
    avg_risk = HazardLog.objects.aggregate(avg=Avg('initial_risk_level'))['avg'] or 0
    status_counts = HazardLog.objects.values('status').annotate(count=Count('id'))
    status_text = ", ".join([f"{s['status']}: {s['count']}" for s in status_counts])
    investigate_counts = HazardLog.objects.values('inspect').annotate(count=Count('id'))
    inspect_text = ", ".join([f"{i['inspect']}: {i['count']}" for i in investigate_counts])

    # Build card list
    cards = [
        {
            "label": "จำนวนรายการความเสี่ยงทั้งหมด",
            "count": total_logs,
            "icon": "ri-alert-line",
            "icon_bg": "bg-danger-subtle",
            "icon_text": "text-danger",
            "trend_icon": "up",
            "trend_color": "success",
            "growth": 12.5,
        },
        {
            "label": "ค่าเฉลี่ยระดับความเสี่ยงเริ่มต้น",
            "count": f"{avg_risk:.1f}",
            "icon": "ri-bar-chart-line",
            "icon_bg": "bg-warning-subtle",
            "icon_text": "text-warning",
            "trend_icon": "down",
            "trend_color": "danger",
            "growth": -3.2,
        },
        {
            "label": "สถานะของความเสี่ยง",
            "count": status_text,
            "icon": "ri-flag-2-line",
            "icon_bg": "bg-info-subtle",
            "icon_text": "text-info",
            "trend_icon": "up",
            "trend_color": "success",
            "growth": 5.8,
        },
        {
            "label": "สถานะการสอบสวน",
            "count": inspect_text,
            "icon": "ri-search-eye-line",
            "icon_bg": "bg-success-subtle",
            "icon_text": "text-success",
            "trend_icon": "up",
            "trend_color": "primary",
            "growth": 9.1,
        },
    ]
    return cards


