from django.shortcuts import render, get_object_or_404, redirect

from ..models import HazardLog
from ..forms import HazardLogForm, CAPFormSet

def update(request, pk):
    hazard_log = get_object_or_404(HazardLog, pk=pk)

    if request.method == 'POST':
        form = HazardLogForm(request.POST, instance=hazard_log)
        formset = CAPFormSet(request.POST, instance=hazard_log)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('your-success-url')  # replace with your success redirect

    else:
        form = HazardLogForm(instance=hazard_log)
        formset = CAPFormSet(instance=hazard_log)

    return render(request, 'RiskManagement/hazard-log/hazard-edit.html', {
        'form': form,
        'formset': formset,
    })
