# safety/Report/views/details.py
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Prefetch

from ..models import HazardLog, CAP


@login_required
@permission_required("RiskManagement.detail_hazard_log", raise_exception=True)
def main(request, id):
    hazard_log = HazardLog.objects.get(id=id)
    caps = hazard_log.caps.all()
    
    initial_likelihood = hazard_log.initial_likelihood
    initial_severity = hazard_log.initial_severity
    residual_likelihood = hazard_log.residual_likelihood
    residual_severity = hazard_log.residual_severity

    initial_image = f"{initial_likelihood}{initial_severity}.jpg"
    residual_image = f"{residual_likelihood}{residual_severity}.jpg"

    context = {
        "hazard_log": hazard_log,
        "caps": caps,
        "initial_image": initial_image,
        "residual_image": residual_image,
    }
    return render(request, "RiskManagement/hazard-log/hazard-detail.html", context)
