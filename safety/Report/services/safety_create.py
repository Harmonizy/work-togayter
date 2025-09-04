import logging
from django.db import transaction

logger = logging.getLogger(__name__)  

def perform_create_all(base_form, image_fs, rec_fs, file_fs,
                       ground_form, aviation_form,
                       request, priority):
    with transaction.atomic():
        base_report = base_form.save(commit=False)

        if not getattr(base_report, "anonymous", False):
            base_report.recorder = request.user
        base_report.priority = priority
        base_report.save()

        for fs in (image_fs, rec_fs, file_fs):
            objs = fs.save(commit=False)
            for obj in objs:
                obj.base_report = base_report
                obj.save()

        if ground_form:
            g = ground_form.save(commit=False)
            g.base_report = base_report
            g.save()

        if aviation_form:
            a = aviation_form.save(commit=False)
            a.base_report = base_report
            a.save()
            aviation_form.save_m2m()

        logger.info("Report #%d created successfully by %s",
                    base_report.id, getattr(request.user, "username", "-"))

        return base_report
