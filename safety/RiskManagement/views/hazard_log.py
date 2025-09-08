from django.shortcuts import render

from ..models import HazardLog
from ..services.hazard_summary import get_hazard_summary_cards

def list(request):    
    hazard_log = HazardLog.objects.all()
    cards = get_hazard_summary_cards()
    context = {
        "cards": cards,
        'hazard_log': hazard_log,        
    }
    return render(request, "RiskManagement/hazard-log/hazard-list.html", context)