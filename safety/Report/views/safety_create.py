from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from ..forms.reports import BaseReportForm, GroundReportForm, AviationReportForm
from ..forms.attachments import ImageFormSet, RecommendationFormSet, FileFormSet
from ..constants import default_content
from ..choices import ReportTypeChoices
from ..services.reports import save_new_report
from common.RTAFUser.models import Affiliation



        
@login_required
def new_report(request):
    if request.method == "GET":
        affiliation = Affiliation.objects.get(id=request.GET.get("affiliation")) if request.GET.get("affiliation") else None
        report_type = request.GET.get("report_type", "")

        initial = {
            "affiliation": affiliation,
            "report_type": report_type,
            "content": affiliation.airviation_content if affiliation and affiliation.airviation_content else default_content,
        }
        
        context = {
            "base_form": BaseReportForm(prefix="base_form", initial=initial),
            "image_formset": ImageFormSet(prefix="images"),
            "recommendation_formset": RecommendationFormSet(prefix="recommendations"),
            "file_formset": FileFormSet(prefix="files"),
            
            "ReportTypeChoices" : ReportTypeChoices,
            "report_type": report_type,
        }

        if report_type in [ReportTypeChoices.HAZARD_GROUND, ReportTypeChoices.SAFETY_GROUND]:
            context["ground_form"] = GroundReportForm(prefix="ground")
        elif report_type in [ReportTypeChoices.HAZARD_AVIATION, ReportTypeChoices.SAFETY_AVIATION]:
            initial_form = {'affiliation': affiliation} if affiliation else {}
            context["aviation_form"] = AviationReportForm(prefix="aviation", initial=initial_form)

        return render(request, "Report/safety-reports/safety-create.new-report.html", context)

    # in case request.method == "POST":
    print("Processing POST request for new report")
    print("POST data:", request.POST)
    base_form = BaseReportForm(request.POST, prefix="base_form")
    image_formset = ImageFormSet(request.POST, request.FILES, prefix="images")
    rec_formset = RecommendationFormSet(request.POST, prefix="recommendations")
    file_formset = FileFormSet(request.POST, request.FILES, prefix="files")
    
    priority = request.POST.get('priority',"L")

    report_type = request.POST.get("base_form-report_type", "")

    forms_valid = [base_form.is_valid(), image_formset.is_valid(), rec_formset.is_valid(), file_formset.is_valid()]

    addition_form = {}
    if report_type in [ReportTypeChoices.HAZARD_GROUND, ReportTypeChoices.SAFETY_GROUND]:
        ground_form = GroundReportForm(request.POST, prefix="ground")
        forms_valid.append(ground_form.is_valid())
        addition_form['ground_form'] = ground_form
    elif report_type in [ReportTypeChoices.HAZARD_AVIATION, ReportTypeChoices.SAFETY_AVIATION]:
        aviation_form = AviationReportForm(request.POST, prefix="aviation")
        forms_valid.append(aviation_form.is_valid())
        addition_form['aviation_form'] = aviation_form

    if all(forms_valid):
        base_form.instance.report_type = report_type
        base_report = save_new_report(base_form, image_formset, rec_formset, file_formset, request, priority, **addition_form)
        messages.success(request, f"บันทึกเหตุการณ์ {base_report} เรียบร้อยแล้ว")
        if request.POST.get("surveyCheck") == "1":
            return redirect("evaluate:evaluate-main", report_id=base_report.id)
        else:
            return redirect("report:safety-report.list")


    
    messages.error(request, "กรุณาตรวจสอบข้อมูลให้ถูกต้อง")
    return render(request, "Report/safety-reports/safety-create.new-report.html", {
        "base_form": base_form,
        "image_formset": image_formset,
        "recommendation_formset": rec_formset,
        "file_formset": file_formset,
    })