from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from ..models import CAP
from ..forms import CAPForm

@login_required
@permission_required("RiskManagement.create_cap", raise_exception=True)
def cap_delete_view(request, cap_id):
    cap = get_object_or_404(CAP, id=cap_id)
    title = cap.title
    hazard_id = cap.hazard_log.id
    if request.method == "POST":
        cap.delete()
        messages.success(request, f"ลบ CAP: {title} เรียบร้อยแล้ว")
    return redirect("risk_management:hazard-detail", id=hazard_id)