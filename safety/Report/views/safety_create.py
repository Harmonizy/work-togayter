import logging

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction

from ..forms.reports import BaseReportForm
from ..choices import PriorityChoices
# , HazardReportForm, AviationReportForm, GroundReportForm, SafetyReportForm
from ..forms.attachments import ImageFormSet, RecommendationFormSet, FileFormSet
from ..services.safety_create import create_new_report


logger = logging.getLogger('report')

@login_required
def new_report(request): 
    if request.method == 'POST':
        base_form = BaseReportForm(request.POST, prefix="base_form")
        image_formset = ImageFormSet(request.POST, request.FILES, prefix='images')
        recommendation_formset = RecommendationFormSet(request.POST, prefix='recommendations')
        file_formset = FileFormSet(request.POST, request.FILES, prefix='files')
        
        if "priority-H" in request.POST:
            priority = "H"
        elif "priority-M" in request.POST:
            priority = "M"
        else:
            priority = "L"

        forms_validate = [base_form.is_valid(), image_formset.is_valid(), recommendation_formset.is_valid(), file_formset.is_valid()]
        if all(forms_validate):        
            success, forms, base_report = create_new_report(base_form, image_formset, recommendation_formset, file_formset, request.user, priority)
            base_form, image_formset, recommendation_formset, file_formset = forms
        if success:
            
            messages.info(request, f"บันทึกข้อมูลเหตุการณ์ {base_report} เรียบร้อยแล้ว")
            return redirect('report:safety-report.list')

    else:  # GET
        initial_data = {'affiliation': request.user.affiliation}
        if request.user.affiliation.airviation_content:
            initial_data['content'] = request.user.affiliation.airviation_content

        base_form = BaseReportForm(prefix="base_form", initial=initial_data)
        image_formset = ImageFormSet(prefix='images')
        recommendation_formset = RecommendationFormSet(prefix='recommendations')
        file_formset = FileFormSet(prefix='files')

    return render(request, 'Report/safety-reports/safety-create.new-report.html', {
        'base_form': base_form,
        'image_formset': image_formset,
        'recommendation_formset': recommendation_formset,
        'file_formset': file_formset,
    })

