from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect

from ..forms.reports import BaseReportForm, GroundReportForm, AviationReportForm, ParticipantForm, ParticipantFormSet, ReferenceReportForm, ReferenceReportFormSet
from ..forms.attachments import ImageFormSet, RecommendationFormSet, FileFormSet
from ..constants import default_content
from ..choices import ReportTypeChoices
from ..services.reports import save_new_report_officer
from common.RTAFUser.models import Affiliation
from ..forms.attachments import BulkAttachmentForm


@login_required
@permission_required("Report.create_report", raise_exception=True)
def new_report(request):
    if request.method == "GET":
        initial, affiliation, report_type = extract_get_params(request)
        context = build_context_for_get(initial, report_type, affiliation)
        return render(request, "Report/safety-reports/report-create-officer.html", context)

    base_form = BaseReportForm(request.POST, prefix="base_form")
    participant_formset = ParticipantFormSet(request.POST, prefix="participants")
    image_formset = ImageFormSet(request.POST, request.FILES, prefix="images")
    rec_formset = RecommendationFormSet(request.POST, prefix="recommendations")
    file_formset = FileFormSet(request.POST, request.FILES, prefix="files")
    reference_formset = ReferenceReportFormSet(request.POST, prefix="references")

    bulk_form = BulkAttachmentForm(request.POST, request.FILES)

    report_type = request.POST.get("base_form-report_type", "")
    priority = request.POST.get("priority", "L")

    additional_form, addition_context = build_additional_form(report_type, request)

    forms_to_validate = [
        base_form,
        participant_formset,
        image_formset,
        rec_formset,
        file_formset,
        reference_formset,
    ]
    if additional_form:
        forms_to_validate.append(additional_form)

    if all(form.is_valid() for form in forms_to_validate):
        base_form.instance.report_type = report_type

        base_report = save_new_report_officer(
            request,
            base_form,
            participant_formset,
            image_formset,
            rec_formset,
            file_formset,
            reference_formset,
            priority,
            **addition_context
        )

        if bulk_form.is_valid():
            bulk_form.save(base_report, request.user)

        return handle_post_success(request, base_report)

    return handle_post_failure(
        [
            base_form,
            participant_formset,
            image_formset,
            rec_formset,
            file_formset,
            reference_formset,
        ],
        {"bulk_form": bulk_form, **addition_context},
    )


# --- Subfunctions ---
def extract_get_params(request):
    affiliation_id = request.GET.get("affiliation")
    affiliation = Affiliation.objects.get(id=affiliation_id) if affiliation_id else None
    report_type = request.GET.get("report_type", "")
    initial = {
        "affiliation": affiliation,
        "report_type": report_type,
        "content": affiliation.airviation_content if affiliation and affiliation.airviation_content else default_content,
    }
    return initial, affiliation, report_type


def build_context_for_get(initial, report_type, affiliation):
    context = {
        "base_form": BaseReportForm(prefix="base_form", initial=initial),
        "participant_formset": ParticipantFormSet(prefix="participants"),
        "image_formset": ImageFormSet(prefix="images"),
        "recommendation_formset": RecommendationFormSet(prefix="recommendations"),
        "file_formset": FileFormSet(prefix="files"),
        "reference_formset": ReferenceReportFormSet(prefix="references"),
        "bulk_form": BulkAttachmentForm(),
        "ReportTypeChoices": ReportTypeChoices,
        "report_type": report_type,
    }

    if report_type in [
        ReportTypeChoices.HAZARD_GROUND,
        ReportTypeChoices.SAFETY_GROUND,
        ReportTypeChoices.MINOR_ACCIDENT_GROUND,
        ReportTypeChoices.MAJOR_ACCIDENT_GROUND,
    ]:
        context["ground_form"] = GroundReportForm(prefix="ground")

    elif report_type in [
        ReportTypeChoices.HAZARD_AVIATION,
        ReportTypeChoices.SAFETY_AVIATION,
        ReportTypeChoices.ANALYSIS_AVIATION,
        ReportTypeChoices.BIRD_AVIATION,
        ReportTypeChoices.FIX_ANALYSIS_AVIATION,
    ]:
        aviation_initial = {"affiliation": affiliation} if affiliation else {}
        context["aviation_form"] = AviationReportForm(
            prefix="aviation", initial=aviation_initial
        )

    return context


def build_additional_form(report_type, request):
    if report_type in [
        ReportTypeChoices.HAZARD_GROUND,
        ReportTypeChoices.SAFETY_GROUND,
        ReportTypeChoices.MINOR_ACCIDENT_GROUND,
        ReportTypeChoices.MAJOR_ACCIDENT_GROUND,
    ]:
        ground_form = GroundReportForm(request.POST, prefix="ground")
        return ground_form, {"ground_form": ground_form}

    elif report_type in [
        ReportTypeChoices.HAZARD_AVIATION,
        ReportTypeChoices.SAFETY_AVIATION,
        ReportTypeChoices.ANALYSIS_AVIATION,
        ReportTypeChoices.BIRD_AVIATION,
        ReportTypeChoices.FIX_ANALYSIS_AVIATION,
    ]:
        aviation_form = AviationReportForm(request.POST, prefix="aviation")
        return aviation_form, {"aviation_form": aviation_form}

    return None, {}


def handle_post_success(request, base_report):
    messages.success(request, f"บันทึกเหตุการณ์ {base_report} เรียบร้อยแล้ว")
    if request.POST.get("surveyCheck") == "1":
        return redirect("evaluate:evaluate-main", report_id=base_report.id)
    return redirect("report:safety-report.list")


def handle_post_failure(forms, addition_context):
    messages.error(None, "กรุณาตรวจสอบข้อมูลให้ถูกต้อง")
    context = {
        "base_form": forms[0],
        "participant_formset": forms[1],
        "image_formset": forms[2],
        "recommendation_formset": forms[3],
        "file_formset": forms[4],
        "reference_formset": forms[5],
        **addition_context,
        "ReportTypeChoices": ReportTypeChoices,
    }
    return render(
        None,
        "Report/safety-reports/report-create-officer.html",
        context,
    )
