# ✅ API endpoint สำหรับส่งข้อมูล CAP แยกตามหน่วยและสถานะ
from django.http import JsonResponse
from django.db.models import Count, Q
from safety.RiskManagement.models import CAP

def cap_data_api(request):
    data = (
        CAP.objects.values("hazard_log__affiliation__short_name")
        .annotate(
            planning=Count("id", filter=Q(status="P")),
            in_progress=Count("id", filter=Q(status="I")),
            complete=Count("id", filter=Q(status="C")),
        )
        .order_by("hazard_log__affiliation__short_name")
    )
    return JsonResponse(list(data), safe=False)