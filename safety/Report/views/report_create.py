from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from ..forms.reports import (
    BaseReportForm,
    GroundReportForm,
    AviationReportForm
)
from ..forms.attachments import (
    ImageFormSet,
    RecommendationFormSet,
    FileFormSet,
    BulkAttachmentForm
)
from ..constants import default_content
from ..choices import ReportTypeChoices
from ..services.reports import save_new_report
from common.RTAFUser.models import Affiliation


@login_required
def new_report(request):
    """
    Policy:
    - new_report = SIMPLE report only
    - report_type is ALWAYS ReportTypeChoices.SIMPLE
    """

    # ======================
    # GET
    # ======================
    if request.method == "GET":
        initial, affiliation, report_type = extract_get_params(request)
        context = build_context_for_get(initial, report_type, affiliation)
        return render(
            request,
            "Report/safety-reports/report-create.html",
            context
        )

    # ======================
    # POST
    # ======================
    base_form = BaseReportForm(
        request.POST,
        prefix="base_form",
        user=request.user
    )
    image_formset = ImageFormSet(
        request.POST,
        request.FILES,
        prefix="images"
    )
    rec_formset = RecommendationFormSet(
        request.POST,
        prefix="recommendations"
    )
    file_formset = FileFormSet(
        request.POST,
        request.FILES,
        prefix="files"
    )

    bulk_form = BulkAttachmentForm(
        request.POST,
        request.FILES
    )

    priority = request.POST.get("priority", "L")

    if all(form.is_valid() for form in [
        base_form,
        image_formset,
        rec_formset,
        file_formset
    ]):
        # 🔒 Enforce SIMPLE report
        base_form.instance.report_type = ReportTypeChoices.SIMPLE

        base_report = save_new_report(
            request,
            base_form,
            image_formset,
            rec_formset,
            file_formset,
            priority
        )

        # Optional bulk attachments
        if bulk_form.is_valid():
            bulk_form.save(base_report, request.user)

        return handle_post_success(request, base_report)

    return handle_post_failure(
        request,
        base_form,
        image_formset,
        rec_formset,
        file_formset,
        bulk_form
    )


# ======================================================
# Helper functions
# ======================================================

def extract_get_params(request):
    """
    GET policy:
    - Ignore report_type from URL
    - Always use SIMPLE
    """
    affiliation_id = request.GET.get("affiliation")
    affiliation = (
        Affiliation.objects.get(id=affiliation_id)
        if affiliation_id
        else None
    )

    report_type = ReportTypeChoices.SIMPLE

    initial = {
        "affiliation": affiliation,
        "report_type": report_type,
        "content": (
            affiliation.airviation_content
            if affiliation and affiliation.airviation_content
            else default_content
        ),
    }
    return initial, affiliation, report_type


def build_context_for_get(initial, report_type, affiliation):
    context = {
        "base_form": BaseReportForm(
            prefix="base_form",
            initial=initial
        ),
        "image_formset": ImageFormSet(prefix="images"),
        "recommendation_formset": RecommendationFormSet(prefix="recommendations"),
        "file_formset": FileFormSet(prefix="files"),
        "bulk_form": BulkAttachmentForm(),
        "ReportTypeChoices": ReportTypeChoices,
        "report_type": report_type,
    }

    # SIMPLE report has no extra forms
    return context


def handle_post_success(request, base_report):
    messages.success(
        request,
        f"บันทึกเหตุการณ์ {base_report} เรียบร้อยแล้ว"
    )

    if request.POST.get("surveyCheck") == "1":
        return redirect(
            "evaluate:evaluate-main",
            report_id=base_report.id
        )

    return redirect("report:safety-report.list")


def handle_post_failure(
    request,
    base_form,
    image_formset,
    rec_formset,
    file_formset,
    bulk_form
):
    messages.error(
        request,
        "กรุณาตรวจสอบข้อมูลให้ถูกต้อง"
    )

    context = {
        "base_form": base_form,
        "image_formset": image_formset,
        "recommendation_formset": rec_formset,
        "file_formset": file_formset,
        "bulk_form": bulk_form,
        "ReportTypeChoices": ReportTypeChoices,
        "report_type": ReportTypeChoices.SIMPLE,
    }

    return render(
        request,
        "Report/safety-reports/report-create.html",
        context
    )
