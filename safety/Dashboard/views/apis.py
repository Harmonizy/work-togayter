# safety/Dashboard/views/dashboard_home.py

from django.http import JsonResponse
from django.db.models import Count
from safety.RiskManagement.models import CAP

# ✅ API endpoint สำหรับส่งข้อมูล CAP แยกตามหน่วยงาน
def cap_data_api(request):
    data = (
        CAP.objects
        .values("hazard_log__affiliation__short_name")
        .annotate(total=Count("id"))
        .order_by("hazard_log__affiliation__short_name")
    )
    return JsonResponse(list(data), safe=False)
