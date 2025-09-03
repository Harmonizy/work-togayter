import logging
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction

from ..forms.reports import BaseReportForm, GroundReportForm, AviationReportForm
from ..forms.attachments import ImageFormSet, RecommendationFormSet, FileFormSet
from ..services.safety_create import create_new_report

logger = logging.getLogger('report')

def _priority_from_request(request):
    mapping = (('priority-H', 'H'), ('priority-M', 'M'), ('priority-L', 'L'))
    return next((v for k, v in mapping if k in request.POST), 'L')

@login_required
def new_report(request):

    if request.method != 'POST':
        initial = {'affiliation': getattr(request.user, 'affiliation', None)}
        airv = getattr(getattr(request.user, 'affiliation', None), 'airviation_content', None)
        if airv:
            initial['content'] = airv
        return render(request, 'Report/safety-reports/safety-create.new-report.html', {
            'base_form': BaseReportForm(prefix='base_form', initial=initial),
            'image_formset': ImageFormSet(prefix='images'),
            'recommendation_formset': RecommendationFormSet(prefix='recommendations'),
            'file_formset': FileFormSet(prefix='files'),
        })

    base_form = BaseReportForm(request.POST, prefix='base_form')
    image_fs = ImageFormSet(request.POST, request.FILES, prefix='images')
    rec_fs = RecommendationFormSet(request.POST, prefix='recommendations')
    file_fs = FileFormSet(request.POST, request.FILES, prefix='files')
    priority = _priority_from_request(request)

    ok = base_form.is_valid()
    report_type = base_form.cleaned_data.get('report_type') if ok else request.POST.get('base_form-report_type', '')

    ground_form = GroundReportForm(request.POST, prefix='ground') if report_type and 'G' in report_type else None
    aviation_form = AviationReportForm(request.POST, prefix='aviation') if report_type and 'A' in report_type else None

    if ground_form:
        ok = ok and ground_form.is_valid()
    if aviation_form:
        ok = ok and aviation_form.is_valid()

    for fs in (image_fs, rec_fs, file_fs):
        ok = ok and fs.is_valid()
        
    if ok and report_type and 'A' in report_type:
        content_val = base_form.cleaned_data.get('content')
        if not content_val:
            default_airv = getattr(getattr(request.user, 'affiliation', None), 'airviation_content', None)
            if default_airv:
                base_form.instance.content = default_airv
            else:
                base_form.add_error('content', "จำเป็นต้องกรอกเนื้อหา (รายงานภาคอากาศ)")
                ok = False

    if not ok:
        messages.error(request, "กรุณาตรวจสอบข้อมูลให้ถูกต้อง")
        return render(request, 'Report/safety-reports/safety-create.new-report.html', {
            'base_form': base_form,
            'image_formset': image_fs,
            'recommendation_formset': rec_fs,
            'file_formset': file_fs,
        })

    with transaction.atomic():
        success, _, base_report = create_new_report(base_form, image_fs, rec_fs, file_fs, request, priority)
        if not success:
            messages.error(request, "เกิดข้อผิดพลาดในการบันทึกรายงาน")
            return render(request, 'Report/safety-reports/safety-create.new-report.html', {
                'base_form': base_form,
                'image_formset': image_fs,
                'recommendation_formset': rec_fs,
                'file_formset': file_fs,
            })

        if ground_form:
            g = ground_form.save(commit=False)
            g.base_report = base_report
            g.save()

        if aviation_form:
            a = aviation_form.save(commit=False)
            a.base_report = base_report
            a.save()
            aviation_form.save_m2m()

    messages.info(request, f"บันทึกข้อมูลเหตุการณ์ {base_report} เรียบร้อยแล้ว")
    return redirect('report:safety-report.list')
