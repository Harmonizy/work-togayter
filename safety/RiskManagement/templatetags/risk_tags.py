from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def risk_box(value, label=""):
    """
    Render a colored risk box with a number and optional label under it.
    Usage:
        {% risk_box 16 "ก่อนแก้ไข" %}
        {% risk_box 6 "หลังแก้ไข" %}
    """
    try:
        num = int(value)
    except (ValueError, TypeError):
        num = value

    base_style = (
        "width:100px; height:100px; "
        "border:3px solid #333; border-radius:8px; margin:10px; "
        "display:flex; flex-direction:column; align-items:center; justify-content:center; "
        "font-weight:bold; font-size:2.5rem; "
        "box-shadow:3px 3px 3px rgba(0,0,0,0.3);"
    )

    # Pick colors
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

    # Label (small text under number)
    label_html = f'<div style="font-size:0.8rem; font-weight:normal; margin-top:5px;">{label}</div>' if label else ""

    html = f'''
    <div style="{base_style}{color_style}">
        <div>{num}</div>
        {label_html}
    </div>
    '''
    return mark_safe(html)
