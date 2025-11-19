from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from ..models import HazardLog, CAP
from ..choices import HazardSourceChoices
from ..forms import HazardLogForm, CAPFormSet
from ..services.hazard_summary import get_hazard_summary_cards


@login_required
def cap_list(request):
    if request.user.has_perm('RiskManagement.view_all_hazard_log'):
        cap = CAP.objects.all()
    
    elif request.user.has_perm('RiskManagement.view_affiliation_hazard_log'):
        cap = CAP.objects.filter(hazard_log__affiliation=request.user.affiliation)
    
    else:
        raise PermissionDenied()

    context = {
        "cap": cap,
    }
    return render(request, "RiskManagement/hazard-log/cap-list.html", context)
