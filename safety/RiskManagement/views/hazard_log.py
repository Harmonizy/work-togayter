from django.shortcuts import get_object_or_404, render

def list(request):
    return render(request, "RiskManagement/hazard-log/hazard-list.html", {})