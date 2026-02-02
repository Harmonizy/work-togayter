from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction

from ..models import BaseReport
from ..forms.reports import (
    BaseReportForm, GroundReportForm, AviationReportForm,
    ParticipantFormSet, ReferenceReportFormSet
)
from ..forms.attachments import (
    ImageFormSet, RecommendationFormSet, FileFormSet,
    BulkAttachmentForm  
)
from ..choices import ReportTypeChoices, ReportStatusChoices

import logging
logger = logging.getLogger("report")

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render


@login_required
@permission_required("Report.edit_report", raise_exception=True)
def edit_report(request, report_id):
    base_report = get_object_or_404(BaseReport, pk=report_id)

    report_type = base_report.report_type
    affiliation = base_report.affiliation

    # ======================
    # GET
    # ======================
    if request.method == "GET":
        context = build_context_for_edit(
            base_report=base_report,
            report_type=report_type,
            affiliation=affiliation,
        )
        return render(
            request,
            "Report/safety-reports/report-edit.html",
            context
        )

    # ======================
    # POST
    # ======================
    base_form = BaseReportForm(
        request.POST,
        instance=base_report,
        prefix="base_form",
        user=request.user,
    )

    participant_formset = ParticipantFormSet(
        request.POST,
        instance=base_report,
        prefix="participants",
    )

    image_formset = ImageFormSet(
        request.POST,
        request.FILES,
        instance=base_report,
        prefix="images",
    )

    rec_formset = RecommendationFormSet(
        request.POST,
        instance=base_report,
        prefix="recommendations",
    )

    file_formset = FileFormSet(
        request.POST,
        request.FILES,
        instance=base_report,
        prefix="files",
    )

    reference_formset = ReferenceReportFormSet(
        request.POST,
        instance=base_report,
        prefix="references",
    )

    bulk_form = BulkAttachmentForm(
        request.POST or None,
        request.FILES or None,
    )

    additional_form, addition_context = build_additional_form_edit(
        report_type,
        request,
        base_report,
    )

    forms_valid = (
        base_form.is_valid()
        and participant_formset.is_valid()
        and image_formset.is_valid()
        and rec_formset.is_valid()
        and file_formset.is_valid()
        and reference_formset.is_valid()
        and (additional_form.is_valid() if additional_form else True)
    )

    if forms_valid:
        base_report = base_form.save()

        participant_formset.instance = base_report
        participant_formset.save()

        image_formset.instance = base_report
        image_formset.save()

        rec_formset.instance = base_report
        rec_formset.save()

        file_formset.instance = base_report
        file_formset.save()

        reference_formset.instance = base_report
        reference_formset.save()

        if additional_form:
            additional_form.save()

        if bulk_form.is_valid():
            bulk_form.save(base_report, request.user)

        messages.success(request, "แก้ไขรายงานเรียบร้อยแล้ว")
        return redirect(
            "report:safety-report.detail",
            pk=base_report.pk
        )

    messages.error(request, "กรุณาตรวจสอบข้อมูล")

    return render(
        request,
        "Report/safety-reports/report-edit-officer.html",
        {
            "base_report": base_report,
            "base_form": base_form,
            "participant_formset": participant_formset,
            "image_formset": image_formset,
            "recommendation_formset": rec_formset,
            "file_formset": file_formset,
            "reference_formset": reference_formset,
            "bulk_form": bulk_form,
            **addition_context,
            "report_type": report_type,
            "ReportTypeChoices": ReportTypeChoices,
        }
    )



def build_context_for_edit(base_report, report_type, affiliation):
    context = {
        "base_form": BaseReportForm(
            instance=base_report,
            prefix="base_form"
        ),
        "participant_formset": ParticipantFormSet(
            instance=base_report,
            prefix="participants"
        ),
        "image_formset": ImageFormSet(
            instance=base_report,
            prefix="images"
        ),
        "recommendation_formset": RecommendationFormSet(
            instance=base_report,
            prefix="recommendations"
        ),
        "file_formset": FileFormSet(
            instance=base_report,
            prefix="files"
        ),
        "reference_formset": ReferenceReportFormSet(
            instance=base_report,
            prefix="references"
        ),
        "bulk_form": BulkAttachmentForm(),
        "report_type": report_type,
        "ReportTypeChoices": ReportTypeChoices,
    }

    if report_type in [
        ReportTypeChoices.HAZARD_GROUND,
        ReportTypeChoices.SAFETY_GROUND,
        ReportTypeChoices.MINOR_ACCIDENT_GROUND,
        ReportTypeChoices.MAJOR_ACCIDENT_GROUND,
    ]:
        context["ground_form"] = GroundReportForm(
            instance=base_report.groundreport,
            prefix="ground"
        )

    elif report_type in [
        ReportTypeChoices.HAZARD_AVIATION,
        ReportTypeChoices.SAFETY_AVIATION,
        ReportTypeChoices.ANALYSIS_AVIATION,
        ReportTypeChoices.BIRD_AVIATION,
        ReportTypeChoices.FIX_ANALYSIS_AVIATION,
    ]:
        context["aviation_form"] = AviationReportForm(
            instance=base_report.aviationreport,
            prefix="aviation",
            initial={"affiliation": affiliation}
        )

    return context


def build_additional_form_edit(report_type, request, base_report):
    if report_type in [
        ReportTypeChoices.HAZARD_GROUND,
        ReportTypeChoices.SAFETY_GROUND,
        ReportTypeChoices.MINOR_ACCIDENT_GROUND,
        ReportTypeChoices.MAJOR_ACCIDENT_GROUND,
    ]:
        form = GroundReportForm(
            request.POST,
            instance=base_report.groundreport,
            prefix="ground"
        )
        return form, {"ground_form": form}

    elif report_type in [
        ReportTypeChoices.HAZARD_AVIATION,
        ReportTypeChoices.SAFETY_AVIATION,
        ReportTypeChoices.ANALYSIS_AVIATION,
        ReportTypeChoices.BIRD_AVIATION,
        ReportTypeChoices.FIX_ANALYSIS_AVIATION,
    ]:
        form = AviationReportForm(
            request.POST,
            instance=base_report.aviationreport,
            prefix="aviation"
        )
        return form, {"aviation_form": form}

    return None, {}
