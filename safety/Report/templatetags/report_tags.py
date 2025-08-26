from django import template
from django.utils.safestring import mark_safe

from ..choices import ReportStatusChoices

register = template.Library()

@register.simple_tag
def status_badge(report):
    status = report.status

    # Map status to bootstrap classes
    classes_map = {
        ReportStatusChoices.DRAFT: "bg-info-subtle text-info",
        ReportStatusChoices.SUBMITTED: "bg-warning-subtle text-warning",
        ReportStatusChoices.CHECKING: "bg-primary-subtle text-primary",
        ReportStatusChoices.APPROVED: "bg-success-subtle text-success",
        ReportStatusChoices.REJECTED: "bg-danger-subtle text-danger",
    }

    badge_class = classes_map.get(status, "bg-secondary-subtle text-secondary")
    status_display = report.get_status_display()

    html = f'<span class="badge {badge_class}">{status_display}</span>'
    return mark_safe(html)
