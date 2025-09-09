from django.shortcuts import render
from safety.Data.models import Event
from safety.Report.models import BaseReport, AviationReport, GroundReport

def index(request):
    event = Event.objects.all()
    report = BaseReport.objects.all()
    context = {
        'event': event,
        'report': report,
    }
    return render(request, 'Dashboard/home-index.html', context)
