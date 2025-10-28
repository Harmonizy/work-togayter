from django.shortcuts import redirect, render
from django.contrib import messages
from ..models import CAP
from ..forms import CAPForm

def cap_edit(request, cap_id):
    cap = CAP.objects.get(id=cap_id)
    if request.method == "POST":
        form = CAPForm(request.POST, instance=cap)
        if form.is_valid():
            form.save()
            messages.success(request, "CAP ถูกแก้ไขเรียบร้อยแล้ว")
            return redirect("risk_management:hazard-detail", id=cap.hazard_log.id)
    else:
        form = CAPForm(instance=cap)
    
    return render(request, "RiskManagement/hazard-log/cap-edit.html", {"form": form, "cap": cap, "hazard": cap.hazard_log })