from django.shortcuts import get_object_or_404, render

def list(request):
    return render(request, "Report/hazard-log/hazard-list.html")