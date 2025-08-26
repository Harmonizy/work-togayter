from django.shortcuts import render

from ..forms.reports import BaseReportTitleContentPartForm, GroundReportForm, AviationReportForm
from common.RTAFUser.models import Affiliation

def base_title_air_ground(request):
    report_type = request.GET.get('base_form-report_type')
    affiliation_id = request.GET.get('base_form-affiliation')
    
    initial_data={}

    if affiliation_id:
        try:
            affiliation = Affiliation.objects.get(id=affiliation_id)
            if affiliation.airviation_content:
                initial_data['content'] = affiliation.airviation_content
        except Affiliation.DoesNotExist:
            pass

    base_form = BaseReportTitleContentPartForm(prefix='base_form', initial=initial_data)

    context = {
        'base_form': base_form
    }
    
    if "G" in report_type:
        context["ground_form"] = GroundReportForm(prefix='ground')
        
    if "A" in report_type:
        context["aviation_form"] = AviationReportForm(prefix='aviation')

    return render(request, 'Report/safety-reports/partials/base-title-air-ground.html', context)