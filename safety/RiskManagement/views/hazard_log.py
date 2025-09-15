from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from ..models import HazardLog
from ..choices import HazardSourceChoices
from ..forms import HazardLogForm, CAPFormSet
from ..services.hazard_summary import get_hazard_summary_cards


def list(request):
    hazard_log = HazardLog.objects.all()
    cards = get_hazard_summary_cards()
    context = {
        "cards": cards,
        "hazard_log": hazard_log,
    }
    return render(request, "RiskManagement/hazard-log/hazard-list.html", context)


def handle_create(request, initial_data=None):
    if request.method == "POST":
        form = HazardLogForm(request.POST)
        formset = CAPFormSet(request.POST)
        if form.is_valid():
            form.save()
            # formset.save()
            return redirect("risk_management:hazard-log")
        else:
            print(form.errors)
    else:
        form = HazardLogForm(initial=initial_data)
        formset = CAPFormSet()

    context = {
        "form": form,
        "formset": formset,
        "title": "เพิ่มรายการอันตราย",
        "HazardSourceChoices": HazardSourceChoices,
    }
    return render(request, "RiskManagement/hazard-log/hazard-create.html", context)


def create(request):
    return handle_create(request)


def create_by_report(request, report_id):
    return handle_create(request, initial_data={"related_report_id": report_id})


@require_POST
def delete(request, pk):
    hazard = get_object_or_404(HazardLog, pk=pk)
    code = hazard.code
    hazard.delete()  
    messages.success(request, f"ลบทะเบียนความเสี่ยง {code} เรียบร้อย")
    return redirect("risk_management:hazard-log")