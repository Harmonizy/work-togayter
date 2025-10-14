from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from ..models import HazardLog
from ..choices import HazardSourceChoices
from ..forms import HazardLogForm, CAPFormSet
from ..services.hazard_summary import get_hazard_summary_cards


@login_required
def list(request):
    if request.user.has_perm('RiskManagement.view_all_hazard_log'):
        hazard_log = HazardLog.objects.all()
    elif request.user.has_perm('RiskManagement.view_own_hazard_log'):
        hazard_log = HazardLog.objects.filter(affiliation=request.user.affiliation)
    else:
        raise PermissionDenied() ## Djano ใช้ PermissionDenied เพื่อส่งไป 403

    cards = get_hazard_summary_cards()
    context = {"cards": cards, "hazard_log": hazard_log}
    return render(request, "RiskManagement/hazard-log/hazard-list.html", context)

@login_required
@permission_required("RiskManagement.create_hazard_log", raise_exception=True)
def handle_create(request, initial_data=None):
    if request.method == "POST":
        form = HazardLogForm(request.POST)
        if form.is_valid():
            hazard = form.save()
            return redirect("risk_management:hazard-detail", hazard.id)
        else:
            print(form.errors)
    else:
        form = HazardLogForm(initial=initial_data)

    context = {
        "form": form,
        "title": "เพิ่มรายการอันตราย",
        "HazardSourceChoices": HazardSourceChoices,
    }
    return render(request, "RiskManagement/hazard-log/hazard-create.html", context)


@login_required
@permission_required("RiskManagement.create_caps", raise_exception=True)
def handle_create_cap(request, hazard_id):

    hazard = get_object_or_404(HazardLog, id=hazard_id)

    if request.method == "POST":
        formset = CAPFormSet(request.POST, instance=hazard)
        if formset.is_valid():
            formset.save()
            return redirect("risk_management:hazard-detail", hazard.id)
        else:
            print("❌ Formset invalid:", formset.errors)
    else:
        formset = CAPFormSet(instance=hazard)

    context = {
        "hazard": hazard,
        "formset": formset,
    }
    return render(request, "RiskManagement/hazard-log/cap-create.html", context)


def create(request):
    return handle_create(request)


def create_by_report(request, report_id):
    return handle_create(request, initial_data={"related_report_id": report_id})


@login_required
@permission_required("RiskManagement.delete_hazard_log", raise_exception=True)
@require_POST
def delete(request, pk):
    hazard = get_object_or_404(HazardLog, pk=pk)
    code = hazard.code
    hazard.delete()  
    messages.success(request, f"ลบทะเบียนความเสี่ยง {code} เรียบร้อย")
    return redirect("risk_management:hazard-log")