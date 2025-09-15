from django import template
from django.utils.safestring import mark_safe

register = template.Library()

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

"""
{% load cap_tags %}

<!-- Large Box -->
{% risk_box cap.before_risk "ก่อนแก้ไข" %}

<!-- Small Box for table -->
{% risk_box_small cap.after_risk "หลังแก้ไข" %}
"""

def render_risk_box(value, label="", size="large"):
    try:
        num = int(value)
    except (ValueError, TypeError):
        num = value

    # Color logic
    if isinstance(num, int):
        if 1 <= num <= 12:
            color_style = "color:green; border-color:green; background-color:#e0f8e0;"
        elif 13 <= num <= 18:
            color_style = "color:goldenrod; border-color:goldenrod; background-color:#fff8e0;"
        elif 19 <= num <= 22:
            color_style = "color:orange; border-color:orange; background-color:#fff4e0;"
        elif 23 <= num <= 25:
            color_style = "color:red; border-color:red; background-color:#ffe0e0;"
        else:
            color_style = ""
    else:
        color_style = ""

    # Size presets
    if size == "small":
        base_style = (
            "width:50px; height:50px; "
            "border:2px solid #333; border-radius:6px; margin:2px auto; "
            "display:flex; flex-direction:column; align-items:center; justify-content:center; "
            "font-weight:bold; font-size:1.2rem; "
            "box-shadow:2px 2px 2px rgba(0,0,0,0.2);"
        )
        label_style = "font-size:0.6rem; font-weight:normal; margin-top:1px;"
    else:  # large
        base_style = (
            "width:100px; height:100px; "
            "border:3px solid #333; border-radius:8px; margin:10px; "
            "display:flex; flex-direction:column; align-items:center; justify-content:center; "
            "font-weight:bold; font-size:2.5rem; "
            "box-shadow:3px 3px 3px rgba(0,0,0,0.3);"
        )
        label_style = "font-size:0.8rem; font-weight:normal; margin-top:5px;"

    label_html = f'<div style="{label_style}">{label}</div>' if label else ""

    html = f'''
    <div style="{base_style}{color_style}">
        <div>{num}</div>
        {label_html}
    </div>
    '''
    return mark_safe(html)


@register.simple_tag
def risk_box(value, label=""):
    """
    Render a large risk box (e.g. for detail views).
    Usage: {% risk_box 16 "ก่อนแก้ไข" %}
    """
    return render_risk_box(value, label, size="large")


@register.simple_tag
def risk_box_small(value, label=""):
    """
    Render a small risk box (e.g. for table views).
    Usage: {% risk_box_small 6 "หลังแก้ไข" %}
    """
    return render_risk_box(value, label, size="small")




from ..choices import CAPStatusChoices  # Update with your app name

@register.simple_tag
def cap_status_badge(status_code):
    status_map = {
        CAPStatusChoices.PLANNING: ('วางแผน', 'bg-secondary'),
        CAPStatusChoices.IN_PROGRESS: ('กำลังดำเนินการ', 'bg-warning'),
        CAPStatusChoices.COMPLETE: ('เสร็จสิ้น', 'bg-success'),
    }

    label, badge_class = status_map.get(status_code, ('ไม่ทราบสถานะ', 'bg-light text-dark'))

    html = f'<h3><span class="badge {badge_class}">{label}</span></h3>'
    return mark_safe(html)
