from datetime import datetime
from django.shortcuts import render

from ..models import CalendarEvent, EventCategory, ThailandHoliday

def index(request):
    current_month = datetime.now().month
    context = {
        # filter this month, order by date asc
        'events': CalendarEvent.objects.filter(date__month=current_month).order_by('date','time')
    }
    return render(request, 'Dashboard/home-index.html', context)
