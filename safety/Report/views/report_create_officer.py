from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect

from ..forms.reports import BaseReportForm, GroundReportForm, AviationReportForm, ParticipantForm, ParticipantFormSet
from ..forms.attachments import ImageFormSet, RecommendationFormSet, FileFormSet
from ..constants import default_content
from ..choices import ReportTypeChoices
from ..services.reports import save_new_report
from common.RTAFUser.models import Affiliation


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
# @permission_required("Report.create_safety_report", raise_exception=True)
def new_report(request):
    if request.method == "GET":
        initial, affiliation, report_type = extract_get_params(request)
        context = build_context_for_get(initial, report_type, affiliation)
        return render(request, "Report/safety-reports/report-create-officer.html", context)

    # POST
    base_form = BaseReportForm(request.POST, prefix="base_form")
    participant_formset = ParticipantFormSet(request.POST, prefix="participants")
    image_formset = ImageFormSet(request.POST, request.FILES, prefix="images")
    rec_formset = RecommendationFormSet(request.POST, prefix="recommendations")
    file_formset = FileFormSet(request.POST, request.FILES, prefix="files")

    report_type = request.POST.get("base_form-report_type", "")
    priority = request.POST.get("priority", "L")

    additional_form, addition_context = build_additional_form(report_type, request)

    forms_to_validate = [
        base_form, participant_formset, image_formset, rec_formset, file_formset
    ]
    if additional_form:
        forms_to_validate.append(additional_form)

    if all(form.is_valid() for form in forms_to_validate):
        base_form.instance.report_type = report_type
        base_report = save_new_report(request, base_form, participant_formset, image_formset, rec_formset, file_formset, priority, **addition_context)
        return handle_post_success(request, base_report)

    return handle_post_failure([base_form, participant_formset, image_formset, rec_formset, file_formset], addition_context)


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
    """สร้าง context สำหรับ GET request"""
    context = {
        "base_form": BaseReportForm(prefix="base_form", initial=initial),
        "participant_formset": ParticipantFormSet(prefix="participants"),
        "image_formset": ImageFormSet(prefix="images"),
        "recommendation_formset": RecommendationFormSet(prefix="recommendations"),
        "file_formset": FileFormSet(prefix="files"),
        "ReportTypeChoices": ReportTypeChoices,
        "report_type": report_type,
    }
    if report_type in [ReportTypeChoices.HAZARD_GROUND, ReportTypeChoices.SAFETY_GROUND]:
        context["ground_form"] = GroundReportForm(prefix="ground")
    elif report_type in [ReportTypeChoices.HAZARD_AVIATION, ReportTypeChoices.SAFETY_AVIATION]:
        aviation_initial = {"affiliation": affiliation} if affiliation else {}
        context["aviation_form"] = AviationReportForm(prefix="aviation", initial=aviation_initial)
    return context


def build_additional_form(report_type, request):
    """สร้างฟอร์มเพิ่มเติมตามประเภท report"""
    if report_type in [ReportTypeChoices.HAZARD_GROUND, ReportTypeChoices.SAFETY_GROUND]:
        ground_form = GroundReportForm(request.POST, prefix="ground")
        return ground_form, {"ground_form": ground_form}
    elif report_type in [ReportTypeChoices.HAZARD_AVIATION, ReportTypeChoices.SAFETY_AVIATION]:
        aviation_form = AviationReportForm(request.POST, prefix="aviation")
        return aviation_form, {"aviation_form": aviation_form}
    return None, {}


def handle_post_success(request, base_report):
    """จัดการหลังจากบันทึกสำเร็จ"""
    messages.success(request, f"บันทึกเหตุการณ์ {base_report} เรียบร้อยแล้ว")
    if request.POST.get("surveyCheck") == "1":
        return redirect("evaluate:evaluate-main", report_id=base_report.id)
    return redirect("report:safety-report.list")


def handle_post_failure(forms, addition_context):
    """จัดการเมื่อบันทึกไม่สำเร็จ"""
    messages.error(None, "กรุณาตรวจสอบข้อมูลให้ถูกต้อง")
    context = {
        "base_form": forms[0],
        "participant_formset": forms[1],
        "image_formset": forms[2],
        "recommendation_formset": forms[3],
        "file_formset": forms[4],
        **addition_context,
        "ReportTypeChoices": ReportTypeChoices,
    }
    return render(None, "Report/safety-reports/report-create-officer.html", context)