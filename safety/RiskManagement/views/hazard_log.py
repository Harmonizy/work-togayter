from django.shortcuts import render, redirect, get_object_or_404

from ..models import HazardLog
from ..choices import HazardSourceChoices
from ..forms import HazardLogForm
from ..services.hazard_summary import get_hazard_summary_cards

def list(request):    
    hazard_log = HazardLog.objects.all()
    cards = get_hazard_summary_cards()
    context = {
        "cards": cards,
        'hazard_log': hazard_log,        
    }
    return render(request, "RiskManagement/hazard-log/hazard-list.html", context)

# Create View
def create(request):
    if request.method == 'POST':
        form = HazardLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hazard-log-list')  # Change to your actual list view name
        else:
            print(form.errors)
    else:
        form = HazardLogForm()
    
    context = {
        'form': form,
        'title': 'เพิ่มรายการอันตราย',
        'HazardSourceChoices': HazardSourceChoices,
    }
    return render(request, 'RiskManagement/hazard-log/hazard-log-form.html', context)

# Update View
def update(request, pk):
    hazard = get_object_or_404(HazardLog, pk=pk)
    if request.method == 'POST':
        form = HazardLogForm(request.POST, instance=hazard)
        if form.is_valid():
            form.save()
            return redirect('RiskManagement/hazard-log/hazard_log_list')  # Change to your actual list view name
    else:
        form = HazardLogForm(instance=hazard)
    return render(request, 'hazard_log/hazard_form.html', {'form': form, 'title': 'แก้ไขรายการอันตราย'})
