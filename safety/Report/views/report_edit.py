from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction

from ..models import BaseReport
from ..forms.reports import (
    BaseReportForm, GroundReportForm, AviationReportForm,
    ParticipantFormSet, ReferenceReportFormSet
)
from ..forms.attachments import ImageFormSet, RecommendationFormSet, FileFormSet
from ..choices import ReportTypeChoices, ReportStatusChoices

import logging
logger = logging.getLogger("report")


@login_required
@permission_required("Report.edit_report", raise_exception=True)
def edit_report(request, report_id):
    """แก้ไขรายงานได้ทั้งแบบพื้นฐานและแบบเจ้าหน้าที่"""
    report = get_object_or_404(BaseReport, pk=report_id) 

    # ตรวจสิทธิ์
    if report.status == ReportStatusChoices.DRAFT:
        # if report.recorder != request.user and not request.user.has_perm("Report.edit_report"):
        if not report.recorder == request.user :
            messages.error(request, "คุณไม่มีสิทธิ์แก้ไขรายงานฉบับร่างของผู้อื่น")
            return redirect("report:safety-report.list")
    # else:
    #     if not request.user.has_perm("Report.edit_report"):
    #         messages.error(request, "คุณไม่มีสิทธิ์แก้ไขรายงานนี้ เนื่องจากรายงานนี้ได้รับการอนุมัติแล้ว")
    #         return redirect("report:safety-report.list")

    # เตรียมฟอร์มหลัก
    if request.method == "POST":
        base_form = BaseReportForm(request.POST, instance=report, prefix="base_form", user=request.user)
        participant_formset = ParticipantFormSet(request.POST, prefix="participants", instance=report)
        reference_formset = ReferenceReportFormSet(request.POST, prefix="references", instance=report)
        image_formset = ImageFormSet(request.POST, request.FILES, instance=report, prefix="images")
        rec_formset = RecommendationFormSet(request.POST, instance=report, prefix="recommendations")
        file_formset = FileFormSet(request.POST, request.FILES, instance=report, prefix="files")

        # ฟอร์มพิเศษตามประเภท
        report_type = report.report_type
        additional_form = None
        if report_type in [ReportTypeChoices.HAZARD_GROUND, ReportTypeChoices.SAFETY_GROUND, ReportTypeChoices.MINOR_ACCIDENT_GROUND, ReportTypeChoices.MAJOR_ACCIDENT_GROUND]:
            additional_form = GroundReportForm(request.POST, instance=report, prefix="ground")
        elif report_type in [ReportTypeChoices.HAZARD_AVIATION, ReportTypeChoices.SAFETY_AVIATION, ReportTypeChoices.ANALYSIS_AVIATION, ReportTypeChoices.BIRD_AVIATION, ReportTypeChoices.FIX_ANALYSIS_AVIATION]:
            additional_form = AviationReportForm(request.POST, instance=report, prefix="aviation")

        # ตรวจสอบความถูกต้องทั้งหมด
        form_list = [
                base_form, image_formset, rec_formset, file_formset, participant_formset, reference_formset
            ]
        if additional_form:
            form_list.append(additional_form)

        if all(form.is_valid() for form in form_list):
            try:
                with transaction.atomic():
                    base_report = base_form.save()

                    # Save all formsets
                    save_formset_with_parent(image_formset, base_report)
                    save_formset_with_parent(rec_formset, base_report)
                    save_formset_with_parent(file_formset, base_report)
                    save_formset_with_parent(participant_formset, base_report)
                    save_formset_with_parent(reference_formset, base_report)

                    if additional_form:
                        additional_form.save()

                messages.success(request, f"อัปเดตรายงาน {base_report} เรียบร้อยแล้ว")
                return redirect("report:safety-report.list")
            except Exception as e:
                logger.exception(f"Error updating report #{report.id}: {e}")
                messages.error(request, "เกิดข้อผิดพลาดขณะอัปเดตรายงาน กรุณาลองใหม่อีกครั้ง")
        else:
            messages.error(request, "กรุณาตรวจสอบข้อมูลอีกครั้งก่อนบันทึก")
            print_form_errors(form_list)
    else:
        # GET Method
        base_form = BaseReportForm(instance=report, prefix="base_form", user=request.user)
        participant_formset = ParticipantFormSet(prefix="participants", instance=report)
        reference_formset = ReferenceReportFormSet(prefix="references", instance=report)
        image_formset = ImageFormSet(prefix="images", instance=report)
        rec_formset = RecommendationFormSet(prefix="recommendations", instance=report)
        file_formset = FileFormSet(prefix="files", instance=report)

        additional_form = None
        if report.report_type in [ReportTypeChoices.HAZARD_GROUND, ReportTypeChoices.SAFETY_GROUND]:
            additional_form = GroundReportForm(prefix="ground", instance=report)
        elif report.report_type in [ReportTypeChoices.HAZARD_AVIATION, ReportTypeChoices.SAFETY_AVIATION]:
            additional_form = AviationReportForm(prefix="aviation", instance=report)

    context = {
        "report": report,
        "base_form": base_form,
        "participant_formset": participant_formset,
        "reference_formset": reference_formset,
        "image_formset": image_formset,
        "recommendation_formset": rec_formset,
        "file_formset": file_formset,
        "additional_form": additional_form,
        "ReportTypeChoices": ReportTypeChoices,
    }
    return render(request, "Report/safety-reports/report-edit.html", context)


def save_formset_with_parent(formset, parent):
    """บันทึกฟอร์มเซ็ตพร้อม parent"""
    instances = formset.save(commit=False)
    for obj in instances:
        obj.base_report = parent
        obj.save()
    for obj in formset.deleted_objects:
        obj.delete()


def print_form_errors(forms):
    """พิมพ์ error ของทุกฟอร์มเพื่อ debug"""
    for f in forms:
        if hasattr(f, "errors") and f.errors:
            print(f"{f.__class__.__name__} Errors:", f.errors)
