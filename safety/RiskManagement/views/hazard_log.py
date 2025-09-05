from django.shortcuts import get_object_or_404, render

from safety.Data.models import Event
from safety.RiskManagement.models import HazardLog

def list(request):
    event = Event.objects.all()
    hazard_log = HazardLog.objects.all()
    context = {
        'event': event,
        'hazard_log': hazard_log,
        
    }
    return render(request, "RiskManagement/hazard-log/hazard-list.html", context)