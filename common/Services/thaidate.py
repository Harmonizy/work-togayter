thai_months = [
    "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
    "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
]

thai_weekdays = [
    "จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"
]

def thai_date(date_obj):
    day = date_obj.day
    month = thai_months[date_obj.month - 1]  
    year = date_obj.year + 543  
    
    return f"{day} {month} {year%100}"

def thai_date_short(date_obj):
    day = date_obj.day
    year = date_obj.year + 543  
    
    return f"{day:02}/{date_obj.month:02}/{year%100}"

def thai_date_month(date_obj):
    day = date_obj.day
    month = thai_months[date_obj.month - 1]  
    year = date_obj.year + 543  
    
    return f"{day} {month} {year%100}"


def thai_month_year(date_obj):
    month = thai_months[date_obj.month - 1]  
    year = date_obj.year + 543  
    return f"{month} {year%100}"
