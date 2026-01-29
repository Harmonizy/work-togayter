from django import template
from django.utils.safestring import mark_safe

from ..choices import ReportStatusChoices, PriorityChoices

register = template.Library()

@register.simple_tag
def status_badge(report):
    status = report.status

    # Map status to bootstrap classes
    classes_map = {
        ReportStatusChoices.DRAFT: "bg-secondary-subtle text-secondary",
        ReportStatusChoices.APPROVE: "bg-info-subtle text-info",
        ReportStatusChoices.REJECT: "bg-danger-subtle text-danger",
        ReportStatusChoices.SEND: "bg-warning-subtle text-warning",
        ReportStatusChoices.RECEIVE: "bg-primary-subtle text-primary",
        ReportStatusChoices.COMPLETE: "bg-success-subtle text-success",
        ReportStatusChoices.ARCHIVE: "bg-secondary-subtle text-secondary",
    }

    badge_class = classes_map.get(status, "bg-secondary-subtle text-secondary")
    status_display = report.get_status_display()

    html = f'<span class="badge {badge_class}">{status_display}</span>'
    return mark_safe(html)


@register.simple_tag
def priority_badge(report):
    priority = report.priority

    # Map status to bootstrap classes
    classes_map = {
        PriorityChoices.HIGH: "bg-danger-subtle text-danger",
        PriorityChoices.MEDIUM: "bg-warning-subtle text-warning",
        PriorityChoices.LOW: "bg-success-subtle text-success",

    }

    badge_class = classes_map.get(priority, "bg-secondary-subtle text-secondary")
    priority_display = report.get_priority_display()

    html = f'<span class="badge {badge_class}">{priority_display}</span>'
    return mark_safe(html)
