import logging
from django.db import transaction

logger = logging.getLogger('report')

def create_new_report(base_form, image_formset, recommendation_formset, file_formset, request, priority):
    with transaction.atomic():
        base_report = base_form.save(commit=False)

        if not base_report.anonymous and request.user.is_authenticated:
            base_report.recorder = request.user

        base_report.priority = priority
        base_report.save()

        for fs in (image_formset, recommendation_formset, file_formset):
            fs.instance = base_report
            fs.save()

        logger.info("Report #%d created successfully by %s", base_report.id, getattr(request.user, "username", "system"))
        return True, (base_form, image_formset, recommendation_formset, file_formset), base_report

    return False, (base_form, image_formset, recommendation_formset, file_formset)
