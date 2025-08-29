import logging
from django.db import transaction
from django.contrib import messages

from ..forms.reports import BaseReportForm
from ..forms.attachments import ImageFormSet, RecommendationFormSet, FileFormSet

logger = logging.getLogger('report')


def create_new_report(base_form, image_formset, recommendation_formset, file_formset, request, priority):
    with transaction.atomic():
        base_report = base_form.save(commit=False)

        # assign user if not anonymous
        if not base_report.anonymous:
            base_report.recorder = request.user

        # set priority
        base_report.priority = request.POST.get("initial_assessment")
        base_report.save()

        # save related formsets
        for formset in [image_formset, recommendation_formset, file_formset]:
            for obj in formset.save(commit=False):
                obj.base_report = base_report
                obj.save()
        logger.info("Report #%d created successfully by %s", base_report.id, request.user.username)
        return True, (base_form, image_formset, recommendation_formset, file_formset), base_report

    return False, (base_form, image_formset, recommendation_formset, file_formset)
