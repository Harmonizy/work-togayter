import logging

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction

from ..forms.reports import BaseReportForm
from ..choices import PriorityChoices
# , HazardReportForm, AviationReportForm, GroundReportForm, SafetyReportForm
from ..forms.attachments import ImageFormSet, RecommendationFormSet, FileFormSet


logger = logging.getLogger('report')

@login_required
def new_report(request):
    if request.method == 'POST':
        base_form = BaseReportForm(request.POST, prefix="base_form")
        image_formset = ImageFormSet(request.POST, request.FILES, prefix='images')
        recommendation_formset = RecommendationFormSet(request.POST, prefix='recommendations')
        file_formset = FileFormSet(request.POST, request.FILES, prefix='files')

        if base_form.is_valid() and image_formset.is_valid() and recommendation_formset.is_valid() and file_formset.is_valid():

            with transaction.atomic():
                base_report = base_form.save(commit=False)
                if not base_report.anonymous:
                    base_report.recorder = request.user

                base_report.priority = request.POST.get("initial_assessment")
                base_report.save()

                for formset in [image_formset, recommendation_formset, file_formset]:
                    for obj in formset.save(commit=False):
                        obj.base_report = base_report
                        obj.save()

            return redirect('report:safety-report.list')
    else:
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

