# safety/Report/views/details.py
from django.shortcuts import get_object_or_404, render
from django.db.models import Prefetch

from ..models import HazardLog, CAP

def main(request, id):
    hazard_log = HazardLog.objects.get(id=id)
    caps = hazard_log.caps.all()
    context = {
        "hazard_log": hazard_log,
        "caps": caps,
    }
    return render(request, "RiskManagement/hazard-log/hazard-detail.html", context)
