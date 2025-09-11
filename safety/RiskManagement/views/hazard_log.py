from django.shortcuts import render, redirect

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


def create(request):
    if request.method == "POST":
        form = HazardLogForm(request.POST)
        formset = CAPFormSet(request.POST)
        if form.is_valid():
            form.save()
            formset.save()
            return redirect("risk_management:hazard-log")  
        else:
            print(form.errors)
    else:
        form = HazardLogForm()
        formset = CAPFormSet()

    context = {
        "form": form,
        'formset': formset,
        "title": "เพิ่มรายการอันตราย",
        "HazardSourceChoices": HazardSourceChoices,
    }
    return render(request, "RiskManagement/hazard-log/hazard-log-form.html", context)