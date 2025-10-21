import logging
from django.db import transaction

logger = logging.getLogger('report')  


def save_new_report(request, base_form, image_formset, rec_formset, file_formset, priority):
    with transaction.atomic():
        base_report = base_form.save(commit=False)

        if not base_report.anonymous:
            base_report.recorder = request.user
        
        base_report.priority = priority
        base_report.save()

        for formset in (image_formset, rec_formset, file_formset):
            attachments = formset.save(commit=False)
            for attach in attachments:
                attach.base_report = base_report
                attach.save()

        logger.info("Report #%d created successfully by %s", base_report.id, request.user.username)

        return base_report


def save_new_report_officer(request, base_form, participant_formset, image_formset, rec_formset, file_formset, reference_formset, priority, ground_form=None, aviation_form=None):
    with transaction.atomic():
        base_report = base_form.save(commit=False)

        if not base_report.anonymous:
            base_report.recorder = request.user
        
        base_report.priority = priority
        base_report.save()

        for formset in (participant_formset, image_formset, rec_formset, file_formset, reference_formset):
            attachments = formset.save(commit=False)
            for attach in attachments:
                attach.base_report = base_report
                attach.save()
                
        if ground_form:
            # print("Saving ground report")
            ground = ground_form.save(commit=False)
            ground.base_report = base_report
            ground.save()

        if aviation_form:
            # print("Saving aviation report")
            aviation = aviation_form.save(commit=False)
            aviation.base_report = base_report
            aviation.save()
            aviation_form.save_m2m()

        logger.info("Report #%d created successfully by %s", base_report.id, request.user.username)

        return base_report
