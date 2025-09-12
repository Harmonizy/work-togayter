import logging

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction

from ..models import BaseReport  # Import your report model
from ..forms.reports import BaseReportForm
from ..forms.attachments import ImageFormSet, RecommendationFormSet, FileFormSet

logger = logging.getLogger('report')


@login_required
def edit_report(request, report_id):
    report = get_object_or_404(BaseReport, pk=report_id)

    if request.method == 'POST':
        base_form = BaseReportForm(request.POST, instance=report, prefix='base_form', user=request.user)
        image_formset = ImageFormSet(request.POST, request.FILES, instance=report, prefix='images')
        recommendation_formset = RecommendationFormSet(request.POST, instance=report, prefix='recommendations')
        file_formset = FileFormSet(request.POST, request.FILES, instance=report, prefix='files')

        if all([base_form.is_valid(), image_formset.is_valid(),
                recommendation_formset.is_valid(), file_formset.is_valid()]):
            try:
                with transaction.atomic():
                    base_report = base_form.save()

                    for formset in [image_formset, recommendation_formset, file_formset]:
                        instances = formset.save(commit=False)
                        for obj in instances:
                            obj.base_report = base_report
                            obj.save()
                        for obj in formset.deleted_objects:
                            obj.delete()

                logger.info("Report #%d updated successfully by %s", base_report.id, request.user.username)
                messages.success(request, f"อัปเดตรายงาน {base_report} เรียบร้อยแล้ว")
                return redirect('report:safety-report.list')
            except Exception as e:
                logger.exception("Error while updating report: %s", str(e))
                messages.error(request, "เกิดข้อผิดพลาดขณะอัปเดตรายงาน กรุณาลองใหม่อีกครั้ง")
        else:
            logger.warning("Form validation failed while editing report #%d", report.id)
            print("Base Form Errors:", base_form.errors)
            print("Image Formset Errors:", image_formset.errors)
            print("Recommendation Formset Errors:", recommendation_formset.errors)
            print("File Formset Errors:", file_formset.errors)

    else:
        base_form = BaseReportForm(instance=report, prefix='base_form', user=request.user)
        image_formset = ImageFormSet(instance=report, prefix='images')
        recommendation_formset = RecommendationFormSet(instance=report, prefix='recommendations')
        file_formset = FileFormSet(instance=report, prefix='files')

    context = {
        'base_form': base_form,
        'image_formset': image_formset,
        'recommendation_formset': recommendation_formset,
        'file_formset': file_formset,
        'report': report,
    }
    return render(request, 'Report/safety-reports/report-edit.html', context)
