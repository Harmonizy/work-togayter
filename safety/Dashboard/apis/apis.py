# ✅ API endpoint สำหรับส่งข้อมูล CAP แยกตามหน่วยและสถานะ
from django.http import JsonResponse
from django.db.models import Count, Q
from safety.RiskManagement.models import CAP

from common.RTAFUser.models import Affiliation 
def cap_data_api(request):
    cap_data = (
        CAP.objects.values("hazard_log__affiliation__short_name")
        .annotate(
            planning=Count("id", filter=Q(status="P")),
            in_progress=Count("id", filter=Q(status="I")),
            complete=Count("id", filter=Q(status="C")),
        )
    )

    cap_dict = {
        d["hazard_log__affiliation__short_name"]: d for d in cap_data
    }

    all_affiliations = Affiliation.objects.values_list("short_name", flat=True)

    result = []
    for aff in all_affiliations:
        data = cap_dict.get(aff, {
            "hazard_log__affiliation__short_name": aff,
            "planning": 0,
            "in_progress": 0,
            "complete": 0,
        })
        result.append(data)

    result.sort(key=lambda x: x["hazard_log__affiliation__short_name"])

    return JsonResponse(result, safe=False)
