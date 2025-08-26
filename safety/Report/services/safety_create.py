import logging
from django.db import transaction
from django.contrib import messages

from ..forms.reports import BaseReportForm
from ..forms.attachments import ImageFormSet, RecommendationFormSet, FileFormSet

logger = logging.getLogger('report')


def create_new_report(request):
    base_form = BaseReportForm(request.POST, prefix="base_form")
    image_formset = ImageFormSet(request.POST, request.FILES, prefix='images')
    recommendation_formset = RecommendationFormSet(request.POST, prefix='recommendations')
    file_formset = FileFormSet(request.POST, request.FILES, prefix='files')

    if all([base_form.is_valid(), image_formset.is_valid(),
            recommendation_formset.is_valid(), file_formset.is_valid()]):

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
            messages.info(request, f"บันทึกข้อมูลเหตุการณ์ {base_report} เรียบร้อยแล้ว")

        return True, (base_form, image_formset, recommendation_formset, file_formset), base_report

    # return invalid forms for re-render
    return False, (base_form, image_formset, recommendation_formset, file_formset), None
