from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from ..models import HazardCategory
from ..services.hazard_summary import get_hazard_summary_cards

def list(request):    
    hazard_category = HazardCategory.objects.all()
    cards = get_hazard_summary_cards()
    context = {
        "cards": cards,
        'hazard_category': hazard_category,        
    }
    return render(request, "RiskManagement/hazard-log/hazard-category.html", context)