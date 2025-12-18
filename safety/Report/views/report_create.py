from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect

from ..forms.reports import BaseReportForm, GroundReportForm, AviationReportForm
from ..forms.attachments import ImageFormSet, RecommendationFormSet, FileFormSet, BulkAttachmentForm
from ..constants import default_content
from ..choices import ReportTypeChoices
from ..services.reports import save_new_report
from common.RTAFUser.models import Affiliation

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required 
def new_report(request):

    if request.method == "GET":
        initial, affiliation, report_type = extract_get_params(request)
        context = build_context_for_get(initial, report_type, affiliation)
        return render(request, "Report/safety-reports/report-create.html", context)

    # POST
    base_form = BaseReportForm(request.POST, prefix="base_form")
    image_formset = ImageFormSet(request.POST, request.FILES, prefix="images")
    rec_formset = RecommendationFormSet(request.POST, prefix="recommendations")
    file_formset = FileFormSet(request.POST, request.FILES, prefix="files")
    
    bulk_form = BulkAttachmentForm(request.POST, request.FILES)
    
    report_type = request.POST.get("base_form-report_type", "")
    priority = request.POST.get("priority", "L")
    

    if all(form.is_valid() for form in [base_form, image_formset, rec_formset, file_formset]):
        base_form.instance.report_type = report_type
        base_report = save_new_report(request, base_form, image_formset, rec_formset, file_formset, priority)
        
        #เสริม bulk แบบ optional
        if bulk_form.is_valid():
            bulk_form.save(base_report, request.user)
        
        return handle_post_success(request, base_report)
    

    return handle_post_failure([base_form, image_formset, rec_formset, file_formset],{"bulk_form": bulk_form})

# --- Subfunctions ---

def extract_get_params(request):
    affiliation_id = request.GET.get("affiliation")
    
    affiliation = (Affiliation.objects.get(id=affiliation_id)
        if affiliation_id
        else request.user.work_affiliation or request.user.affiliation
    )
    
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
        "image_formset": ImageFormSet(prefix="images"),
        "recommendation_formset": RecommendationFormSet(prefix="recommendations"),
        "file_formset": FileFormSet(prefix="files"),
        "bulk_form": BulkAttachmentForm(), 
        "ReportTypeChoices": ReportTypeChoices,
        "report_type": report_type,
    }
    if report_type in [ReportTypeChoices.HAZARD_GROUND, ReportTypeChoices.SAFETY_GROUND]:
        context["ground_form"] = GroundReportForm(prefix="ground")
    elif report_type in [ReportTypeChoices.HAZARD_AVIATION, ReportTypeChoices.SAFETY_AVIATION]:
        aviation_initial = {"affiliation": affiliation} if affiliation else {}
        context["aviation_form"] = AviationReportForm(prefix="aviation", initial=aviation_initial)
    return context


def handle_post_success(request, base_report):
    messages.success(request, f"บันทึกเหตุการณ์ {base_report} เรียบร้อยแล้ว")
    if request.POST.get("surveyCheck") == "1":
        return redirect("evaluate:evaluate-main", report_id=base_report.id)
    return redirect("report:safety-report.list")


def handle_post_failure(forms, addition_context):
    messages.error(forms[0].request, "กรุณาตรวจสอบข้อมูลให้ถูกต้อง") if hasattr(forms[0], 'request') else messages.error(None, "กรุณาตรวจสอบข้อมูลให้ถูกต้อง")
    context = {
        "base_form": forms[0],
        "image_formset": forms[1],
        "recommendation_formset": forms[2],
        "file_formset": forms[3],
        **addition_context,
        "ReportTypeChoices": ReportTypeChoices,
    }
    return render(forms[0].request if hasattr(forms[0], 'request') else None, "Report/safety-reports/report-create.html", context)
