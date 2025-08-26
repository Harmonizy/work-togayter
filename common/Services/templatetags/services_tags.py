from django import template

from ..thaidate import thai_date, thai_date_short, thai_months

register = template.Library()

@register.filter(name='thai_date')
def thai_date_filter(value):
    """
    Converts a date object to a Thai-style date string.
    """
    if value:
        try:
            return thai_date(value)  
        except:
            return "-"
    return value

@register.filter('thai_date_short')
def thai_date_short_filter(value):
    """
    Converts a date object to a short Thai-style date string.
    """
    if value:
        try:
            return thai_date_short(value)
        except:
            return "-"
    return value


@register.simple_tag
def format_date_range(start_date, end_date):
    if not start_date or not end_date:
        return ""

    start_year_be = (start_date.year + 543) % 100
    end_year_be = (end_date.year + 543) % 100
    
    str_end_date = f"{end_date.day:02d} {thai_months[end_date.month-1]} {end_year_be}"
    
    if start_date.year == end_date.year:
        if start_date.month == end_date.month:
            return f"{start_date.day:02d}-{str_end_date}"
        else:
            return f"{start_date.day:02d} {thai_months [start_date.month-1]}-{str_end_date}"
    else:
        return f"{start_date.day:02d}{thai_months[start_date.month-1]} {start_year_be}-{str_end_date}"

# {% format_date_range start_date end_date %}